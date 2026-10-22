from typing import TypedDict

from .base import VotingResultException


class Score(TypedDict):
    choice: str
    score: int


class StarResult(TypedDict):
    scores: list[Score]
    gold: list[str]
    silver: list[str]
    bronze: list[str]


type SanitizedSubmissions = list[dict[str, int]]


def get_choice_with_most_stars(choice_a: str, choice_b: str, totals: dict[str, int]):
    if totals[choice_a] > totals[choice_b]:
        return choice_a
    elif totals[choice_a] < totals[choice_b]:
        return choice_b
    else:
        return None


def get_choice_with_most_five_stars(
    choice_a: str, choice_b: str, totalFiveStarCount: dict[str, int]
) -> str | None:
    if totalFiveStarCount[choice_a] > totalFiveStarCount[choice_b]:
        return choice_a
    elif totalFiveStarCount[choice_a] < totalFiveStarCount[choice_b]:
        return choice_b
    else:
        return None


def get_runoff_winner(
    choice_a: str, choice_b: str, sanitizedSubmissions: SanitizedSubmissions
) -> str | None:
    choice_a_total = 0
    choice_b_total = 0

    for submission in sanitizedSubmissions:
        if submission[choice_a] > submission[choice_b]:
            choice_a_total += 1
        elif submission[choice_a] < submission[choice_b]:
            choice_b_total += 1

    if choice_a_total > choice_b_total:
        return choice_a
    elif choice_a_total < choice_b_total:
        return choice_b
    else:
        return None


def get_winner(
    orderedScores: list[Score],
    scores: dict[str, int],
    totalFiveStars: dict[str, int],
    sanitizedSubmissions: SanitizedSubmissions,
) -> list[str]:
    leading_ties = [
        score["choice"]
        for score in orderedScores
        if orderedScores[0]["score"] == score["score"]
    ]

    if len(orderedScores) == 0:
        return []

    if len(leading_ties) == 1 or len(leading_ties) > 2:
        gold = leading_ties
    else:
        winner = get_runoff_winner(
            leading_ties[0], leading_ties[1], sanitizedSubmissions
        )

        if winner is None:
            winner = get_choice_with_most_stars(
                leading_ties[0], leading_ties[1], scores
            )

        if winner is None:
            winner = get_choice_with_most_five_stars(
                leading_ties[0], leading_ties[1], totalFiveStars
            )

        if winner is None:
            gold = leading_ties
        else:
            gold = [winner]

    return gold


def get_result(
    choices: list[str], submissions: list[dict[str, int] | None]
) -> StarResult:
    if len(choices) < 2:
        raise VotingResultException("Must have atleast 2 choices")

    scores = {choice: 0 for choice in choices}
    totalFiveStars = {choice: 0 for choice in choices}

    sanitizedSubmissions: SanitizedSubmissions = []

    gold = []
    silver = []
    bronze = []

    for sub in submissions:
        if sub is None:
            break

        sanitizedSubmissions.append(sub)

        for choice, rating in sub.items():
            scores[choice] += rating

            if rating == 5:
                totalFiveStars[choice] += 1

    orderedScores = [
        Score(choice=score[0], score=score[1])
        for score in sorted(scores.items(), key=lambda item: item[1], reverse=True)
    ]

    gold = get_winner(orderedScores, scores, totalFiveStars, sanitizedSubmissions)

    silver = get_winner(
        [score for score in orderedScores if score["choice"] not in gold],
        scores,
        totalFiveStars,
        sanitizedSubmissions,
    )

    bronze = get_winner(
        [score for score in orderedScores if score["choice"] not in gold + silver],
        scores,
        totalFiveStars,
        sanitizedSubmissions,
    )

    return StarResult(scores=orderedScores, gold=gold, silver=silver, bronze=bronze)
