Our two final Resistance agents are the Bayesian agents Bayes3 and Evolved.

Bayes3 is hard-coded with our best estimates of behavioural patterns. Evolved is
hard-coded with values that were achieved through 900 genetic trails of 7500
games each (6,750,000 games). See genes.json for a list of the trait values.

To view the results from 10,000 games between Bayes3, Evolved, as well as our
Baseline and Random agents:
> py run.py

To perform more genetic trials on the data stored in genes.json:
> py genetics.py

To play against a random selection of Bayes3 and Evolved agents as a human:
> py print_game.py

To view a random game between Bayes3, Evolved, Baseline and Random agents:
> py game.py