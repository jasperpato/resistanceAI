import unittest
from baseline import BaselineAgent
from itertools import combinations

class TestBaseline(unittest.TestCase):

    def print_(self, worlds):
        s = "{"
        for i, (k, v) in enumerate(worlds.items()):
            s += str(k) + ": " + str(round(v,4))
            if i != len(worlds)-1: s += ", "
        print(s+'}')

    def test_mission_outcome(self):
        b = BaselineAgent("b0")
        num_players = 5
        
        for s in [2,3]:
            for mission in combinations(range(5), s):
                for betrayals in [0,1,2]:
                    b.new_game(num_players, 0, [])
                    b.vote_outcome(mission, 1, range(num_players))
                    b.mission_outcome(mission, 1, betrayals, betrayals == 0)

                    print(f"Mission: {mission}, betrayals: {betrayals}")
                    self.print_(b.worlds)
                    print(round(sum([w[1] for w in b.worlds.items()]),3))
                    print()

TestBaseline().test_mission_outcome()