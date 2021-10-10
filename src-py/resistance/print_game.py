from agent import Agent
from human import Human
import random, sys, time

class PrintGame:
    '''
    A copy of Game, however the game state is printed throughout play (not afterwards)
    to inform human players.
    '''

    def __init__(self, agents):
        if len(agents)<5 or len(agents)>10:
            raise Exception('Agent array out of range')
        #clone and shuffle agent array
        self.agents = agents.copy()
        random.shuffle(self.agents)
        self.num_players = len(agents)
        #allocate spies
        self.spies = []
        self.humans = []
        while len(self.spies) < Agent.spy_count[self.num_players]:
            spy = random.randrange(self.num_players)
            if spy not in self.spies:
                self.spies.append(spy)
        #start game for each agent        
        for agent_id in range(self.num_players):
            spy_list = self.spies.copy() if agent_id in self.spies else []
            self.agents[agent_id].new_game(self.num_players,agent_id, spy_list)
            if isinstance(self.agents[agent_id], Human): self.humans.append(agent_id)
        #initialise rounds
        self.missions_lost = 0
        self.rounds = []

        print(f"\nNumber of players: {self.num_players}")
        print(f"Humans: {self.humans}\t" +
        f"AIs: {[i for i in range(self.num_players) if i not in self.humans]}")
        
        print(f"Spies: {self.spies}")
        
        for h in self.humans:
            input(f"Press enter to show Player {h} info for 5 seconds:")
            if h in self.spies:
                print(f"Spies: {sorted(self.spies)}\t" +
                f"Resistance: {sorted([i for i in range(self.num_players) if i not in self.spies])}", end='')
                sys.stdout.flush()
                time.sleep(3)
                sys.stdout.write('\r' + ' ' * 100)
                sys.stdout.flush()
            else:
                print("You are Resistance.")
                sys.stdout.flush()
                time.sleep(1)
                sys.stdout.write('\r' + ' ' * 100)
                sys.stdout.flush()

    def play(self):
        leader_id = 0
        for i in range(5):
            r = Round(leader_id,self.agents, self.spies, i)
            self.rounds.append(r)
            if not self.rounds[i].play(): self.missions_lost+= 1
            for a in self.agents:
                a.round_outcome(i+1, self.missions_lost)
            leader_id = (leader_id+len(self.rounds[i].missions)) % len(self.agents)  
            if self.missions_lost == 3 or len(self.rounds) - self.missions_lost == 3:
                break 
        for a in self.agents:
            a.game_outcome(self.missions_lost<3, self.spies) 

        print("\nResistance won\n" if self.missions_lost<3 else "Spies won\n")
        print(f"Spies: {self.spies}") 

class Round():

    def __init__(self, leader_id, agents, spies, rnd):
        self.leader_id = leader_id
        self.agents = agents
        self.spies = spies
        self.rnd = rnd
        self.missions = []   

    def play(self):
        mission_size = Agent.mission_sizes[len(self.agents)][self.rnd]
        fails_required = Agent.fails_required[len(self.agents)][self.rnd]
        while len(self.missions)<5:
            print(f"\nRound: {self.rnd+1}")
            print(f"Leader: {self.leader_id}")
            print(f"Fails required: {fails_required}")
            team = self.agents[self.leader_id].propose_mission(mission_size, fails_required)
            print(f"Mission: {team}")
            mission = Mission(self.leader_id, team, self.agents, self.spies, self.rnd)
            self.missions.append(mission)
            self.leader_id = (self.leader_id+1) % len(self.agents)
            if mission.is_approved():
                return mission.is_successful()

        if len(self.missions) == 5:
            print("\nMission failed")
        
        return mission.is_successful()   

    def is_successful(self):
        return len(self.missions)>0 and self.missions[-1].is_successful()


class Mission():

    def __init__(self, leader_id, team, agents, spies, rnd):
        self.leader_id = leader_id
        self.team = team
        self.agents = agents
        self.spies = spies
        self.rnd = rnd
        self.run()

    def run(self):    
        self.votes_for = [i for i in range(len(self.agents)) if self.agents[i].vote(self.team, self.leader_id)]
        print()
        for i in range(len(self.agents)):
            print(str(i) + (": yes" if i in self.votes_for else ": no"))
        for a in self.agents:
            a.vote_outcome(self.team, self.leader_id, self.votes_for)
        if 2*len(self.votes_for) > len(self.agents):
            self.fails = [i for i in self.team if i in self.spies and self.agents[i].betray(self.team, self.leader_id)]
            success = len(self.fails) < Agent.fails_required[len(self.agents)][self.rnd]
            for a in self.agents:
                a.mission_outcome(self.team,self.leader_id, len(self.fails), success)
            print("\nMission " + ("succeeded" if success else "failed"))
            print(f"Betrayals: {len(self.fails)}")
    
    def is_approved(self):
        return 2*len(self.votes_for) > len(self.agents)

    def is_successful(self):
        return self.is_approved() and len(self.fails) < Agent.fails_required[len(self.agents)][self.rnd]

if __name__ == "__main__":
   from bayes3 import Bayes3
   from baseline import Baseline
   PrintGame([Bayes3() for i in range(4)] + [Human()]).play()