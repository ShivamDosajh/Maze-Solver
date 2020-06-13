import random
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            return None
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            pass
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class PQ_Entry:
    def __init__(self,state, action, parent, priority):
        self.state = state
        self.action = action
        self.parent = parent
        self.priority = priority


class PriorityQueue:
    def __init__(self):
        self.frontier = []
    def isEmpty(self):
        return len(self.frontier) == 0
    def __len__(self):
        return len(self.frontier)
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    def add(self,node):
        self.frontier.append(node)
        i = len(self.frontier) -1
        while i >= 0:
            if i >=1:
                if self.frontier[i].priority < self.frontier[i-1].priority:
                    self.frontier[i],self.frontier[i-1] = self.frontier[i-1], self.frontier[i]
                    i -= 1
                else:
                    break
            if i == 0:
                break
    def remove(self):
        if self.isEmpty():
            pass
        else:
            node = self.frontier[0]
            self.frontier.pop(0)
            return node
