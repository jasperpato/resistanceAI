from random_agent import *
from human import *
from game import *

agents = [HumanAgent(name='h0'), 
        RandomAgent(name='r1'),  
        RandomAgent(name='r2'),  
        RandomAgent(name='r3'),  
        RandomAgent(name='r4')]

game = Game(agents)
game.play()
print(game)


