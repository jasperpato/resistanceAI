from agent import Agent
from random import random, sample
from itertools import combinations
from math import comb
# from mission import Mission

class Bayes3(Agent):    
    '''
    Maintains probabilities of all possible worlds.
    Calculates the probabilty of each player being a spy from set of worlds.
    Probabilities are based on mission outcome, voting pattern and proposer.

    Behavioural data is hard coded based off my best estimates having played the
    game extensively with humans.
    '''    

    def __init__(self, name='Bayes3'):
        self.name = name

        # outcome weight is 1.0
        self.voting_weight   = 0.4
        self.proposer_weight = 0.3

        # hard coding behaviour per round

        self.vote_threshold          = [1.05, 1.05, 1.00, 0.95, 0.80] # multiplied by average suspicion
        self.failable_vote_threshold = [1.10, 1.10, 1.20, 1.40, 2.00] # multiplied by average suspicion
                                                                      # spy vote knowing enough spies on mission
        
        self.betray_rate       = [0.20, 0.40, 0.60, 0.80, 1.00] # chance of betraying
        self.risky_betray_rate = [0.15, 0.30, 0.45, 0.60, 1.00] # chance of betraying with more spies on mission

        # hardcoded opponent modelling per round

        self.opponent_betray_rate = self.betray_rate
              
        self.spy_vote_failed     = [0.50, 0.55, 0.60, 0.80, 0.95] # chance of spy voting for a failed mission
        self.spy_vote_success    = [0.50, 0.45, 0.40, 0.20, 0.05] # chance of spy voting for a successful mission

        self.spy_propose_failed  = [0.50, 0.55, 0.60, 0.80, 0.95] # chance of spy proposing a failed mission
        self.spy_propose_success = [0.50, 0.45, 0.40, 0.20, 0.05] # chance of spy proposing a successful mission 

        self.res_vote_failed     = [0.50, 0.45, 0.40, 0.20, 0.05]
        self.res_vote_success    = [0.50, 0.55, 0.60, 0.80, 0.95]
        
        self.res_propose_failed  = [0.50, 0.45, 0.45, 0.40, 0.30]
        self.res_propose_success = [0.50, 0.55, 0.55, 0.60, 0.70]

    def is_spy(self): return self.spies != []

    def average_suspicion(self):
        return self.spy_count[self.num_players] / self.num_players

    def betrayals_required(self):
        return self.fails_required[self.num_players][self.rnd]

    def new_game(self, num_players, player_number, spies):
        '''
        initialises the game, spies is empty if player is not a spy
        '''
        self.rnd       = 0
        self.successes = 0
        self.fails     = 0
        self.downvotes = 0

        self.num_players = num_players
        self.player_number = player_number
        self.num_spies = self.spy_count[self.num_players]
        self.spies = spies
        self.failed_teams = [] # teams that betrayed - avoid them
        self.votes_for = [] # players that voted for last proposed mission
        # self.missions = []

        worlds = list(combinations(range(self.num_players), self.num_spies))
        self.worlds = {w: 1/len(worlds) for w in worlds}
        self.update_suspicions()

    def possible_teams(self, l):
        '''
        Returns list of all possible teams of length l including self,
        in ascending average suspicion
        '''
        teams = [t for t in list(combinations(range(self.num_players), l))
                 if self.player_number in t]
        return sorted(teams, key=lambda t: sum([self.suspicions[x] for x in t]))

    def num_spies_in(self, mission):
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
        return self.num_spies_in(mission) >= self.betrayals_required()

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
            if self.successes < 2:
                team = ps[0]
                for n in range(1, len(ps)):
                    if self.bad_mission(team): team = ps[n]
                    else: return team
            else:
                team = ps[0]
                for n in range(1, len(ps)):
                    if not self.enough_spies(team): team = ps[n]
                    else: return team
        return [self.player_number] + sample([x for x in range(self.num_players) if x != self.player_number], team_size-1)

    def mission_suspicion(self, mission):
        '''
        Returns the average suspicion of a mission. Does not include self
        '''
        others = [self.suspicions[x] for x in mission if x != self.player_number]
        return sum(others) / len(others)

    def vote(self, mission, proposer):
        if self.rnd == 0 or proposer == self.player_number or self.downvotes == 4:
            return True
        res_vote = self.mission_suspicion(mission) <= \
            self.vote_threshold[self.rnd] * self.average_suspicion()
        if self.is_spy():
            if self.successes == 2:
                return True if self.enough_spies(mission) else False
            if self.enough_spies(mission) and not self.bad_mission(mission):
                return res_vote or self.mission_suspicion(mission) <= \
                    self.failable_vote_threshold[self.rnd] * self.average_suspicion()
        if self.bad_mission(mission): return False
        if self.player_number not in mission and \
            len(mission) >= self.num_players - self.num_spies: return False
        return res_vote

    def vote_outcome(self, mission, proposer, votes_for):
        # self.missions.append(Mission(self.num_players, self.rnd, proposer, mission, votes))
        self.votes_for = votes_for
        if 2 * len(votes_for) <= self.num_players: self.downvotes += 1

    def betray(self, mission, proposer):
        if self.is_spy():
            if self.fails == 2 and self.enough_spies(mission): return True
            if self.successes == 2: return True
            elif self.num_spies_in(mission) > self.betrayals_required():
                return random() < self.risky_betray_rate[self.rnd]
            elif self.num_spies_in(mission) < self.betrayals_required(): return False
            else: return random() < self.betray_rate[self.rnd]
        return False # is resistance

    def update_suspicions(self):
            '''
            Updates self.suspicions to reflect the probability of each player being
            a spy
            '''
            self.suspicions = {x: 0 for x in range(self.num_players)}
            worlds = self.worlds.items()
            for x in range(self.num_players):
                for w, wp in worlds:
                    if x in w: self.suspicions[x] += wp

    # def print_suspicions(self):
    #     print(f"\nPlayer {self.player_number}:")
    #     print({s[0]: round(s[1],5) for s in self.suspicions.items()})

    def outcome_probability(self, spies_in_mission, betrayals, betray_rate):
        '''
        Probability of a mission outcome given a world
        '''
        if spies_in_mission < betrayals: return 0
        if spies_in_mission == 0 and betrayals == 0: return 1
        return betray_rate ** betrayals * (1-betray_rate) ** (spies_in_mission-betrayals) \
                * comb(spies_in_mission, betrayals)

    def vote_probability(self, world, sf, ss, rf, rs, mission_success):
        '''
        Probability of a voting pattern for a mission outcome given a world
        '''
        p = 1
        for x in range(self.num_players):
            if x in world and x in self.votes_for:
                if mission_success: p *= ss
                else: p *= sf
            elif x in world and x not in self.votes_for:
                if mission_success: p *= (1-ss)
                else: p *= (1-sf)
            elif x not in world and x in self.votes_for:
                if mission_success: p *= rs
                else: p *= rf
            elif x not in world and x not in self.votes_for:
                if mission_success: p *= (1-rs)
                else: p *= (1-rf)
        return p

    def proposer_probability(self, world, proposer, sf, ss, rf, rs, mission_success):
        '''
        Probability of proposer causing a mission outcome given a world
        '''
        if proposer in world and mission_success: return ss
        elif proposer in world and not mission_success: return sf
        elif proposer not in world and mission_success: return rs
        elif proposer not in world and not mission_success: return rf

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        Update the last Mission object with mission info
        Update world probabilities
        '''
        # self.missions[-1].betrayals = betrayals
        # self.missions[-1].success = mission_success
        if not mission_success: self.failed_teams.append(mission)

        if len(self.worlds) > 1 and self.rnd < 4:

            br = self.opponent_betray_rate[self.rnd]

            vsf = self.spy_vote_failed[self.rnd]
            vss = self.spy_vote_success[self.rnd]
            vrf = self.res_vote_failed[self.rnd]
            vrs = self.res_vote_success[self.rnd]

            psf = self.spy_propose_failed[self.rnd]
            pss = self.spy_propose_success[self.rnd]
            prf = self.res_propose_failed[self.rnd]
            prs = self.res_propose_success[self.rnd]

            outcome_prob = 0  # overall probability of this mission outcome
            for w, wp in self.worlds.items():
                spies_in_mission = len([x for x in w if x in mission])
                outcome_prob += self.outcome_probability(spies_in_mission, betrayals, br) * wp
            
            impossible_worlds = []
            for w, wp in self.worlds.items():
                spies_in_mission = len([x for x in w if x in mission])
                if spies_in_mission == betrayals and len(mission) == betrayals:
                    self.worlds = {w:1}
                    break 
                self.worlds[w] *= self.outcome_probability(spies_in_mission, betrayals, br) / outcome_prob
                if self.worlds[w] == 0: impossible_worlds.append(w) 
            for w in impossible_worlds: self.worlds.pop(w, None)
            
            voting_prob = 0  # overall probability of a voting pattern given mission outcome
            for w, wp in self.worlds.items():    
                voting_prob += self.vote_probability(w, vsf, vss, vrf, vrs, mission_success) * wp
            
            for w in self.worlds.keys():
                new_p = self.vote_probability(w, vsf, vss, vrf, vrs, mission_success) \
                    * self.worlds[w] / voting_prob
                self.worlds[w] = self.voting_weight * new_p + (1-self.voting_weight) * self.worlds[w]

            proposer_prob = 0  # overall probability of a proposer given mission outcome    
            for w, wp in self.worlds.items():    
                proposer_prob += self.proposer_probability(w, proposer, psf, pss, prf, prs, mission_success) * wp
            
            for w in self.worlds.keys(): 
                new_p = self.proposer_probability(w, proposer, psf, pss, prf, prs, mission_success) \
                    * self.worlds[w] / proposer_prob
                self.worlds[w] = self.proposer_weight * new_p + (1-self.proposer_weight) * self.worlds[w]

            self.update_suspicions()

    def round_outcome(self, rounds_complete, missions_failed):
        
        #self.missions[-1].success = (missions_failed == self.fails)
        self.rnd = rounds_complete
        self.fails = missions_failed
        self.successes = rounds_complete - missions_failed
        self.downvotes = 0
    
    def game_outcome(self, spies_win, spies): pass
