import uuid
from datetime import datetime, timezone

from django.test import TestCase
from ninja.testing import TestAsyncClient

from ..api import router
from ..models import Ballot, Choice, Event


class BallotTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.aclient = TestAsyncClient(router)
        cls.event = Event.objects.create(
            name="Big Cookoff",
            electoral_system="PL",
            allow_registration=True,
        )
        cls.event.choices.add(
            Choice(label="Tom's Texas Chili"),
            Choice(label="Jim's Vegan Chili"),
            Choice(label="Ed's Fusion Chili"),
            bulk=False,
        )
        cls.ballot = Ballot.objects.create(event=cls.event, voter_name="Becky")

    async def test_ballot_creation(self):
        response = await self.aclient.post(
            f"/event/{self.event.pk}/create-ballot",
            headers={"X-API-Key": self.event.share_token},
            query_params={
                "voter_name": "Don",
            },
        )

        self.assertEqual(response.status_code, 200)

    async def test_ballot_creation_with_duplicate_name(self):
        response = await self.aclient.post(
            f"/event/{self.event.pk}/create-ballot",
            headers={"X-API-Key": self.event.share_token},
            query_params={
                "voter_name": "Becky",
            },
        )
        self.assertEqual(response.status_code, 422)

    async def test_ballot_creation_with_bad_token(self):
        response = await self.aclient.post(
            f"/event/{self.event.pk}/create-ballot",
            headers={"X-API-Key": uuid.uuid4()},
            query_params={
                "voter_name": "Don",
            },
        )
        self.assertEqual(response.status_code, 403)

    async def test_ballot_creation_with_wrong_event_status(self):
        self.event.allow_registration = False
        self.event.allow_voting = True
        await self.event.asave()

        response = await self.aclient.post(
            f"/event/{self.event.pk}/create-ballot",
            headers={"X-API-Key": self.event.share_token},
            query_params={
                "voter_name": "Don",
            },
        )
        self.assertEqual(response.status_code, 409)

        self.event.allow_registration = False
        self.event.allow_voting = False
        await self.event.asave()

        response = await self.aclient.post(
            f"/event/{self.event.pk}/create-ballot",
            headers={"X-API-Key": self.event.share_token},
            query_params={
                "voter_name": "Don",
            },
        )
        self.assertEqual(response.status_code, 409)

    async def test_ballot_submission(self):
        self.event.allow_registration = False
        self.event.allow_voting = True
        await self.event.asave()

        vote = "Ed's Fusion Chili"

        response = await self.aclient.post(
            f"/ballot/{self.ballot.pk}/submit",
            headers={"X-API-Key": self.ballot.token},
            json={"vote": vote},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["vote"], vote)

    async def test_ballot_resubmission(self):
        self.event.allow_registration = False
        self.event.allow_voting = True
        await self.event.asave()

        submission = await self.aclient.post(
            f"/ballot/{self.ballot.pk}/submit",
            headers={"X-API-Key": self.ballot.token},
            json={"vote": "Ed's Fusion Chili"},
        )
        self.assertEqual(submission.status_code, 200)

        resubmission = await self.aclient.post(
            f"/ballot/{self.ballot.pk}/submit",
            headers={"X-API-Key": self.ballot.token},
            json={"vote": "Tom's Texas Chili"},
        )
        self.assertEqual(resubmission.status_code, 409)

    async def test_ballot_submission_with_bad_token(self):
        self.event.allow_registration = False
        self.event.allow_voting = True
        await self.event.asave()

        response = await self.aclient.post(
            f"/ballot/{self.ballot.pk}/submit",
            headers={"X-API-Key": uuid.uuid4()},
            json={"vote": "Ed's Fusion Chili"},
        )
        self.assertEqual(response.status_code, 403)

    async def test_ballot_submission_when_voting_not_allowed(self):
        self.event.allow_registration = False
        self.event.allow_voting = False
        await self.event.asave()

        response = await self.aclient.post(
            f"/ballot/{self.ballot.pk}/submit",
            headers={"X-API-Key": self.ballot.token},
            json={"vote": "Ed's Fusion Chili"},
        )
        self.assertEqual(response.status_code, 409)

    async def test_ballot_submission_when_event_closed(self):
        self.event.allow_registration = False
        self.event.allow_voting = True
        self.event.closed = datetime.now(timezone.utc)
        await self.event.asave()

        response = await self.aclient.post(
            f"/ballot/{self.ballot.pk}/submit",
            headers={"X-API-Key": self.ballot.token},
            json={"vote": "Ed's Fusion Chili"},
        )
        self.assertEqual(response.status_code, 409)

    async def test_ballot_list(self):
        event = Event(
            name="Small Cookoff",
            electoral_system="PL",
            allow_registration=False,
            allow_voting=False,
            closed=datetime.now(timezone.utc),
            show_results=True,
        )
        await event.asave()

        await Choice(label="Chilli 1", event=event).asave()
        await Choice(label="Chilli 2", event=event).asave()
        await Choice(label="Chilli 3", event=event).asave()

        ballot1 = Ballot(event=event, voter_name="Bob")
        ballot2 = Ballot(event=event, voter_name="Jeff")
        ballot3 = Ballot(event=event, voter_name="Billy")
        await ballot1.asave()
        await ballot2.asave()
        await ballot3.asave()

        response = await self.aclient.get(
            f"/event/{event.pk}/ballots",
            headers={"X-API-Key": event.host_token},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

        response = await self.aclient.get(
            f"/event/{event.pk}/ballots",
            headers={"X-API-Key": ballot1.token},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    async def test_ballot_list_unauthorized(self):
        event = Event(
            name="Small Cookoff",
            electoral_system="PL",
        )
        await event.asave()

        await Choice(label="Chilli 1", event=event).asave()
        await Choice(label="Chilli 2", event=event).asave()
        await Choice(label="Chilli 3", event=event).asave()

        event1 = Event(
            name="Big Cooky",
            electoral_system="PL",
        )
        await event1.asave()

        await Choice(label="Chilli 1", event=event1).asave()
        await Choice(label="Chilli 2", event=event1).asave()
        await Choice(label="Chilli 3", event=event1).asave()

        ballot = Ballot(event=event, voter_name="Train")

        ballot1 = Ballot(event=event, voter_name="Bob")
        ballot2 = Ballot(event=event, voter_name="Jeff")
        ballot3 = Ballot(event=event, voter_name="Billy")
        await ballot1.asave()
        await ballot2.asave()
        await ballot3.asave()

        response = await self.aclient.get(
            f"/event/{event.pk}/ballots",
            headers={"X-API-Key": event1.host_token},
        )

        self.assertEqual(response.status_code, 403)

        response = await self.aclient.get(
            f"/event/{event.pk}/ballots",
            headers={"X-API-Key": ballot.token},
        )

        self.assertEqual(response.status_code, 403)

    async def test_ballot_list_for_voter_event_not_closed(self):
        # TODO: Seperate out into individual tests
        event = Event(
            name="Small Cookoff",
            electoral_system="PL",
            show_results=True,
            allow_registration=True,
            allow_voting=False,
        )
        await event.asave()

        await Choice(label="Chilli 1", event=event).asave()
        await Choice(label="Chilli 2", event=event).asave()
        await Choice(label="Chilli 3", event=event).asave()

        ballot1 = Ballot(event=event, voter_name="Bob")
        await ballot1.asave()

        response = await self.aclient.get(
            f"/event/{event.pk}/ballots",
            headers={"X-API-Key": event.host_token},
        )

        self.assertEqual(response.status_code, 200)

        response = await self.aclient.get(
            f"/event/{event.pk}/ballots",
            headers={"X-API-Key": ballot1.token},
        )

        self.assertEqual(response.status_code, 403)

        event.allow_registration = False
        event.allow_voting = False
        event.show_results = False
        await event.asave()

        response = await self.aclient.get(
            f"/event/{event.pk}/ballots",
            headers={"X-API-Key": ballot1.token},
        )

        self.assertEqual(response.status_code, 403)

    async def test_get_ballot(self):
        response = await self.aclient.get(
            f"/ballot/{self.ballot.pk}",
            headers={"X-API-Key": self.ballot.token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["voter_name"], "Becky")

    async def test_get_ballot_with_event_host_token(self):
        response = await self.aclient.get(
            f"/ballot/{self.ballot.pk}",
            headers={"X-API-Key": self.event.host_token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["voter_name"], "Becky")

    async def test_get_ballot_random_token(self):
        response = await self.aclient.get(
            f"/ballot/{self.ballot.pk}",
            headers={"X-API-Key": uuid.uuid4()},
        )
        self.assertEqual(response.status_code, 403)
