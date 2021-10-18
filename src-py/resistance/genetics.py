from evolver import Evolver
from bayes3 import Bayes3
from baseline import Baseline
from random_agent import Random

from run import run
from copy import deepcopy
import json
from random import random, randrange

def child(d1, d2):
    d = {}
    for k in d1.keys():
        d[k] = []
        for n in range(len(d1[k])):
            d[k].append(round((d1[k][n] + d2[k][n]) / 2, 2))
    return d

def mutate(d_in):
    d = deepcopy(d_in)
    for k in d.keys():
        if random() < 0.5:
            for n in range(len(d[k])):
                if random() < 0.5:
                    d[k][n] = round(d[k][n] + randrange(-5, 6) / 100, 2)
    return d

if __name__ == '__main__':

    num_games  = 5000
    
    t = 0
    while True:
        
        genes = None
        with open('genes.json') as f: genes = json.load(f)
        
        agents = [Evolver(data, name) for name, data in genes.items()]
        agents += [Bayes3(), Baseline(), Random()]

        print(f"Trial {t}")
        t+=1
        win_rates = run(num_games, agents, False)
        win_rates.pop('Bayes3')
        win_rates.pop('Baseline')
        win_rates.pop('Random')

        rankings = sorted(win_rates, key=win_rates.get, reverse=True)

        new_genes = {}
        for i, k in enumerate(genes.keys()):
            if i < 3:
                new_genes[k] = genes[rankings[i]]
            elif i == 3:
                new_genes[k] = child(genes[rankings[0]], genes[rankings[1]])
            elif i == 4:
                new_genes[k] = child(genes[rankings[0]], genes[rankings[2]])
            elif i < 7:
                new_genes[k] = mutate(genes[rankings[0]])
            else:
                new_genes[k] = mutate(genes[rankings[1]])

        with open('genes.json', 'w') as f: json.dump(new_genes, f)

        


