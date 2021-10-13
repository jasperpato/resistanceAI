if __name__ == "__main__":
    from learning_bayes import LearningBayes
    from bayes3 import Bayes3
    from learning_bayes import LearningBayes
    from random import randrange, choice, sample
    import json
    from run import run

    trials    = 100
    games     = 1000
    changes   = 3
    increment = 0.02
    dp        = 2     # decimal places of data
    chances_to_improve = 5
    agents = [LearningBayes, Bayes3]

    with open('data.json') as f: data = json.load(f)
    old_win_rate = data["win_rate"]
    keys = list(data.keys())
    keys.remove("win_rate")
    attributes = sample(keys, changes)

    abc = [randrange(changes) for i in range(3)]
    amount = [choice([-increment, increment]) for i in range(changes)]
    for i in range(changes): data[attributes[i]][abc[i]] += amount[i]
    for k in keys:
        for i in range(3): data[k][i] = round(data[k][i], dp)

    did_not_improve_count = 0

    for i in range(trials):
        print(f'\nTrial {i+1}\n')
        new_win_rate = run(games, agents, data)
        if new_win_rate > data["win_rate"]: 
            print("Improved.")
            did_not_improve_count = 0
            
            # update data
            data["win_rate"] = round(new_win_rate, 4)
            with open("data.json", 'w') as f: json.dump(data, f, indent=2)
            
            # increment same values again
            for i in range(changes): data[attributes[i]][abc[i]] += amount[i]
            for k in keys:
                for i in range(3): data[k][i] = round(data[k][i], dp)       
        else:
            print("Did not improve.")
            did_not_improve_count += 1

            if did_not_improve_count == chances_to_improve:
                print("Reverting changes")
                # revert changes
                with open('data.json') as f: data = json.load(f)
                #for i in range(changes): data[attributes[i]][abc[i]] -= amount[i]

                did_not_improve_count = 0
            
            # increment new random numbers
            attributes = sample(keys, changes)
            abc = [randrange(changes) for i in range(changes)]
            amount = [choice([-increment, increment]) for i in range(changes)]

            for i in range(changes): data[attributes[i]][abc[i]] += amount[i]
            for k in keys:
                for i in range(3): data[k][i] = round(data[k][i], dp)


