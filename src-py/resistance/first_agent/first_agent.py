from agent import Agent
from random import randrange, random

class Turn:
    '''
    A turn can be either: [team proposition + vote]             (not majority)
                      or: [team proposition + vote + outcome]   (majority)
    '''
    def __init__(self, proposer, team, votes):
        self.proposer = proposer
        self.team = team # list of players proposed
        self.votes = votes # dictionary mapping players to boolean vote
        self.betrayals = None # number of betrayals or None if no mission carried out
        self.success = None # True iff mission succeeded, None if no mission carried out

    def is_majority(self):
        y = 0
        for v in self.votes:
            if v:
                y += 1
        return True if y > len(self.votes) // 2 else False

    def is_completed(self):
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
            if t.is_completed() and not t.success:
                f += 1
        return f

    def missions_succeeded(self):
        s = 0
        for t in self.turns:
            if t.is_completed() and t.success:
                s += 1
        return s

    def rounds_completed(self):
        r = 0
        for t in self.turns:
            if t.is_completed():
                r += 1
        return r

    def round(self):
        return self.rounds_completed()-1

    def fails_required(self):
        return self.fails_required[self.number_of_players][self.rounds_completed()+1]

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, spy_list is empty if player is not a spy
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
        Resistance method
        returns the n least suspicious players, not including self
        '''
        d = self.suspicions.copy()
        d.pop(self.player_number)
        s = sorted(d.items(), key=lambda x: x[1])
        return [i[0] for i in s][:n]

    def least_suspicious_spies(self, n):
        '''
        Spy method
        returns the n least suspicious spies, not including self
        '''
        return [i[0] for i in self.least_suspicious(self.number_of_players) if i in self.spy_list][:n]

    def propose_mission(self, team_size, betrayals_required = 1):
        if not self.is_spy: # team is self + least suspicious players
            return [self.player_number] + self.least_suspicious(team_size-1)
        elif betrayals_required == 1: # team is self + random, non-spies
            team = [self.player_number]
            while len(team) < team_size:
                n = randrange(self.players)
                if self.players[n] not in self.spy_list and self.players[n] not in team:
                    team.append(self.players[n])
            return team
        elif betrayals_required == 2: # team is self + most suspicious spy + random, non-spies
            team = [self.player_number, max(self.spy_list, key=lambda x: self.suspicions[x])]
            while len(team) < team_size:
                n = randrange(self.players)
                if self.players[n] not in self.spy_list and self.players[n] not in team:
                    team.append(self.players[n])
            return team
        else: # team is self + random players
            team = [self.player_number]
            while len(team) < team_size:
                n = randrange(len(self.players))
                if self.players[n] not in team:
                    team.append(self.players[n])
            return team

    def vote(self, mission, proposer):
        if(self.rounds_completed() == 0):
            return True # always vote yes on first round
        return random() < 0.75   

    def vote_outcome(self, mission, proposer, votes):
        '''
        add a new Turn object to our stored info
        '''
        self.turns.append(Turn(proposer, mission, votes))

    def betray(self, mission, proposer):
        if self.is_spy():
            number_of_spies_on_mission = len([i for i in self.spy_list if i in mission])
            if (self.missions_succeeded() == 2):
                return True # must betray to avoid losing
            elif number_of_spies_on_mission != self.fails_required():
                return False # either too many or not enough spies on the mission to sabotage
            else:
                return random() < 0.3 # betray 30% of the time
        return False # is resistance

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        update the last Turn object with mission info
        '''
        self.turns[-1].betrayals = betrayals
        self.turns[-1].success = mission_success

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        unnecessary - can infer this information
        '''
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        unnecessary - do not store info between games (yet...)
        '''
        pass



