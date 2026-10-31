from datetime import datetime
from typing import Any, Generic, Literal, TypeVar

from ninja import ModelSchema, Schema

from vote.models import Ballot, Event
from voting_systems.types import AllResultTypes

T = TypeVar("T")

type EventStatus = Literal["RE", "CL", "VO"]


class EventStatusUpdateBody(Schema):
    allow_registration: bool | None = None
    allow_voting: bool | None = None
    show_results: bool | None = None


class ChoiceID(Schema):
    id: int


class ChoiceAlias(Schema):
    alias: str | None = None


class ChoiceLabel(Schema):
    label: str


class ChoiceWithLabel(ChoiceID, ChoiceLabel):
    pass


class ChoiceWithAlias(ChoiceID, ChoiceAlias):
    pass


class ChoiceSchema(ChoiceID, ChoiceLabel, ChoiceAlias):
    pass


class ChoiceInput(ChoiceLabel, ChoiceAlias):
    pass


class EventCreationBody(Schema):
    name: str
    choices: list[ChoiceInput]
    electoral_system: str
    allow_registration: bool = False
    allow_voting: bool = False


class EventDetails(ModelSchema):
    class Meta:
        model = Event
        fields = [  # noqa: RUF012
            "id",
            "name",
            "electoral_system",
            "allow_registration",
            "allow_voting",
            "closed",
            "share_token",
            "show_results",
            "result",
            "host_token",
        ]

    choices: list[ChoiceSchema]


class EventCloseResponse(Schema):
    closed: datetime


class EventCreationResponse(ModelSchema):
    class Meta:
        model = Event
        fields = [  # noqa: RUF012
            "id",
            "name",
            "electoral_system",
            "allow_registration",
            "allow_voting",
            "closed",
            "share_token",
            "show_results",
            "result",
            "host_token",
        ]

    choices: list[ChoiceSchema]


class BallotSchema(ModelSchema):
    class Meta:
        model = Ballot
        fields = ["id", "voter_name", "vote", "created", "submitted"]  # noqa: RUF012


class CreateBallotSchema(ModelSchema):
    class Meta:
        model = Ballot
        fields = ["id", "voter_name", "vote", "created", "submitted", "token"]  # noqa: RUF012


class BallotSubmission(Schema):
    vote: Any
