from datetime import datetime
from typing import Any, Literal, Optional, TypeVar

from ninja import ModelSchema, Schema

from vote.models import Ballot, Event

T = TypeVar("T")

type EventStatus = Literal["RE", "CL", "VO"]


class EventStatusUpdateBody(Schema):
    allow_registration: bool | None = None
    allow_voting: bool | None = None
    show_results: bool | None = None


class ChoiceSchema(Schema):
    id: int
    alias: str | None
    label: str
    string_id: str

    @staticmethod
    def resolve_label(obj, context):
        if "hide_choice_labels" in context and context["hide_choice_labels"] is True:
            return ""
        else:
            return obj.label


class ChoiceInput(Schema):
    label: str
    alias: str | None = None


class EventCreationBody(Schema):
    name: str
    choices: list[ChoiceInput]
    electoral_system: str
    allow_registration: bool = False
    allow_voting: bool = False
    hide_choice_labels: bool = False


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
            "hide_choice_labels",
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
            "hide_choice_labels",
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
