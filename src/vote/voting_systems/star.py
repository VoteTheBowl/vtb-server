def get_result(
    choices: list[str], submissions: list[dict[str, int] | None]
) -> list[dict[str, int]]:
    ratings = {choice: 0 for choice in choices}

    for sub in submissions:
        if sub is None:
            break

        for choice, rating in sub.items():
            ratings[choice] += rating

    return [{"test": 2}]
