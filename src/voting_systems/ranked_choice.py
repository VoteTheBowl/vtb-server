from typing import TypedDict


class RankedChoiceResult(TypedDict):
    rounds: list[dict[str,int]]
    roundWinner: str

def get_result(choices: list[str], submissions: list[list[str] | None]) -> RankedChoiceResult:
    rounds: list[dict[str, int]] = []

    while True:
        tallies: dict[str, int] = {choice: 0 for choice in choices}
        tallies["Exhausted"] = 0

        for submission in submissions:
            if len(submission):
                tallies[submission[0]] += 1
            else:
                tallies['Exhausted'] += 1

            rounds.append(tallies)

            roundWinner = choices[0]
            roundLosers = [choices[0]]

            for choice in choices:
                if tallies[choice] > tallies[roundWinner]:
                    roundWinner = choice

                if tallies[choice] < tallies[roundLosers[0]]:
                    roundLosers = [choice]

                if tallies[choice] == tallies[roundLosers[0]]:
                    roundLosers.append(choice)

            #Purge roundLosers from the submissions (and choice list)
            for submission in submissions:
                submission = [sub for sub in submissions if sub not in roundLosers] #Might need to be keys

            choices = [choice for choice in choices if choice not in roundLosers]

            #Check for a tie and/or an overall winner
            if len(choices) == 0:
                return RankedChoiceResult(rounds=rounds, roundWinner='__TIE_FLAG__')

            validVoteCount = len[submissions] - tallies['Exhausted']

            if tallies[roundWinner] / validVoteCount > 0.5:
                return RankedChoiceResult(rounds=rounds, roundWinner=roundWinner)
