# from determined_game import Game  # first spy_count players in agent list become spies
from game import Game               # spies are randomly assigned
from random_agent import Random
from baseline import Baseline
from bayes import Bayes
from bayes2 import Bayes2
from random import randrange, choice

class AgentStats():
    '''
    Collects the stats for each agent class.
    '''
    def __init__(self, agent_class):
        self.agent_class = agent_class
        self.name = agent_class().class_str
        self.spy_wins = 0
        self.res_wins = 0
        self.spy_plays = 0
        self.res_plays = 0

    def spy_win_rate(self):
        if self.spy_plays <= 0: return 0
        else: return round(self.spy_wins / self.spy_plays, 5)

    def res_win_rate(self):
        if self.res_plays <= 0: return 0
        else: return round(self.res_wins / self.res_plays, 5)
    
    def win_rate(self):
        if self.spy_plays + self.res_plays <= 0: return 0
        else: return round((self.spy_wins + self.res_wins) / (self.spy_plays + self.res_plays), 5)

if __name__ == "__main__":
    '''
    Simulates s random games between the agents specified in agents and prints results
    '''
    s = 10000
    agents = [Bayes, Bayes2]

    agent_groups = [AgentStats(c) for c in agents]
    for i in range(s):
        n = randrange(5,11)
        game = Game([choice(agents)() for i in range(n)])
        game.play()
        for j in range(n): 
            for a in agent_groups:
                if isinstance(game.agents[j], a.agent_class):
                    if j in game.spies: a.spy_plays += 1
                    else: a.res_plays += 1
            if game.missions_lost >= 3 and j in game.spies:
                for a in agent_groups:
                    if isinstance(game.agents[j], a.agent_class): a.spy_wins += 1      
            elif game.missions_lost < 3 and j not in game.spies:
                for a in agent_groups:
                    if isinstance(game.agents[j], a.agent_class): a.res_wins += 1
    print()
    for a in agent_groups:
        print(f"{a.name}: spy wins {a.spy_wins}, spy plays {a.spy_plays}, spy win rate {a.spy_win_rate()}")
        print(f"{a.name}: res wins {a.res_wins}, res plays {a.res_plays}, res win rate {a.res_win_rate()}\n")
        print(f"{a.name}: overall win rate {a.win_rate()}\n")




