from agent import Agent
from random import randrange, random

class Turn:
    '''
    A turn can be either: [team proposition + vote]             (not majority)
                      or: [team proposition + vote + outcome]   (majority)
    '''
    def __init__(self, proposer, team, votes):
        '''
        leader: leader of round
        team: proposed team
        votes: list of booleans, eg. votes[player_number] = True
        outcome: true if mission succeeded
        '''
        self.proposer = proposer
        self.team = team
        self.votes = votes
        self.betrayals = None
        self.success = None

    def majority(self):
        y = 0
        for v in self.votes:
            if v:
                y += 1
        return True if y > len(self.votes) // 2 else False

    def completed(self):
        return self.success is not None

class FirstAgent(Agent):        

    def __init__(self, name='Japer'):
        self.name = name
        self.number_of_players = 0
        self.players = []
        self.player_number = 0
        self.spy_list = []
        self.suspicions = {} # for each player, probability of being a spy
        self.is_spy = False
        self.turns = [] # stores all turn information

    def missions_failed(self):
        f = 0
        for t in self.turns:
            if t.completed() and not t.success:
                f += 1
        return f

    def missions_succeeded(self):
        s = 0
        for t in self.turns:
            if t.completed() and t.success:
                s += 1
        return s

    def rounds_completed(self):
        r = 0
        for t in self.turns:
            if t.completed():
                r += 1
        return r

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the 
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy,
        or empty otherwise
        '''
        self.number_of_players = number_of_players
        self.players = [p for p in range(number_of_players)]
        self.player_number = player_number
        self.spy_list = spy_list
        self.is_spy = True if spy_list != [] else False
        for p in self.players:
            self.suspicions[p] = self.spy_count[number_of_players] / number_of_players
        self.turns = []

    def least_suspicious(self, n):
        '''
        returns the n least suspicious players, not including self
        '''
        d = self.suspicions.copy()
        d.pop(self.player_number)
        s = sorted(d.items(), key=lambda x: x[1])
        return [i[0] for i in s][:n]

    def propose_mission(self, team_size, betrayals_required = 1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive)
        and number_of_players (exclusive) to be returned. 
        betrayals_required are the number of betrayals required for the mission
        to fail.
        '''
        if not self.is_spy: # team is self + least suspicious players
            return [self.player_number] + self.least_suspicious(team_size-1)
        else: # team is self + random, non-spy players
            res_list = [p for p in self.players if p not in self.spy_list]
            team = [self.player_number]
            while len(team) < team_size:
                n = randrange(len(res_list))
                if res_list(n) not in team:
                    team.append(res_list[n])
            return team

    def vote(self, mission, proposer):
        if(self.rounds_completed() == 0):
            return True # always vote yes on first round
        return random() < 0.75   

    def vote_outcome(self, mission, proposer, votes):
        self.turns.append(Turn(proposer, mission, votes))

    def betray(self, mission, proposer):
        if self.is_spy():
            spies_on_mission = len([i for i in self.spy_list if i in mission])
            fails_required = self.fails_required[self.number_of_players][self.rounds_completed()+1]
            if (self.rounds_completed() == 4):
                return True # must betray on the final, game-deciding vote
            elif spies_on_mission != fails_required:
                return False # either too many or not enough spies on the mission to sabotage
            else:
                return random() < 0.3 # betray 30% of the time
        return False # is resistance member

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        self.turns[-1].betrayals = betrayals
        self.turns[-1].success = mission_success

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        unnecessary - can infer this information
        '''
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        unnecessary - do not store info between games (yet)
        '''
        pass



