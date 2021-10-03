from agent import Agent

class HumanAgent(Agent):
    '''
    A human agent.
    Actions must be input on the command line.
    '''
    def __init__(self, name="Human"):
        self.name = name
        self.number_of_players = 0
        self.player_number = 0

    def __str__(self): return 'Agent '+self.name

    def __repr__(self): return self.__str__()

    def new_game(self, number_of_players, player_number, spies):
        self.number_of_players = number_of_players
        self.player_number = player_number

    def propose_mission(self, team_size, fails_required = 1):
        i = input(f"\nPlayer {self.player_number}, propose a team of {team_size}.\nInput player numbers separated by spaces: ")
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
        if len(team) != team_size: return self.propose_mission(team_size, fails_required)
        print()
        return team
                
    def vote(self, mission, proposer):
        i = input(f"\nPlayer {self.player_number}, vote for leader: {proposer}, team: {mission}?\nInput y or n: ")
        if i == 'y': return True
        elif i == 'n': return False
        return self.vote(mission, proposer)

    def vote_outcome(self, mission, proposer, votes): pass

    def betray(self, mission, proposer):
        i = input(f"\nPlayer {self.player_number}, betray leader: {proposer}, team: {mission}?\nInput y or n: ")
        if i == 'y': return True
        elif i == 'n': return False
        return self.betray(mission, proposer)

    def mission_outcome(self, mission, proposer, num_fails, mission_success): pass

    def round_outcome(self, rounds_complete, missions_failed): pass
    
    def game_outcome(self, spies_win, spies): pass