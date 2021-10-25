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
    Simulates randomised games between agents
    Returns a dictionary mapping the agents' name to their win rate 
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
    from random_agent import RandomAgent
    from baseline import Baseline
    from bayes import Bayes
    from bayes2 import Bayes2
    from bayes3 import Bayes3
    from evolver import Evolver
    from evolved import Evolved
    from monte_high_bf import MonteHigh
    from monte_low_bf import MonteLow
    import json

    num_games = 500
    agents    = [Evolved(), Bayes3(), MonteLow(), MonteHigh(), RandomAgent()]

    if len(sys.argv) > 1:
        
        try: num_games = int(sys.argv[1])
        except: num_games = 10000

        if sys.argv[1] == 'compare':
            genes = None
            with open('genes.json') as f: genes = json.load(f)['Ev0']
            agents = [Evolver(genes), Bayes3(), Baseline(), RandomAgent()]
        else:
            try:
                genes = None
                with open(sys.argv[1]) as f: genes = json.load(f)
                agents = [Evolver(data, name) for name, data in genes.items()] 
            except: pass
        
        if len(sys.argv) > 2:
            try: num_games = int(sys.argv[2])
            except: num_games = 10000

    run(num_games, agents)
