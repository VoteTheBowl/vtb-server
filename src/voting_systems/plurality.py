from .base import VotingResultException


def get_result(choices: list[str], submissions: list[str | None]) -> dict[str, int]:
    if len(choices) < 2:
        raise VotingResultException("Must have atleast 2 choices")

    results = {choice: 0 for choice in choices}

    for sub in submissions:
        if sub in choices:
            results[sub] = results[sub] + 1

    return results
