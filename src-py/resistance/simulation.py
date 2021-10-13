from game import Game
from learning_bayes import LearningBayes
import sys, time
from random import randrange, choice, sample
import json

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

def run(num_games, agents, data=None, verbose=True):
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
    l_win_rate = 0
    for a in agent_groups:
        print(f"{a.name}: spy win rate {a.spy_win_rate()}, res win rate {a.res_win_rate()}, overall win rate {a.win_rate()}\n")
        if a.name == "LearningBayes": l_win_rate = a.win_rate()
    
    return l_win_rate

    
if __name__ == "__main__":
    from random_agent import Random
    from baseline import Baseline
    from learning_bayes import LearningBayes
    from bayes3 import Bayes3

    trials    = 100
    games     = 1000
    changes   = 3
    increment = 0.02
    dp        = 3     # decimal places of data
    chances_to_improve = 5
    agents = [LearningBayes, Bayes3]

    with open('data.json') as f: data = json.load(f)
    old_win_rate = data["win_rate"]
    keys = list(data.keys())
    keys.remove("win_rate")
    attributes = sample(keys, changes)

    abc = [randrange(changes) for i in range(3)]
    amount = [choice([-increment, increment]) for i in range(changes)]
    for i in range(changes): data[attributes[i]][abc[i]] += amount[i]
    for k in keys:
        for i in range(3): data[k][i] = round(data[k][i], dp)

    did_not_improve_count = 0

    for i in range(trials):
        print(f'\nTrial {i+1}\n')
        new_win_rate = run(games, agents, data)
        if new_win_rate > data["win_rate"]: 
            print("Improved.")
            did_not_improve_count = 0
            
            # update data
            data["win_rate"] = round(new_win_rate, 4)
            with open("data.json", 'w') as f: json.dump(data, f, indent=2)
            
            # increment same values again
            for i in range(changes): data[attributes[i]][abc[i]] += amount[i]
            for k in keys:
                for i in range(3): data[k][i] = round(data[k][i], dp)       
        else:
            print("Did not improve.")
            did_not_improve_count += 1

            if did_not_improve_count == chances_to_improve:
                print("Reverting changes")
                # revert changes
                with open('data.json') as f: data = json.load(f)
                #for i in range(changes): data[attributes[i]][abc[i]] -= amount[i]

                did_not_improve_count = 0
            
            # increment new random numbers
            attributes = sample(keys, changes)
            abc = [randrange(changes) for i in range(changes)]
            amount = [choice([-increment, increment]) for i in range(changes)]

            for i in range(changes): data[attributes[i]][abc[i]] += amount[i]
            for k in keys:
                for i in range(3): data[k][i] = round(data[k][i], dp)


