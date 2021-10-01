from agent import Agent
from random import randrange, random

class Mission:
    '''
    A Mission can be either: [team proposition + vote]             (aborted)
                         or: [team proposition + vote + outcome]   (carried out)
    '''
    def __init__(self, round, proposer, team, votes):
        self.round = round
        self.proposer = proposer
        self.team = team # list of players proposed
        self.votes = votes # dictionary mapping players to boolean vote
        self.betrayals = None # number of betrayals or None if no mission carried out
        self.success = None # True iff mission succeeded, None if no mission carried out

    def carried_out(self):
        return self.success is not None

class FirstAgent(Agent):        

    def __init__(self, name='Japer'):
        self.name = name
        self.number_of_players = 0
        self.players = []
        self.player_number = 0
        self.spy_list = []
        self.suspicions = {} # for each player, probability of being a spy
        self.missions = [] # stores all game history

    def is_spy(self):
        return self.spy_list != []

    def missions_failed(self):
        f = 0
        for m in self.missions:
            if m.carried_out() and not m.success:
                f += 1
        return f

    def missions_succeeded(self):
        s = 0
        for m in self.missions:
            if m.carried_out() and m.success:
                s += 1
        return s

    def rounds_completed(self):
        r = 0
        for m in self.missions:
            if m.carried_out():
                r += 1
        return r

    def round(self):
        return self.rounds_completed()+1

    def fails_required(self):
        return self.fails_required[self.number_of_players][self.round()]

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, spy_list is empty if player is not a spy
        '''
        self.number_of_players = number_of_players
        self.players = [p for p in range(number_of_players)]
        self.player_number = player_number
        self.spy_list = spy_list
        for p in self.players:
            self.suspicions[p] = self.spy_count[number_of_players] / number_of_players
        self.missions = []

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
        return [i[0] for i in self.least_suspicious(self.number_of_players)
        if i in self.spy_list][:n]

    def most_suspicious_resistance(self, n):
        '''
        Spy method
        returns the n most suspicious resistance members
        '''
        return [i[0] for i in self.least_suspicious(self.number_of_players).reverse()
        if i not in self.spy_list][:n]

    def propose_mission(self, team_size, betrayals_required = 1):
        if not self.is_spy(): # team is self + least suspicious players
            return [self.player_number] + self.least_suspicious(team_size-1)
        elif betrayals_required == 1: # team is self + most suspicious resistance
            return [self.player_number] + self.most_suspicious_resistance(team_size-1)    
        elif betrayals_required == 2: # team is self + least suspicious spy + most suspicious resistance
            return [self.player_number, self.least_suspicious_spies(1)] + \
                    self.most_suspicious_resistance(team_size-2)

    def vote(self, mission, proposer):
        if(self.round() == 1 or proposer == self.player_number):
            return True
        return random() < 0.5  

    def vote_outcome(self, mission, proposer, votes):
        '''
        add a new Mission object to our stored info
        '''
        self.missions.append(Mission(self.round(), proposer, mission, votes))

    def betray(self, mission, proposer):
        if self.is_spy():
            number_of_spies_on_mission = len([i for i in self.spy_list if i in mission])
            if (self.missions_succeeded() == 2):
                return True # must betray to avoid losing
            elif number_of_spies_on_mission != self.fails_required():
                return False # either too many or not enough spies on the mission to sabotage
            else:
                return random() < 0.2 * self.round() # betray more later in game
        return False # is resistance

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        update the last Mission object with mission info
        '''
        self.missions[-1].betrayals = betrayals
        self.missions[-1].success = mission_success

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



