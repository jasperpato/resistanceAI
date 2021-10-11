# from determined_game import Game  # first spy_count players in agent list become spies
from game import Game               # spies are randomly assigned
import sys, time
from random import randrange, choice
import json

class AgentStats():
    '''
    Collects the stats for each agent class.
    '''
    def __init__(self, agent_class):
        self.agent_class = agent_class
        if agent_class is LearningBayes: self.name = "LearningBayes"
        else : self.name = agent_class().class_name
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

def fitness_function(s, agents):
    '''
    Simulates s random games between the agents specified in agents and prints results
    '''
    t = time.time()

    with open ('base_data.json') as f:
            data = json.load(f)

    agent_groups = [AgentStats(c) for c in agents]
    print('\n'+str([a.name for a in agent_groups]))
    for i in range(s):
        sys.stdout.write(f"\rSimulating game {i+1} / {s}")
        sys.stdout.flush()
        n = randrange(5,11)
        players = []
        for i in range(n):
            player = choice(agents)
            if player is LearningBayes: players.append(player(data))
            else : players.append(player())
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
    genetic_win_rate = 0
    for a in agent_groups:
        print(f"{a.name}: spy wins {a.spy_wins}, spy plays {a.spy_plays}, spy win rate {a.spy_win_rate()}")
        print(f"{a.name}: res wins {a.res_wins}, res plays {a.res_plays}, res win rate {a.res_win_rate()}\n")
        print(f"{a.name}: overall win rate {a.win_rate()}\n")
        if a.name == "LearningBayes": learner_win_rate = a.win_rate()
    
    return learner_win_rate

def mutator(data):
    with open("new_data.json", 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    from random_agent import Random
    from baseline import Baseline
    from learning_bayes import LearningBayes
    from bayes3 import Bayes3

    s = 200
    agents = [LearningBayes, Baseline, Random]
    
    if len(sys.argv) > 1:
        s = int(sys.argv[1])

    current_win_rate = 0
    for i in range(1):
        new_win_rate = fitness_function(s, agents)
        if current_win_rate < new_win_rate:
            #learn some stuff
            pass


