from game import Game
import sys, time
from random import randrange, choice
from copy import deepcopy

class AgentStats():
    '''
    Collects the stats for each agent.
    '''
    def __init__(self, name):
        self.name      = name
        self.spy_wins  = 0
        self.res_wins  = 0
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

def run(num_games, agents, verbose=True):
    '''
    Simulates s random games between the agents specified in agents and prints results
    '''
    t = time.time()

    agent_stats = [AgentStats(a.name) for a in agents]
    if verbose: print('\n'+str([a.name for a in agent_stats]))
    for i in range(num_games):
        if verbose:
            sys.stdout.write(f"\rSimulating game {i+1} / {num_games}")
            sys.stdout.flush()
        n = randrange(5,11)
        game = Game([deepcopy(choice(agents)) for p in range(n)])
        game.play()
        for j in range(n): 
            for a in agent_stats:
                if game.agents[j].name == a.name:
                    if j in game.spies: a.spy_plays += 1
                    else: a.res_plays += 1
            if game.missions_lost >= 3 and j in game.spies:
                for a in agent_stats:
                    if game.agents[j].name == a.name: a.spy_wins += 1      
            elif game.missions_lost < 3 and j not in game.spies:
                for a in agent_stats:
                    if game.agents[j].name == a.name: a.res_wins += 1
    
    if verbose:
        print(f'\nTime taken {round(time.time()-t,2)} seconds\n')
        for a in agent_stats:
            print(f"{a.name}: spy win rate {a.spy_win_rate()}, res win rate {a.res_win_rate()}, overall win rate {a.win_rate()}\n")

    return {a.name: a.win_rate() for a in agent_stats}

if __name__ == "__main__":
    from random_agent import Random
    from baseline import Baseline
    from bayes import Bayes
    from bayes2 import Bayes2
    from bayes3 import Bayes3
    from evolver import Evolver
    import json
    import os
    p = os.path.dirname(__file__)

    genes = None
    with open(os.path.join(p, 'genes.json')) as f: genes = json.load(f)['Ev0']

    jordan = None
    with open(os.path.join(p, 'genes_jordan.json')) as f: jordan = json.load(f)['Ev0']

    genes250 = None
    with open(os.path.join(p, 'genes_250.json')) as f: genes250 = json.load(f)['Ev0']

    num_games = 10000

    if len(sys.argv) > 1:
        try: num_games = int(sys.argv[1])
        except: num_games = 10000

    agents    = [Evolver(genes), Bayes3(), Baseline(), Random()]

    run(num_games, agents)


