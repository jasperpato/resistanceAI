from random import randint
from game import *

'''
Simulate games and print aggregates
'''
f_wins = 0
r_wins = 0
for i in range(10000):
    n = randint(0,5)
    g = Game([RandomAgent(str(j)) for j in range(n)] + [FirstAgent(str(5-j)) for j in range(5-n)])
    g.play()
    if g.missions_lost < 3:
        for j in range(g.num_players):
            if j not in g.spies:
                if j < n:
                    r_wins += 1
                else:
                    f_wins += 1
    else:
        for j in range(g.num_players):
            if j in g.spies:
                if j < n:
                    r_wins += 1
                else:
                    f_wins += 1

print(f"FirstAgent won {f_wins} times.")
print(f"RandomAgent won {r_wins} times.")

