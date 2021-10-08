from agent import Agent
from determined_game import Game # first spy_count players in agent list become spies
#from game import Game # spies are randomly assigned
from random_agent import Random
from baseline import Baseline
from bayes import Bayes
from human import Human
from spy import Spy
from random import randrange

'''
Simulate games and print aggregates
'''
b_spy_wins, b_res_wins, b_spy_plays, b_res_plays = 0, 0, 0, 0
r_spy_wins, r_res_wins, r_spy_plays, r_res_plays = 0, 0, 0, 0
for i in range(1000):
    n = randrange(5,11)
    s = Agent.spy_count[n]
    r = randrange(n+1)
    g = Game([Baseline() for j in range(s)] + [Random() for j in range(s,n)])
    g.play()
    for j in range(n): 

        if isinstance(g.agents[j], Baseline):
             if j in g.spies: b_spy_plays += 1
             else: b_res_plays += 1
        else:
            if j in g.spies: r_spy_plays += 1
            else: r_res_plays += 1

        if g.missions_lost >= 3 and j in g.spies:
            if isinstance(g.agents[j], Baseline): b_spy_wins += 1
            else: r_spy_wins += 1
        elif g.missions_lost < 3 and j not in g.spies:
            if isinstance(g.agents[j], Baseline): b_res_wins += 1
            else: r_res_wins += 1

print(f"\nBaseline spy wins {b_spy_wins} spy plays {b_spy_plays} spy win rate {round(b_spy_wins/b_spy_plays,4)}")
#print(f"Baseline res wins {b_res_wins} res plays {b_res_plays} res res rate {round(b_res_wins/b_res_plays,4)}\n")
print(f"Baseline overall win rate {round((b_spy_wins+b_res_wins)/(b_spy_plays+b_res_plays),4)}\n")

#print(f"Other spy wins {r_spy_wins} spy plays {r_spy_plays} spy win rate {round(r_spy_wins/r_spy_plays,4)}")
print(f"Other res wins {r_res_wins} res plays {r_res_plays} res win rate {round(r_res_wins/r_res_plays,4)}\n")
print(f"Other overall win rate {round((r_spy_wins+r_res_wins)/(r_spy_plays+r_res_plays),4)}\n")




