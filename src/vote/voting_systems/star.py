from typing import TypedDict

from vote.voting_systems.base import VotingResultException


class Rating(TypedDict):
    choice: str
    rating: int


def get_result(
    choices: list[str], submissions: list[dict[str, int] | None]
) -> list[Rating]:
    if len(choices) < 2:
        raise VotingResultException("Must have atleast 2 choices")

    ratings = {choice: 0 for choice in choices}
    totalFiveStars = {choice: 0 for choice in choices}

    for sub in submissions:
        if sub is None:
            break

        for choice, rating in sub.items():
            ratings[choice] += rating

            if rating == 5:
                totalFiveStars[choice] += 1

    ratingOrder = sorted(ratings.items(), key=lambda item: item[1])

    ties = [rating for rating in ratingOrder if ratingOrder[0][1] == rating[1]]

    if len(ties) == 1:
        results = [
            Rating(choice=choice, rating=rating) for choice, rating in ratingOrder
        ]
    elif len(ties) == 2:
        # Just one tie.
        pass
    else:
        # More ties
        pass

    return results
