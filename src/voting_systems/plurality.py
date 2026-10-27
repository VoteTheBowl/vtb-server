from .base import VotingResultException

type PluralitySubmission = str
type PluralityResult = dict[str, int]


def get_result(
    choices: list[PluralitySubmission], submissions: list[PluralitySubmission]
) -> PluralityResult:
    if len(choices) < 2:
        raise VotingResultException("Must have atleast 2 choices")

    results = {choice: 0 for choice in choices}

    for sub in submissions:
        if sub in choices:
            results[sub] = results[sub] + 1

    return results
