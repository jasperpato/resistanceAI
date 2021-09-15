from agent import Agent
from random import randrange, random

class Round:
    def __init__(self, leader, team, votes, success=False):
        '''
        leader: leader of round
        team: proposed team
        votes: list of booleans, eg. votes[player_number] = true
        outcome: true if mission succeeded
        '''
        self.leader = leader
        self.team = team
        self.votes = votes
        y = 0
        for v in votes:
            if v:
                y += 1
        self.majority = True if y > len(votes) // 2 else False
        self.success = success

class RandomAgent(Agent):        

    def __init__(self, name='Japer'):
        self.name = name
        self.number_of_players = 0
        self.players = []
        self.player_number = 0
        self.spy_list = []
        self.suspicions = [] # for each player, probability of being a spy
        self.is_spy = False
        self.rounds = [] # stores what occurred in each round in Round objects
        self.missions_failed = 0
        self.rounds_complete = 0

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
            self.suspicions.append
            (1.0 * self.spy_count[number_of_players] / number_of_players)

    def propose_mission(self, team_size, betrayals_required = 1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive)
        and number_of_players (exclusive) to be returned. 
        betrayals_required are the number of betrayals required for the mission
        to fail.
        '''
        if not self.is_spy: # team is self + least suspicious players
            s = sorted(self.suspicions).remove(self.player_number)
            return [self.player_number] + [s[i] for i in range(team_size-1)]
        else: # team is self + random, non-spy players
            res_list = [p for p in self.players if p not in self.spy_list]
            team = [self.player_number]
            while len(team) < team_size:
                n = randrange(len(res_list))
                if res_list(n) not in team:
                    team.append(res_list[n])
            return team

    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the
        player who proposed the mission.
        The function should return True if the vote is for the mission, and False
        if the vote is against the mission.
        '''
        return random()<0.5

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the
        player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for
        the mission, False otherwise).
        No return value is required or expected.
        '''
        #nothing to do here
        pass

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players,
        and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the
        player who proposed the mission.
        The method should return True if this agent chooses to betray the mission,
        and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
        if self.is_spy():
            spies_on_mission = sum(i in mission for i in self.spy_list)
            spies_required_for_fail = self.fails_required[self.number_of_players][self.rounds_complete+1]
            
            if (self.mission_fails == 2 and spies_on_mission >= spies_required_for_fail) or \
                (self.rounds_complete - self.mission_fails == 2):
                return True # possible game deciding vote
            elif spies_on_mission != spies_required_for_fail:
                return False # more than enough/not enough spies on mission for sabotage
            else:
                return True
        
        return False # not a spy

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the
        player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the
        mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        pass

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the number of missions (0-3) that have failed.
        '''
        self.rounds_complete = rounds_complete
        self.mission_fails = missions_failed
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        #nothing to do here
        pass



