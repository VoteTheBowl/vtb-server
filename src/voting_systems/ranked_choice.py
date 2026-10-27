from typing import TypedDict

from voting_systems.base import VotingResultException


class RankedChoiceResult(TypedDict):
    rounds: list[dict[str, int]]
    roundWinner: str


class Round(TypedDict):
    tally: dict[str, int]
    exhausted: 0


def get_result(
    choices: list[str], submissions: list[list[str] | None]
) -> RankedChoiceResult:
    if len(choices) < 2:
        raise VotingResultException("Must have atleast 2 choices")

    rounds: list[Round] = []
    eliminated = set()

    # Run until there is only one choice left.
    # Return tie if a winner has not been found yet.
    while len(choices) - len(eliminated) > 1:
        round = Round(
            tally={choice: 0 for choice in choices if choice not in eliminated},
            exhausted=0,
        )

        for submission in submissions:
            sub_set = [vote for vote in submission if vote not in eliminated]

            if len(sub_set):
                round["tally"][sub_set[0]] += 1
            else:
                round["exhausted"] += 1

        rounds.append(round)

        roundWinner = None

        # Find round winner
        sortedVotes = sorted(
            round["tally"].keys(), key=lambda x: round["tally"][x], reverse=True
        )

        roundWinner = sortedVotes[0]

        # Eliminate round loser
        losers = {choice for choice in sortedVotes if choice == sortedVotes[-1]}
        eliminated = eliminated.union(losers)

        # Check if we have an overall winner
        validVoteCount = len(submissions) - round["exhausted"]
        if round["tally"][roundWinner] / validVoteCount > 0.5:
            return RankedChoiceResult(rounds=rounds, roundWinner=roundWinner)

    return RankedChoiceResult(rounds=rounds, roundWinner="__TIE_FLAG__")
