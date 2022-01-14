import itertools
import numpy as np

ids = ["318295029", "316327451"]


""" state:
    drone_loc
    number of packages the drone is holding
    for every drone that we are not holding it's location
"""

""""Q_table:
    states / actions
"""

class DroneAgent:
    def __init__(self, n, m):
        self.mode = 'train'  # do not change this!
        # your code here
        self.Q_table = {}
        self.possible_actions = ('reset', 'wait', 'pick', 'move_up', 'move_down', 'move_left','move_right', 'deliver')
        self.possible_drone_locations = list(itertools.product(range(n), range(m)))
        self.package_num = (0, 1, 2) # possible number of packages that can be carried by the drone
        self.mu = 0
        self.sigma = 2
        self.steps = 0
        self.alpha = 0.1 # learning rate of the model
        self.gamma = 0.90 # discount factor
        self.epsilon = 0.5
        self.start_epsilon_decaying = 1
        self.end_epsilon_decaying = int(200e3)*15
        self.epsilon_decay_value = self.epsilon/ (self.end_epsilon_decaying - self.start_epsilon_decaying)

    def select_action(self, obs0):
        drone_location = obs0['drone_location']

        numbers_of_carried_packages = 0
        unlifted_packages_loc = []
        for package, loc in obs0['packages']:
            if loc == 'drone':
                numbers_of_carried_packages += 1
            else:
                unlifted_packages_loc.append(loc)
        current_state = (drone_location, numbers_of_carried_packages, tuple(sorted(unlifted_packages_loc)))


        if current_state not in self.Q_table:
            # TODO: give to a state only possible actions as far as we know
            # TODO: if we cannot move in a certain direction for a long time we set the value to -infinity
            self.Q_table[current_state] = {}
            for action in self.possible_actions:
                self.Q_table[current_state][action] = np.random.uniform(0, 1)


        ##################### Selecting action #################################
        if np.random.uniform(0, 1) > self.epsilon: # choosing a greedy action
            out = sorted(list(self.Q_table[current_state].items()), key=lambda x: x[1])
            action_to_take = out[-1][0]
        else: # choosing an explorative action
            num = np.random.randint(0, len(self.possible_actions))
            action_to_take = self.possible_actions[num]


        self.steps += 1
        if self.end_epsilon_decaying >= self.steps >= self.start_epsilon_decaying:
            self.epsilon -= self.epsilon_decay_value
        return action_to_take

    def train(self):
        self.mode = 'train'  # do not change this!

    def eval(self):
        self.mode = 'eval'  # do not change this!

    def update(self, obs0, action, obs1, reward):
        drone_location_0 = obs0['drone_location']
        numbers_of_carried_packages_0 = 0
        unlifted_packages_loc_0 = []
        for package, loc in obs0['packages']:
            if loc == 'drone':
                numbers_of_carried_packages_0 += 1
            else:
                unlifted_packages_loc_0.append(loc)
        s = (drone_location_0, numbers_of_carried_packages_0, tuple(sorted(unlifted_packages_loc_0)))

        drone_location_1 = obs1['drone_location']
        numbers_of_carried_packages_1 = 0
        unlifted_packages_loc_1 = []
        for package, loc in obs1['packages']:
            if loc == 'drone':
                numbers_of_carried_packages_1 += 1
            else:
                unlifted_packages_loc_1.append(loc)
        s_tag = (drone_location_1, numbers_of_carried_packages_1, tuple(sorted(unlifted_packages_loc_1)))


        if s_tag not in self.Q_table:
            self.Q_table[s_tag] = {}
            for act in self.possible_actions:
                self.Q_table[s_tag][act] = np.random.uniform(0, 1)

        ###### finding max Q value of actions in s_tag state
        out = sorted(list(self.Q_table[s_tag].items()), key=lambda x: x[1])
        max_q_val = out[-1][1]

        ###### updating Q table of state s and action ######################
        self.Q_table[s][action] = (1-self.alpha)*self.Q_table[s][action] + self.alpha*(reward + self.gamma*max_q_val)