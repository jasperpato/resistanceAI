if __name__ == "__main__":
    from simulation import run
    from random_agent import Random
    from baseline import Baseline
    from bayes import Bayes
    from bayes2 import Bayes2
    from bayes3 import Bayes3
    from learning_bayes import LearningBayes
    import json

    num_games = 2500
    agents    = [Bayes3, LearningBayes]

    data = None
    with open('test_data.json') as f: data = json.load(f)

    run(num_games, agents, data)


