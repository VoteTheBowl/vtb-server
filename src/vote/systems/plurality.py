def results(choices: list[str], submissions: list[str]) -> dict[str, int]:
    results = {choice: 0 for choice in choices}

    for sub in submissions:
        if sub in choices:
            results[sub] = results[sub] + 1

    return results
