
import random
import heapq
import math
import sys
from collections import defaultdict, deque, Counter
from itertools import combinations

from src.components.place import Zone
class Problem(object):

    def __init__(self, initial=None, goal=None, **kwds): 
        self.__dict__.update(initial=initial, goal=goal, **kwds) 
        
    def actions(self, state):        raise NotImplementedError
    def result(self, state, action): raise NotImplementedError
    def is_goal(self, state):        return state == self.goal
    def action_cost(self, s, a, s1): return 1
    def h(self, node):               return 0
    
    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)
    

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '<{}>'.format(self.state)
    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))
    def __lt__(self, other): return self.path_cost < other.path_cost
    
    
failure = Node('failure', path_cost=math.inf)
cutoff  = Node('cutoff',  path_cost=math.inf)
    
    
def expand(problem: Problem, node: Node):
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)

def path_actions(node: Node):
    if node.parent is None:
        return []  
    return path_actions(node.parent) + [node.action]


def path_states(node: Node):
    if node in (cutoff, failure, None): 
        return []
    return path_states(node.parent) + [node.state]

FIFOQueue = deque

LIFOQueue = list

class PriorityQueue:

    def __init__(self, items=(), key=lambda x: x): 
        self.key = key
        self.items = [] # a heap of (score, item) pairs
        for item in items:
            self.add(item)

    def add(self, item):
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        return heapq.heappop(self.items)[1]
    
    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)

def is_cycle(node: Node, k=30):
    def find_cycle(ancestor, k):
        return (ancestor is not None and k > 0 and
                (ancestor.state == node.state or find_cycle(ancestor.parent, k - 1)))
    return find_cycle(node.parent, k)

def best_first_search(problem:Problem, f):
    node = Node(problem.initial)
    frontier = PriorityQueue([node], key=f)
    reached = {problem.initial: node}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return failure

def best_first_tree_search(problem, f):
    frontier = PriorityQueue([Node(problem.initial)], key=f)
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            if not is_cycle(child):
                frontier.add(child)
    return failure

def g(n:Node): return n.path_cost

def astar_tree_search(problem:Problem, h=None):
    h = h or problem.h
    return best_first_tree_search(problem, f=lambda n: g(n) + h(n))


def weighted_astar_search(problem:Problem, h=None, weight=1.4):
    h = h or problem.h
    return best_first_search(problem, f=lambda n: g(n) + weight * h(n))

# Define Problems Below
