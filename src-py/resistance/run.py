from game import Game
from learning_bayes import LearningBayes
import sys, time
from random import randrange, choice

class AgentStats():
    '''
    Collects the stats for each agent class.
    '''
    def __init__(self, agent_class):
        self.agent_class = agent_class
        self.name = agent_class.__name__
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

def run(num_games, agents, data=None):
    '''
    Simulates s random games between the agents specified in agents and prints results
    '''
    t = time.time()

    agent_groups = [AgentStats(c) for c in agents]
    print('\n'+str([a.name for a in agent_groups]))
    for i in range(num_games):
        sys.stdout.write(f"\rSimulating game {i+1} / {num_games}")
        sys.stdout.flush()
        n = randrange(5,11)
        players = []
        for i in range(n):
            p = choice(agents)
            if p is LearningBayes: players.append(p(data))
            else: players.append(p())
        game = Game(players)
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
    
    print(f'\nTime taken {round(time.time()-t,2)} seconds\n')
    for a in agent_groups:
        print(f"{a.name}: spy win rate {a.spy_win_rate()}, res win rate {a.res_win_rate()}, overall win rate {a.win_rate()}\n")

    return {a.name: a.win_rate() for a in agent_groups}

if __name__ == "__main__":
    from random_agent import Random
    from baseline import Baseline
    from bayes import Bayes
    from bayes2 import Bayes2
    from bayes3 import Bayes3
    import json

    num_games = 500
    agents    = [LearningBayes, Bayes3]

    data = None
    with open('data.json') as f: data = json.load(f)

    run(num_games, agents, data)


