# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """

        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.tempvalues = self.values.copy()
        # Write value iteration code here
        #print "start location ", mdp.getStates()
        "*** YOUR CODE HERE ***"
        for i in xrange(0,self.iterations):
            for allstate in mdp.getStates():
                if not mdp.isTerminal(allstate):
                    value=[]
                    for possibleaction in mdp.getPossibleActions(allstate):
                        statevalue = 0
                        statevalue = statevalue + self.computeQValueFromValues(allstate,possibleaction)
                        value.append(statevalue)
                    self.tempvalues[allstate]=max(value)
            self.values = self.tempvalues.copy()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        if action == 'exit' :
            return self.mdp.getReward(state,action,'TERMINAL_STATE')
        Q = 0

        for transition in self.mdp.getTransitionStatesAndProbs(state,action):
            # Q = Q +  self.mdp.getReward(state,action,transition[0]) + self.discount*transition[1]*self.getValue(transition[0])
            # I dont have to add getRewards because all the state here has reward 0
            Q = Q + self.discount * transition[1] * self.getValue(transition[0])
        return Q
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = util.Counter()
        if self.mdp.isTerminal(state):
            return None
        for action in self.mdp.getPossibleActions(state):
            actions[action]=self.computeQValueFromValues(state,action)
        return actions.argMax()
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
