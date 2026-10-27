from voting_systems import plurality, ranked_choice, star

type AllResultTypes = (
    plurality.PluralityResult
    | star.StarResult
    | ranked_choice.RankedChoiceResult
    | None
)
