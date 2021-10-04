from agent import Agent
from random import random, seed
from time import time

class Mission:
    '''
    Stores game history.
    A Mission is either: [team proposition + vote]             (aborted)
                     or: [team proposition + vote + outcome]   (carried out)
    '''
    def __init__(self, number_of_players, rnd, proposer, team, votes_for):
        self.number_of_players = number_of_players
        self.round = rnd            # 1 - 5
        self.proposer = proposer
        self.team = team            # list of players proposed
        self.votes_for = votes_for  # dictionary mapping players to boolean vote
        self.betrayals = None       # number of betrayals or None if no mission carried out
        self.success = None         # True iff mission succeeded, None if no mission carried out
        # change this to handle 5 failed votes

    def carried_out(self): 
        return self.success is not None

    def votes_against(self):
        return [i for i in range(self.number_of_players) if i not in self.votes_for]

class BaselineAgent(Agent):        

    def __init__(self, name='Japer'):
        self.name = name
        seed(time())

    def is_spy(self):
        return self.spy_list != []

    def missions_failed(self):
        f = 0
        for m in self.missions:
            if m.carried_out() and not m.success: f += 1
        return f

    def missions_succeeded(self):
        s = 0
        for m in self.missions:
            if m.carried_out() and m.success: s += 1
        return s

    def missions_downvoted(self):
        d = 0
        for m in reversed(self.missions):
            if not m.carried_out(): d += 1
            else: break
        return d

    def rounds_completed(self):
        r = 0
        for m in self.missions:
            if m.carried_out(): r += 1
        return r

    def rnd(self):
        return self.rounds_completed() + 1

    def average_suspicion(self):
        return self.spy_count[self.number_of_players] / self.number_of_players

    def betrayals_required(self):
        return self.fails_required[self.number_of_players][self.rounds_completed()]

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, spy_list is empty if player is not a spy
        '''
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spy_list = spy_list
        self.suspicions =  {i:self.average_suspicion() for i in range(self.number_of_players)}
        self.missions = []

        # Resistance votes for a mission if average mission suspicion is less than this
        self.vote_threshold = 1.1 * self.average_suspicion()
        # this * round number is the chance a spy votes for a fail-able mission 
        self.vote_spy_rate = 0.2
        # this * round number is the chance a spy betrays the mission
        self.betray_rate = 0.2

    def least_suspicious(self, n):
        '''
        Resistance method
        returns the n least suspicious players, not including self
        '''
        d = self.suspicions.copy()
        d.pop(self.player_number)
        return [i[0] for i in sorted(d.items(), key=lambda x: x[1])][:n]

    def least_suspicious_spies(self, n):
        '''
        Spy method
        returns the n least suspicious spies, not including self
        '''
        return [i for i in self.least_suspicious(self.number_of_players)
                if i in self.spy_list][:n]

    def most_suspicious_resistance(self, n):
        '''
        Spy method
        returns the n most suspicious resistance members
        '''
        return [i for i in reversed(self.least_suspicious(self.number_of_players))
                if i not in self.spy_list][:n]

    def number_of_spies(self, mission):
        '''
        Spy method
        returns number of spies on mission
        '''
        return len([i for i in self.spy_list if i in mission])

    def enough_spies(self, mission):
        '''
        Spy method
        returns True iff there are enough spies in mission to fail the mission
        '''
        return self.number_of_spies(mission) >= self.betrayals_required()

    def mission_suspicion(self, mission):
        '''
        returns average suspicion of players in a mission
        '''
        return sum([s[1] for s in self.suspicions.items() if s[0] in mission]) / len(mission)

    def propose_mission(self, team_size, betrayals_required = 1):
        if not self.is_spy():
            return [self.player_number] + self.least_suspicious(team_size-1)
        elif betrayals_required == 1:
            return [self.player_number] + self.most_suspicious_resistance(team_size-1)  
        elif betrayals_required == 2:
            return [self.player_number, self.least_suspicious_spies(1)] + \
                    self.most_suspicious_resistance(team_size-2)

    def vote(self, mission, proposer):
        if self.rnd() == 1 or proposer == self.player_number \
        or self.missions_downvoted == 4:
            return True
        if self.is_spy():
            if self.missions_succeeded() == 2:
                return True if self.enough_spies(mission) else False
            if self.enough_spies(mission):
                return random() < self.vote_spy_rate * self.rnd()
        return self.mission_suspicion(mission) < self.vote_threshold

    def vote_outcome(self, mission, proposer, votes):
        '''
        Add a new Mission object to our stored info
        '''
        self.missions.append(Mission(self.number_of_players, self.rnd(), proposer, mission, votes))

    def betray(self, mission, proposer):
        if self.is_spy():
            if (self.missions_succeeded() == 2): return True
            elif self.number_of_spies(mission)) != self.betrayals_required(): return False
            else: return random() < self.betray_rate * self.rnd()
        return False # is resistance

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        Update the last Mission object with mission info
        '''
        self.missions[-1].betrayals = betrayals
        self.missions[-1].success = mission_success

        # update suspicions
        # assume there was only one spy in a 1-betrayed mission

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        Unnecessary - can infer this information
        '''
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        Unnecessary - do not store info between games (yet...)
        '''
        pass



