from agent import Agent
from random import random, sample
from itertools import combinations
from math import comb
from mission import Mission

class Evolver(Agent):    
    '''
    Maintains probabilities of all possible worlds.
    Calculates the probabilty of each player being a spy from set of worlds.
    World probabilities are updated on mission outcomes, voting patterns and
    proposers.

    Behavioural data passed in as a dictionary.
    '''    

    def __init__(self, data, name='Evolver'):
        self.data = data
        self.name = name

        # hard code weights for now
        self.data['vote_weight'] = [0,0,0,0.4]
        self.data['proposer_weight'] = [0,0,0,0.3]

    def calc_threshold(self, vec):
        '''
        Converts a 4D vector into an unbounded threshold value
        '''
        return vec[0]*self.rnd*self.rnd + vec[1]*self.rnd + vec[2]*self.fails + vec[3]

    def calc_rate(self, vec):
        '''
        Converts a 4D vector into a probability between 0.01 and 0.99
        '''
        return min(0.99, max(0.01, vec[0]*self.rnd*self.rnd + vec[1]*self.rnd + vec[2]*self.fails + vec[3]))

    def is_spy(self): return self.spies != []

    def average_suspicion(self):
        return self.spy_count[self.num_players] / self.num_players

    def betrayals_required(self):
        return self.fails_required[self.num_players][self.rnd]

    def new_game(self, num_players, player_number, spies):
        '''
        Initialises the game, spies is empty if player is not a spy
        '''
        self.rnd       = 0
        self.successes = 0
        self.fails     = 0
        self.downvotes = 0

        self.num_players   = num_players
        self.player_number = player_number
        self.num_spies     = self.spy_count[self.num_players]
        self.spies         = spies
        self.missions      = []
        self.failed_teams  = [] # teams that betrayed - avoid them

        worlds = list(combinations(range(self.num_players), self.num_spies))
        self.worlds = {w: 1/len(worlds) for w in worlds}
        self.update_suspicions()

    def possible_teams(self, l):
        '''
        Returns list of all possible teams of length l including self,
        in ascending average suspicion
        '''
        teams = [t for t in list(combinations(range(self.num_players), l)) if self.player_number in t]
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
        return [self.player_number] + \
            sample([x for x in range(self.num_players) if x != self.player_number], team_size-1)

    def mission_suspicion(self, mission):
        '''
        Returns the average suspicion of a mission. Does not include self
        '''
        others = [self.suspicions[x] for x in mission if x != self.player_number]
        return sum(others) / len(others)

    def vote(self, mission, proposer):
        if self.rnd == 0 or proposer == self.player_number or self.downvotes == 4:
            return True
        if self.is_spy():
            if self.successes == 2:
                return True if self.enough_spies(mission) else False
            if self.enough_spies(mission) and not self.bad_mission(mission):
                return self.mission_suspicion(mission) <= \
                    self.calc_threshold(self.data['failable_vote_threshold']) * self.average_suspicion()
        if self.bad_mission(mission): return False
        if self.player_number not in mission and \
            len(mission) >= self.num_players - self.num_spies: return False
        return self.mission_suspicion(mission) <= \
            self.calc_threshold(self.data['vote_threshold']) * self.average_suspicion()

    def vote_outcome(self, mission, proposer, votes):
        '''
        Add a new Mission object to our stored info
        '''
        self.missions.append(Mission(self.num_players, self.rnd, proposer, mission, votes))
        if 2 * len(votes) <= self.num_players: self.downvotes += 1

    def betray(self, mission, proposer):
        if self.is_spy():
            if self.fails == 2 and self.enough_spies(mission): return True
            if self.successes == 2: return True
            elif self.num_spies_in(mission) > self.betrayals_required():
                return random() < self.calc_rate(self.data['risky_betray_rate'])
            elif self.num_spies_in(mission) < self.betrayals_required(): return False
            else:
                return random() < self.calc_rate(self.data['betray_rate'])
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

    def print_suspicions(self):
        print(f'\nPlayer {self.player_number}:')
        print({s[0]: round(s[1],5) for s in self.suspicions.items()})

    def outcome_probability(self, spies_in_mission, betrayals, betray_rate):
        '''
        Probability of a mission outcome given a world
        '''
        if spies_in_mission < betrayals: return 0
        if spies_in_mission == 0 and betrayals == 0: return 1
        return betray_rate ** betrayals * (1-betray_rate) ** (spies_in_mission-betrayals) \
                * comb(spies_in_mission, betrayals)

    def vote_probability(self, world, votes_for, sf, ss, rf, rs, mission_success):
        '''
        Probability of a voting pattern for a mission outcome given a world
        '''
        p = 1
        for x in range(self.num_players):
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
        self.missions[-1].betrayals = betrayals
        self.missions[-1].success = mission_success
        if not mission_success: self.failed_teams.append(mission)

        if len(self.worlds) > 1 and self.rnd < 4:

            br  = self.calc_rate(self.data['opponent_betray_rate'])
            vsf = self.calc_rate(self.data['spy_vote_failed'])
            vss = self.calc_rate(self.data['spy_vote_success'])
            vrf = self.calc_rate(self.data['res_vote_failed'])
            vrs = self.calc_rate(self.data['res_vote_success'])
            psf = self.calc_rate(self.data['spy_propose_failed'])
            pss = self.calc_rate(self.data['spy_propose_success'])
            prf = self.calc_rate(self.data['res_propose_failed'])
            prs = self.calc_rate(self.data['res_propose_success'])

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
                voting_prob += self.vote_probability(w, self.missions[-1].votes_for, \
                    vsf, vss, vrf, vrs, mission_success) * wp
            
            for w in self.worlds.keys():
                new_p = self.vote_probability(w, self.missions[-1].votes_for, vsf, vss, vrf, vrs, mission_success) \
                    * self.worlds[w] / voting_prob
                vw = self.calc_rate(self.data['vote_weight'])
                self.worlds[w] = vw * new_p + (1-vw) * self.worlds[w]

            proposer_prob = 0  # overall probability of a proposer given mission outcome    
            for w, wp in self.worlds.items():    
                proposer_prob += self.proposer_probability(w, proposer, psf, pss, prf, prs, mission_success) * wp
            
            for w in self.worlds.keys(): 
                new_p = self.proposer_probability(w, proposer, psf, pss, prf, prs, mission_success) \
                    * self.worlds[w] / proposer_prob
                pw = self.calc_rate(self.data['proposer_weight'])
                self.worlds[w] = pw * new_p + (1-pw) * self.worlds[w]

            self.update_suspicions()

    def round_outcome(self, rounds_complete, missions_failed):
        
        self.missions[-1].success = (missions_failed == self.fails)
        
        self.rnd = rounds_complete
        self.fails = missions_failed
        self.successes = rounds_complete - missions_failed
        self.downvotes = 0
    
    def game_outcome(self, spies_win, spies): pass
