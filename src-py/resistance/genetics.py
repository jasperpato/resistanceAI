from run import run
from evolver import Evolver
import json
from random import random, randrange

def child(d1, d2):
    d = {}
    for k in d1.keys():
        d[k] = []
        for n in range(4):
            d[k].append(round((d1[k][n] + d2[k][n]) / 2, 2))
    return d

def mutate(d_in):
    d = d_in.copy()
    for k in d.keys():
        if random() < 0.5:
            for n in range(4):
                if random() < 0.5:
                    d[k][n] = round(d[k][n] + randrange(-5, 6) / 100, 2)
    return d

if __name__ == '__main__':

    num_trials = 100
    num_games  = 5000

    for t in range(num_trials):
        
        genes = None
        with open('genes.json') as f: genes = json.load(f)
        
        agents = [Evolver(data, name) for name, data in genes.items()]

        print(f"Trial {t}")
        win_rates = run(num_games, agents)
        rankings = sorted(win_rates, key=win_rates.get)

        new_genes = genes
        for i, k in enumerate(new_genes.keys()):
            if i < 3: # top 3 survive
                new_genes[k] = genes[rankings[i]]
            elif i == 3: # next two are children of top 1 with next two
                new_genes[k] = child(genes[rankings[0]], genes[rankings[1]])
            elif i == 4:
                new_genes[k] = child(genes[rankings[0]], genes[rankings[2]])
            elif i < 6: # next two are mutations of top 1
                new_genes[k] = mutate(genes[rankings[0]])
            else: # last one is mutation of rank 2
                new_genes[k] = mutate(genes[rankings[1]])

        with open('genes.json', 'w') as f: json.dump(new_genes, f)

        


