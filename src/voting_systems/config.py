from collections.abc import Callable
from typing import TypedDict

from voting_systems import plurality, ranked_choice, star


class VotingSystemConfig(TypedDict):
    result: Callable
    resultType: type
    submissionType: type


config: dict[str, VotingSystemConfig] = {
    "ST": {
        "result": star.get_result,
        "resultType": star.StarResult,
        "submissionType": star.StarSubmission,
    },
    "PL": {
        "result": plurality.get_result,
        "resultType": plurality.PluralityResult,
        "submissionType": plurality.PluralitySubmission,
    },
    "RC": {
        "result": ranked_choice.get_result,
        "resultType": ranked_choice.RankedChoiceResult,
        "submissionType": ranked_choice.RankedChoiceSubmission,
    },
}
