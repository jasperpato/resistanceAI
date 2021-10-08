# from determined_game import Game # first spy_count players in agent list become spies
from game import Game # spies are randomly assigned
from random_agent import Random
from baseline import Baseline
from bayes import Bayes
# from spy import Spy
from random import randrange, choice

'''
Simulate games and print aggregates
'''
agent_classes = [Baseline, Bayes] # insert the agent classes to be played against each other
stats = []
for a in agent_classes:
    stats.append({"spy_wins": 0, "spy_plays": 0, "res_wins": 0, "res_plays": 0})

for i in range(10000):
    n = randrange(5,11)
    g = Game([choice(agent_classes)() for i in range(n)])
    g.play()
    for j in range(n): 

        for i, a in enumerate(agent_classes):
            if isinstance(g.agents[j], a):
                if j in g.spies: stats[i]["spy_plays"] += 1
                else: stats[i]["res_plays"] += 1

        if g.missions_lost >= 3 and j in g.spies:
            for i, a in enumerate(agent_classes):
                if isinstance(g.agents[j], a):
                    stats[i]["spy_wins"] += 1
                
        elif g.missions_lost < 3 and j not in g.spies:
            for i, a in enumerate(agent_classes):
                if isinstance(g.agents[j], a):
                    stats[i]["res_wins"] += 1

print()
for i, a in enumerate(agent_classes):
    print(f"{a().class_str}: spy wins {stats[i]['spy_wins']}, spy plays {stats[i]['spy_plays']}," + \
    f" spy win rate {stats[i]['spy_plays']/stats[i]['spy_plays']}" if stats[i]['spy_plays'] > 0 else "")
    print(f"{a().class_str}: res wins {stats[i]['res_wins']}, res plays {stats[i]['res_plays']}," + \
    f" res win rate {stats[i]['res_plays']/stats[i]['res_plays']}\n" if stats[i]['res_plays'] > 0 else "\n")
    if stats[i]['spy_plays'] + stats[i]['res_plays'] > 0:
        print(f"{a().class_str}: overall win rate " + \
        f"{(stats[i]['spy_wins']+stats[i]['res_wins'])/(stats[i]['spy_plays']+stats[i]['res_plays'])}\n")




