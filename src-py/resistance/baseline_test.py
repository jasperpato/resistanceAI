import unittest
from baseline import BaselineAgent

class TestBaseline(unittest.TestCase):

    def print_(self, worlds):
        s = "{"
        for i, (k, v) in enumerate(worlds.items()):
            s += str(k) + ": " + str(round(v,4))
            if i != len(worlds)-1: s += ", "
        print(s+'}')

    def test_mission_outcome(self):
        b = BaselineAgent("b0")
        for num_players in range(5, 11):
            b.new_game(num_players, 0, [])

            self.print_(b.worlds)
            print(round(sum([w[1] for w in b.worlds.items()])),3)

            mission = [0,1,2]
            leader = 1
            betrayals = 1

            b.vote_outcome([0,1,2], leader, range(num_players))
            b.mission_outcome(mission, leader, betrayals, betrayals == 0)

            self.print_(b.worlds)
            print(round(sum([w[1] for w in b.worlds.items()]),3))

TestBaseline().test_mission_outcome()