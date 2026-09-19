def get_result(choices: list[str], submissions: list[list[str] | None]):
    active = [sub.copy() for sub in submissions if sub is not None]
    eliminated: list[str] = []

    while len(eliminated) < len(choices) - 2:
        tallies: dict[str, int] = {choice: 0 for choice in choices if not len(eliminated) or eliminated[-1] != choice}
        for sub in active:
            if len(eliminated):
                sub.remove(eliminated[-1])
            tallies[sub[0]] += 1

        winner = None

        #Sort tallies somehow.
        #Run Majority checks.
        #if winner break;
        #remove last tallied choice.
        #run again

        for choice in tallies:
            if tallies[choice] >= len(submissions) // 2:
                winner = choice
                #find 2nd, 3rd place choices
                break
            else:
                eliminated.append() #last tally



"""
let ballots = ballotData.map((b) => {
    const v = b.vote as RankedSubmission;
    return v ? [...v] : [];
});
let choices = [...choiceData];

while (true) {
    // Tally votes

    const tallies: Record<string, number> = Object.fromEntries(
        choices.map((choice) => [choice, 0])
    );
    tallies['Exhausted'] = 0;

    ballots.forEach((b) => {
        if (b.length > 0) {
            tallies[b[0]]++;
        } else {
            tallies['Exhausted']++;
        }
    });

    // Identify round winner and loser (first choices only)

    let roundWinner = choices[0];
    let roundLosers = [choices[0]];

    choices.forEach((choice) => {
        if (tallies[choice] > tallies[roundWinner]) {
            roundWinner = choice;
        }
        if (tallies[choice] < tallies[roundLosers[0]]) {
            roundLosers = [choice];
        }
        if (tallies[choice] === tallies[roundLosers[0]]) {
            roundLosers.push(choice);
        }
    });

    // Purge roundLosers from the ballots (and the choice list)

    ballots.forEach((b, i) => {
        ballots[i] = b.filter((i) => !roundLosers.includes(i));
    });
    choices = choices.filter((c) => !roundLosers.includes(c));

    // Check for a tie and/or an overall winner

    if (choices.length === 0) {
        return { overallWinner: '__TIE_FLAG__' };
    }

    // Winner only needs to take over 50% of non-exhausted votes
    const validVoteCount = ballots.length - tallies['Exhausted'];

    if (tallies[roundWinner] / validVoteCount > 0.5) {
        return { overallWinner: roundWinner };
    }
}
"""