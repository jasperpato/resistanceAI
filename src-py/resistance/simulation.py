from random import Random


if __name__ == "__main__":
    from random_agent import Random
    from baseline import Baseline
    from bayes import Bayes
    from bayes2 import Bayes2
    from bayes3 import Bayes3
    from learning_bayes import LearningBayes
    from random import randrange, choice, sample
    import json
    from run import run

    n_trials    = 100
    n_games     = 500
    n_changes   = 5
    increment   = 0.02
    n_dp        = 2
    agents = [LearningBayes, Bayes3, Bayes2, Bayes, Baseline, Random]

    with open('data.json') as f: data = json.load(f)
    old_win_rate = data["win_rate"]
    keys = list(data.keys())
    keys.remove("win_rate")
    
    attributes = sample(keys, n_changes)
    abc = [randrange(3) for i in range(n_changes)]
    amount = [choice([-increment, increment]) for i in range(n_changes)]

    for i in range(n_changes):
        d = data[attributes[i]][abc[i]]
        data[attributes[i]][abc[i]] = round(d + amount[i], n_dp)

    for i in range(n_trials):
        print(f'\nTrial {i+1}\n')
        
        win_rates = run(n_games, agents, data)
        l_rate = win_rates["LearningBayes"]
        win_rates.pop("LearningBayes")
        others_rate = sum([r for r in win_rates.values()]) / len(win_rates)

        if l_rate - others_rate > data["win_rate_difference"]: 
            print("Improved.")
 
            # update data
            data["win_rate_difference"] = round(l_rate - others_rate, 4)
            with open("data.json", 'w') as f: json.dump(data, f, indent=2)
            
            # increment same values again
            for i in range(n_changes):
                d = data[attributes[i]][abc[i]]
                data[attributes[i]][abc[i]] = round(d + amount[i], n_dp)       
        else:
            print("Did not improve.")

            with open('data.json') as f: data = json.load(f)
            
            # increment new random attributes
            attributes = sample(keys, n_changes)
            abc = [randrange(3) for i in range(n_changes)]
            amount = [choice([-increment, increment]) for i in range(n_changes)]
            
            for i in range(n_changes):
                d = data[attributes[i]][abc[i]]
                data[attributes[i]][abc[i]] = round(d + amount[i], n_dp)  


