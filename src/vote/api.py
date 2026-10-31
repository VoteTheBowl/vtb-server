import uuid
from datetime import UTC, datetime

from django.db import IntegrityError
from django.shortcuts import aget_object_or_404
from ninja import Header, Router
from ninja.errors import AuthorizationError, HttpError, ValidationError
from pydantic import TypeAdapter

import voting_systems
from vote.schemas import (
    BallotSchema,
    BallotSubmission,
    CreateBallotSchema,
    EventCloseResponse,
    EventCreationBody,
    EventCreationResponse,
    EventDetails,
    EventStatusUpdateBody,
)

from .models import Ballot, Choice, Event

router = Router()


@router.post(
    "/event/create",
    response={201: EventCreationResponse},
    tags=["event"],
)
async def create_event(request, payload: EventCreationBody):
    event = await Event.objects.acreate(
        name=payload.name,
        electoral_system=payload.electoral_system,
        allow_registration=payload.allow_registration,
        allow_voting=payload.allow_voting,
    )

    choice_models: list[Choice] = []

    for choice in payload.choices:
        choice_models.append(
            Choice(event=event, label=choice.label, alias=choice.alias)
        )

    await event.choices.aset(choice_models, bulk=False)
    await event.asave()

    new_event = await Event.objects.prefetch_related("choices").aget(pk=event.id)

    return 201, new_event


@router.get("/event/{event_id}", response=EventDetails, tags=["event"])
async def get_event(
    request, event_id: int, token: uuid.UUID = Header(alias="X-API-Key")
):
    event = await aget_object_or_404(
        Event.objects.prefetch_related("choices"), pk=event_id
    )

    isVoter = token in [x.token async for x in event.ballot_set.all()]

    if token != event.share_token and token != event.host_token and not isVoter:
        raise AuthorizationError

    if event.show_results is False and isVoter:
        event.result = None

    return event


@router.patch(
    "/event/{event_id}",
    response={200: EventCreationResponse},
    tags=["event"],
)
async def patch_event(
    request,
    event_id: str,
    body: EventStatusUpdateBody,
    token: uuid.UUID = Header(alias="X-API-Key"),
):
    event = await aget_object_or_404(
        Event.objects.prefetch_related("choices"), pk=event_id
    )

    if token != event.host_token:
        raise AuthorizationError

    if body.allow_registration is not None:
        event.allow_registration = body.allow_registration

    if body.allow_voting is not None:
        event.allow_voting = body.allow_voting

    if body.show_results is not None:
        event.show_results = body.show_results

    await event.asave()
    return event


@router.post(
    "/event/{event_id}/close", response={200: EventCloseResponse}, tags=["event"]
)
async def close_event(
    request, event_id: str, token: uuid.UUID = Header(alias="X-API-Key")
):
    event = await aget_object_or_404(Event, pk=event_id)

    if token != event.host_token:
        raise AuthorizationError

    event.closed = datetime.now(tz=UTC)
    event.allow_registration = False
    event.allow_voting = False
    await event.asave()

    return EventCloseResponse(closed=event.closed)


@router.post(
    "/event/{event_id}/calculate",
    response=voting_systems.types.AllResultTypes,
    tags=["event"],
)
async def calculate_event_result(
    request, event_id: str, token: uuid.UUID = Header(alias="X-API-Key")
):
    event = await aget_object_or_404(Event, pk=event_id)

    if token != event.host_token or (event.closed is None):
        raise AuthorizationError

    if event.electoral_system not in voting_systems.config:
        raise NotImplementedError

    if event.result:
        raise HttpError(409, "The result has already been calculated.")

    result = voting_systems.config[event.electoral_system]["result"](
        [choice.id async for choice in event.choices.all()],
        [x.vote async for x in event.ballot_set.all()],
    )

    event.result = result
    await event.asave()

    return result


# Ballots
@router.post(
    "/event/{event_id}/create-ballot", response=CreateBallotSchema, tags=["ballot"]
)
async def create_ballot(
    request,
    event_id: str,
    voter_name: str,
    share_token: uuid.UUID = Header(alias="X-API-Key"),
):
    event = await aget_object_or_404(Event, pk=event_id)

    if share_token != event.share_token:
        raise AuthorizationError

    if not event.allow_registration:
        raise HttpError(409, "Cannot create ballot at this time")

    ballot = Ballot(event=event, voter_name=voter_name)

    try:
        await ballot.asave()
    except IntegrityError as err:
        if "unique_voter_names_in_event" in str(err):
            raise ValidationError("Duplicate voter name")
        else:
            raise err

    return ballot


@router.post("/ballot/{ballot_id}/submit", response=BallotSchema, tags=["ballot"])
async def submit_ballot(
    request,
    ballot_id: int,
    payload: BallotSubmission,
    token: uuid.UUID = Header(alias="X-API-Key"),
):
    ballot = await aget_object_or_404(
        Ballot.objects.prefetch_related("event"), pk=ballot_id
    )

    try:
        Adapter = TypeAdapter(
            voting_systems.config[ballot.event.electoral_system]["submissionType"]
        )
    except KeyError:
        raise NotImplementedError

    vote = Adapter.validate_python(payload.vote)

    if ballot.event.allow_voting is False or ballot.event.closed is not None:
        raise HttpError(409, "Event is not accepting ballots.")

    if token != ballot.token:
        raise AuthorizationError

    if ballot.submitted is not None:
        raise HttpError(409, "Ballot already submitted.")

    ballot.vote = vote
    ballot.submitted = datetime.now(tz=UTC)
    await ballot.asave()

    return ballot


@router.get("/event/{event_id}/ballots", response=list[BallotSchema], tags=["ballot"])
async def list_ballots(
    request, event_id: str, token: uuid.UUID = Header(alias="X-API-Key")
):
    event = await aget_object_or_404(Event, pk=event_id)

    if token != event.host_token and token not in [
        x.token async for x in event.ballot_set.all()
    ]:
        raise AuthorizationError

    if token != event.host_token and (
        event.closed is None or (event.closed and event.show_results is False)
    ):
        raise AuthorizationError

    return [x async for x in event.ballot_set.all().order_by("created", "submitted")]


@router.get("/ballot/{ballot_id}", response=BallotSchema, tags=["ballot"])
async def get_ballot(
    request, ballot_id: int, token: uuid.UUID = Header(alias="X-API-Key")
):
    ballot = await aget_object_or_404(
        Ballot.objects.prefetch_related("event"), pk=ballot_id
    )

    if token != ballot.token and token != ballot.event.host_token:
        raise AuthorizationError

    return ballot
