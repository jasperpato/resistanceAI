from agent import Agent

class HumanAgent(Agent):
    '''
    A human agent.
    Actions must be input on the command line.
    '''
    def __init__(self, name="Human"):
        self.name = name
        self.number_of_players = 0

    def __str__(self): return 'Agent '+self.name

    def __repr__(self): return self.__str__()

    def new_game(self, number_of_players, player_number, spies):
        self.number_of_players = number_of_players

    def propose_mission(self, team_size, fails_required = 1):
        i = input(f"\nPropose a team of {team_size}.\nInput player numbers separated by spaces: ")
        team = []
        for j in i.split():
            if j == '': continue
            try:
                n = int(j)
                if n < 0 or n >= self.number_of_players or n in team:
                    return self.propose_mission(team_size, fails_required)
                team.append(n)
            except:
                return self.propose_mission(team_size, fails_required)
        return team
                
    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        i = input(f"\nVote for leader: {proposer}, team: {mission}?\nInput y or n: ")
        if i == 'y': return True
        elif i == 'n': return False
        return self.vote(mission, proposer)

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        pass

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        Only spies are permitted to betray the mission. 
        '''
        i = input(f"\nBetray leader: {proposer}, team: {mission}?\nInput y or n: ")
        if i == 'y': return True
        elif i == 'n': return False
        return self.betray(mission, proposer)

    def mission_outcome(self, mission, proposer, num_fails, mission_success):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        num_fails is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        pass

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        pass