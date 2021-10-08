from agent import Agent

class Spy(Agent):
    '''
    I am obviously a spy, I always do evil 😈
    '''
    def __init__(self, name="Spy"):
        self.name = name

    def new_game(self, number_of_players, player_number, spies):
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spies = spies
        self.rounds_completed = 0

    def propose_mission(self, team_size, fails_required = 1):
        return ([self.player_number] + [x for x in self.spies if x != self.player_number] + \
               [x for x in range(self.number_of_players) if x not in self.spies])[:team_size]

    def betrayals_required(self):
        return self.fails_required[self.number_of_players][self.rounds_completed]

    def number_of_spies(self, mission):
        return len([x for x in self.spies if x in mission])

    def enough_spies(self, mission):
        return self.number_of_spies(mission) >= self.betrayals_required()

    def vote(self, mission, proposer):
        if self.enough_spies(mission): return True
        else: return False

    def vote_outcome(self, mission, proposer, votes): pass

    def betray(self, mission, proposer): return True

    def mission_outcome(self, mission, proposer, num_fails, mission_success): pass

    def round_outcome(self, rounds_complete, missions_failed):
        self.rounds_completed = rounds_complete
    
    def game_outcome(self, spies_win, spies): pass