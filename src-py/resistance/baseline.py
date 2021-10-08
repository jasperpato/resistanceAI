from agent import Agent
from random import random, seed
from time import time
from itertools import combinations
from math import comb

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
        self.team = team
        self.votes_for = votes_for
        self.betrayals = None       # None if no mission carried out
        self.success = None         # None if no mission carried out, but False
                                    # if this is the fifth aborted mission

class Baseline(Agent):    
    '''
    Maintains probabilities of all possible worlds.
    Calculates the probabilty of each player being a spy from set of worlds.
    '''    

    def __init__(self, name='Baseline'):
        self.name = name
        self.class_str = "Baseline"

    def is_spy(self): return self.spies != []

    def missions_failed(self):
        f = 0
        for m in self.missions:
            if m.success == False: f += 1
        return f

    def missions_succeeded(self):
        s = 0
        for m in self.missions:
            if m.success: s += 1
        return s

    def missions_downvoted(self):
        d = 0
        for m in reversed(self.missions):
            if m.success is None: d += 1
            else: break
        return d

    def rounds_completed(self):
        r = 0
        for m in self.missions:
            if m.success is not None: r += 1
        return r

    def rnd(self): return self.rounds_completed() + 1

    def betrayals_required(self):
        return self.fails_required[self.number_of_players][self.rounds_completed()]

    def new_game(self, number_of_players, player_number, spies):
        '''
        initialises the game, spies is empty if player is not a spy
        '''
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spies = spies
        self.missions = []
        self.failed_teams = [] # teams that betrayed - avoid them

        self.vote_threshold = 1.0
        self.vote_failable_rate = 0.2
        self.vote_unknown_mission_rate = 0.6
        self.betray_rate = 0.2
        self.risky_betray_rate = 0.2 # if there are more spies on mission than necessary

    def possible_teams(self, l):
        '''
        Returns list of all possible teams of length l including self,
        in ascending average suspicion
        '''
        teams = [t for t in list(combinations(range(self.number_of_players), l))
                 if self.player_number in t]
        return teams

    def number_of_spies(self, mission):
        '''
        Spy method
        returns number of spies on mission
        '''
        return len([x for x in self.spies if x in mission])

    def enough_spies(self, mission):
        '''
        Spy method
        returns True iff there are enough spies in mission to fail the mission
        '''
        return self.number_of_spies(mission) >= self.betrayals_required()

    def bad_mission(self, mission):
        '''
        Returns True iff this mission configuration has already ended in
        betrayal
        '''
        for m in self.failed_teams:
            if mission == m or set(mission).issubset(m): return True
        return False

    def propose_mission(self, team_size, betrayals_required = 1):
        '''
        Propose the least suspicious team including self.
        If spy and two betrayals required, try to return the least suspicious
        team containing two spies.
        '''
        ps = self.possible_teams(team_size)
        if not self.is_spy() or betrayals_required == 1:
            team = ps[0]
            for n in range(1, len(ps)):
                if self.bad_mission(team): team = ps[n]
                else: return team
        elif betrayals_required == 2:
            team = ps[0]
            for n in range(1, len(ps)):
                if self.bad_mission(team) or not self.enough_spies(team): team = ps[n]
                else: return team
            if self.missions_succeeded() < 2:
                team = ps[0]
                for n in range(1, len(ps)):
                    if self.bad_mission(team): team = ps[n]
                    else: return team
            else:
                team = ps[0]
                for n in range(1, len(ps)):
                    if not self.enough_spies(team): team = ps[n]
                    else: return team

    def vote(self, mission, proposer):
        if self.rnd() == 1 or proposer == self.player_number or self.missions_downvoted() == 4:
            return True
        if self.is_spy():
            if self.missions_succeeded() == 2:
                return True if self.enough_spies(mission) else False
            if self.enough_spies(mission) and not self.bad_mission(mission):
                return random() < self.vote_failable_rate * self.rnd()
        if self.bad_mission(mission): return False
        return random() < self.vote_unknown_mission_rate

    def vote_outcome(self, mission, proposer, votes):
        '''
        Add a new Mission object to our stored info
        '''
        self.missions.append(Mission(self.number_of_players, self.rnd(), proposer, mission, votes))

    def betray(self, mission, proposer):
        if self.is_spy():
            if self.missions_failed() == 2 and self.enough_spies(mission): return True
            if self.missions_succeeded() == 2: return True
            elif self.number_of_spies(mission) > self.betrayals_required():
                return random() < self.risky_betray_rate * self.rnd()
            elif self.number_of_spies(mission) < self.betrayals_required(): return False
            else: return random() < self.betray_rate * self.rnd()
        return False # is resistance

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        Update the last Mission object with mission info
        Assumes opponent spies betray with probability of
        self.betray_rate * self.rounds_completed()
        '''
        self.missions[-1].betrayals = betrayals
        self.missions[-1].success = mission_success
        if not mission_success: self.failed_teams.append(mission)

    def round_outcome(self, rounds_complete, missions_failed):
        self.missions[-1].success = (missions_failed == self.missions_failed())
    
    def game_outcome(self, spies_win, spies): pass


