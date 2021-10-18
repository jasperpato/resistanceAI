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

    num_games  = 50
    
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

        for k in genes.keys(): print(k, genes[k]['vote_threshold'], win_rates[k])
        print(rankings)

        new_genes = {
            'Ev0': genes[rankings[0]],
            'Ev1': genes[rankings[1]],
            'Ev2': genes[rankings[2]],
            'Ev3': child(genes[rankings[0]], genes[rankings[1]]),
            'Ev4': child(genes[rankings[0]], genes[rankings[2]]),
            'Ev5': mutate(genes[rankings[0]]),
            'Ev6': mutate(genes[rankings[0]]),
            'Ev7': mutate(genes[rankings[1]])
        }

        for k in new_genes.keys(): print(k, new_genes[k]['vote_threshold'])

        with open('genes.json', 'w') as f: json.dump(new_genes, f)

        


