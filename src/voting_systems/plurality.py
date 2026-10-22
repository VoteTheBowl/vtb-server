from .base import VotingResultException

type PluralityResult = dict[str, int]


def get_result(choices: list[str], submissions: list[str | None]) -> PluralityResult:
    if len(choices) < 2:
        raise VotingResultException("Must have atleast 2 choices")

    results = {choice: 0 for choice in choices}

    for sub in submissions:
        if sub in choices:
            results[sub] = results[sub] + 1

    return results
