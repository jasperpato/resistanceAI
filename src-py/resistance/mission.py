class Mission:
    '''
    Stores game history.
    A Mission is either: [team proposition + vote]             (aborted)
    or:                  [team proposition + vote + outcome]   (carried out)
    '''
    def __init__(self, num_players, rnd, proposer, team, votes_for):
        self.num_players = num_players
        self.rnd = rnd                  # 0 - 4
        self.proposer = proposer
        self.team = team
        self.votes_for = votes_for
        self.betrayals = None           # None if no mission carried out
        self.success = None             # None if no mission carried out, but False
                                        # if this is the fifth aborted mission
