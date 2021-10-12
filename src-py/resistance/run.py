if __name__ == "__main__":
    from simulation import run
    from random_agent import Random
    from baseline import Baseline
    from bayes import Bayes
    from bayes2 import Bayes2
    from bayes3 import Bayes3
    from learning_bayes import LearningBayes
    import json

    s = 2500
    agents = [LearningBayes]

    with open('data.json') as f: data = json.load(f)
    run(s, agents, data)


