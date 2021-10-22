Jasper Paterson 22736341 
Jordan Hartley 22713786 

Our two final Resistance agents we are submitting are Bayes3 and Evolved.

Bayes3 is hard-coded with our best estimates of behavioural patterns. Evolved is
hard-coded with values that were achieved through 900 genetic trails of 7500
games each (6,750,000 games). See genes.json for a list of the trait values.

To view the results from n games between Bayes3, Evolved, as well as our
Baseline and Random agents:
> python3 run.py n

To view the results from the current Evolver agent (genes taken from the latest
genes.json) against the other agents:
> python3 run.py compare n

To perform more genetic trials on the data stored in genes.json:
> python3 genetics.py

To view a random game between Bayes3, Evolved, Baseline and Random agents:
> python3 game.py