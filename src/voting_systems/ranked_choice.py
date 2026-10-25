def get_result(choices: list[str], submissions: list[list[str] | None]):
    rounds: list[dict[str, int]] = []

    while True:
        tallies: dict[str, int] = {choice: 0 for choice in choices}
        tallies["Exhausted"] = 0

        """
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
        
                    rounds.push(tallies);
        
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
                        return { roundData: rounds, overallWinner: '__TIE_FLAG__' };
                    }
        
                    // Winner only needs to take over 50% of non-exhausted votes
                    const validVoteCount = ballots.length - tallies['Exhausted'];
        
                    if (tallies[roundWinner] / validVoteCount > 0.5) {
                        return { roundData: rounds, overallWinner: roundWinner };
                    }
                    """
