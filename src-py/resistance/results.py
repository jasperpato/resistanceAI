from game import *
from random_agent import *
from baseline import *
from human import *
from random import randrange

'''
Simulate games and print aggregates
'''

f_wins, r_wins, f_losses, r_losses = 0, 0, 0, 0
for i in range(10):
    n = randrange(6)
    g = Game([RandomAgent(str(j)) for j in range(n)] + [BaselineAgent(str(j)) for j in range(n, 5)])
    g.play()
    for j in range(5): 
        if g.missions_lost < 3:
            if j not in g.spies:
                if isinstance(g.agents[j], BaselineAgent): f_wins += 1
                else: r_wins += 1
            else:
                if isinstance(g.agents[j], BaselineAgent): f_losses += 1
                else: r_losses += 1
        else:
            if j in g.spies:
                if isinstance(g.agents[j], BaselineAgent): f_wins += 1
                else: r_wins += 1
            else:
                if isinstance(g.agents[j], BaselineAgent): f_losses += 1
                else: r_losses += 1

print(f"BaselineAgent won {f_wins} times.")
print(f"BaselineAgent lost {f_losses} times.")
print(f"RandomAgent won {r_wins} times.")
print(f"RandomAgent lost {r_losses} times.")


