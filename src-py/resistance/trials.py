from evolver import Evolver
from bayes3 import Bayes3
from baseline import Baseline
from random_agent import RandomAgent

from run import run
from copy import deepcopy
import json
from random import random, randrange

def child(d1, d2):
    '''
    Returns the average of two dictionaries.
    '''
    d = {}
    for k in d1.keys():
        d[k] = []
        for n in range(len(d1[k])):
            d[k].append(round((d1[k][n] + d2[k][n]) / 2, 2))
    return d

def mutate(d_in):
    '''
    Returns a randomly mutated deepcopy of input dictionary.
    '''
    d = deepcopy(d_in)
    for k in d.keys():
        # if k in ['outcome_weight', 'vote_weight', 'proposer_weight']: continue
        for n in range(len(d[k])):
            if random() < 0.25: d[k][n] = round(d[k][n] + randrange(-5, 6) / 100, 2)
    return d

if __name__ == '__main__':
    '''
    Performs endless genetic trials. 8 agents play off against each other. Their
    behavioural data is stored in genes.json, and updated after each trial as
    follows:

    - top 3 agents' data survive
    - 4 is child of top 1 and 2
    - 5 is child of top 1 and 3
    - 6, 7 are mutations of top 1
    - 8 is mutation of 2
    '''

    num_games  = 7500
    
    t = 0
    while True:
        
        genes = None
        with open('genes.json') as f: genes = json.load(f)
        
        agents = [Evolver(data, name) for name, data in genes.items()]
        agents += [Bayes3(), Baseline(), RandomAgent()] # other agents added for control

        print('Trial '+str(t))
        t+=1
        
        win_rates = run(num_games, agents, False)
        win_rates.pop('Bayes3')
        win_rates.pop('Baseline')
        win_rates.pop('RandomAgent')

        rankings = sorted(win_rates, key=win_rates.get, reverse=True)
        print(win_rates)

        new_genes = {}
        for i, k in enumerate(genes.keys()):
            if i < 3:    new_genes[k] = genes[rankings[i]]
            elif i == 3: new_genes[k] = child(genes[rankings[0]], genes[rankings[1]])
            elif i == 4: new_genes[k] = child(genes[rankings[0]], genes[rankings[2]])
            elif i < 7:  new_genes[k] = mutate(genes[rankings[0]])
            else:        new_genes[k] = mutate(genes[rankings[1]])

        with open('genes.json', 'w') as f: json.dump(new_genes, f, indent='')
