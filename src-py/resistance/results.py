from random import randrange
from game import *

'''
Simulate games and print aggregates
'''
f_wins = 0
r_wins = 0
for i in range(10000):
    n = randrange(6)
    g = Game([RandomAgent(str(j)) for j in range(n)] + [FirstAgent(str(j)) for j in range(n, 5)])
    g.play()
    if g.missions_lost < 3:
        for j in range(5): 
            if j not in g.spies:
                if isinstance(g.agents[j], FirstAgent): f_wins += 1
                else: r_wins += 1
    else:
        for j in range(5): 
            if j in g.spies:
                if isinstance(g.agents[j], FirstAgent): f_wins += 1
                else: r_wins += 1

print(f"FirstAgent won {f_wins} times.")
print(f"RandomAgent won {r_wins} times.")

