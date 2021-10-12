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
        self.rnd = rnd            # 0 - 4
        self.proposer = proposer
        self.team = team
        self.votes_for = votes_for
        self.betrayals = None       # None if no mission carried out
        self.success = None         # None if no mission carried out, but False
                                    # if this is the fifth aborted mission

class Bayes2(Agent):    
    '''
    Maintains probabilities of all possible worlds.
    Calculates the probabilty of each player being a spy from set of worlds.
    World probabilities are updated on both vote patterns and mission outcomes.
    '''    

    def __init__(self, name='Bayes2'): self.name = name

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

    def average_suspicion(self):
        return self.spy_count[self.number_of_players] / self.number_of_players

    def betrayals_required(self):
        return self.fails_required[self.number_of_players][self.rnd]

    def new_game(self, number_of_players, player_number, spies):
        '''
        initialises the game, spies is empty if player is not a spy
        '''
        self.rnd = 0
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spies = spies
        self.missions = []
        self.failed_teams = [] # teams that betrayed - avoid them

        worlds = list(combinations(range(self.number_of_players), self.spy_count[number_of_players]))
        self.worlds = {w: 1/len(worlds) for w in worlds}
        self.update_suspicions()

        self.vote_threshold          = [1.00, 0.95, 0.90, 0.85, 0.80] # multiplied by average suspicion
        self.failable_vote_threshold = [1.00, 1.10, 1.20, 1.40, 2.00] # spy vote knowing enough spies on mission
        
        self.betray_rate       = [0.20, 0.40, 0.60, 0.80, 1.00] # chance of betraying per round
        self.risky_betray_rate = [0.15, 0.30, 0.45, 0.60, 1.00] # chance of betraying with more spies on mission

        # opponent modelling

        self.opponent_betray_rate = self.betray_rate
        
        self.spy_vote_failed     = [0.50, 0.60, 0.70, 0.80, 0.95] # chance of spy voting for a failed mission per round
        self.spy_vote_success    = [0.50, 0.40, 0.40, 0.30, 0.05] # chance of spy voting for a successful mission

        self.res_vote_failed     = [0.50, 0.50, 0.40, 0.30, 0.10]
        self.res_vote_success    = [0.50, 0.60, 0.70, 0.80, 0.95]

    def possible_teams(self, l):
        '''
        Returns list of all possible teams of length l including self,
        in ascending average suspicion
        '''
        teams = [t for t in list(combinations(range(self.number_of_players), l))
                 if self.player_number in t]
        return sorted(teams, key=lambda t: sum([self.suspicions[x] for x in t]))

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

    def mission_suspicion(self, mission):
        '''
        Returns the average suspicion of a mission. Does not include self
        '''
        others = [self.suspicions[x] for x in mission if x != self.player_number]
        return sum(others) / len(others)

    def vote(self, mission, proposer):
        if self.rnd == 0 or proposer == self.player_number or self.missions_downvoted() == 4:
            return True
        if self.is_spy():
            if self.missions_succeeded() == 2:
                return True if self.enough_spies(mission) else False
            if self.enough_spies(mission) and not self.bad_mission(mission):
                return self.mission_suspicion(mission) <= \
                    self.failable_vote_threshold[self.rnd] * self.average_suspicion()
        if self.bad_mission(mission): return False
        return self.mission_suspicion(mission) <= \
            self.vote_threshold[self.rnd] * self.average_suspicion()

    def vote_outcome(self, mission, proposer, votes):
        '''
        Add a new Mission object to our stored info
        '''
        self.missions.append(Mission(self.number_of_players, self.rnd, proposer, mission, votes))

    def betray(self, mission, proposer):
        if self.is_spy():
            if self.missions_failed() == 2 and self.enough_spies(mission): return True
            if self.missions_succeeded() == 2: return True
            elif self.number_of_spies(mission) > self.betrayals_required():
                return random() < self.risky_betray_rate[self.rnd]
            elif self.number_of_spies(mission) < self.betrayals_required(): return False
            else: return random() < self.betray_rate[self.rnd]
        return False # is resistance

    def update_suspicions(self):
            '''
            Updates self.suspicions to reflect the probability of each player being
            a spy
            '''
            suspicions = {x: 0 for x in range(self.number_of_players)}
            worlds = self.worlds.items()
            for x in range(self.number_of_players):
                for w, wp in worlds:
                    if x in w: suspicions[x] += wp
            self.suspicions = suspicions

    def outcome_probability(self, spies_in_mission, betrayals, betray_rate):
        '''
        Determines the probability of a mission outcome given a world
        Assume spy always betrays with probability betray_rate
        '''
        if spies_in_mission < betrayals: return 0
        p = 1
        for i in range(betrayals): p *= betray_rate
        for i in range(spies_in_mission - betrayals): p *= 1 - betray_rate
        if spies_in_mission > 0: p *= comb(spies_in_mission, betrayals)
        return p

    def vote_probability(self, world, votes_for, sf, ss, rf, rs, mission_success):
        '''
        Determines the probability of voting pattern given a world and a mission outcome
        '''
        p = 1
        for x in range(self.number_of_players):
            if x in world and x in votes_for:
                if mission_success: p *= ss
                else: p *= sf
            elif x in world and x not in votes_for:
                if mission_success: p *= (1-ss)
                else: p *= (1-sf)
            elif x not in world and x in votes_for:
                if mission_success: p *= rs
                else: p *= rf
            elif x not in world and x not in votes_for:
                if mission_success: p *= (1-rs)
                else: p *= (1-rf)
        return p

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        Update the last Mission object with mission info
        Update world probabilities
        '''
        self.missions[-1].betrayals = betrayals
        self.missions[-1].success = mission_success
        if not mission_success: self.failed_teams.append(mission)

        if len(self.worlds) > 1 and self.rnd < 4:

            outcome_prob = 0 # overall probability of this mission outcome
            voting_prob = 0  # overall probability of a voting pattern given a mission outcome

            br = self.opponent_betray_rate[self.rnd]

            sf = self.spy_vote_failed[self.rnd]
            ss = self.spy_vote_success[self.rnd]
            rf = self.res_vote_failed[self.rnd]
            rs = self.res_vote_success[self.rnd]

            for w, wp in self.worlds.items():
                spies_in_mission = len([x for x in w if x in mission])
                outcome_prob += self.outcome_probability(spies_in_mission, betrayals, br) * wp
                voting_prob += self.vote_probability(w, self.missions[-1].votes_for, \
                    sf, ss, rf, rs, mission_success) * wp

            impossible_worlds = []
            for w, wp in self.worlds.items():
                
                # mission outcome
                spies_in_mission = len([x for x in w if x in mission])
                if spies_in_mission == betrayals and len(mission) == betrayals:
                    self.worlds = {w:1}
                    break   
                self.worlds[w] *= self.outcome_probability(spies_in_mission, betrayals, br)
                self.worlds[w] /= outcome_prob
                
                # voting patterns
                self.worlds[w] *= self.vote_probability(w, self.missions[-1].votes_for, \
                    sf, ss, rf, rs, mission_success)
                self.worlds[w] /= voting_prob

                if self.worlds[w] == 0: impossible_worlds.append(w)

            for w in impossible_worlds: self.worlds.pop(w, None)
            self.update_suspicions()

    def round_outcome(self, rounds_complete, missions_failed):
        self.rnd += 1
        self.missions[-1].success = (missions_failed == self.missions_failed())
    
    def game_outcome(self, spies_win, spies): pass


