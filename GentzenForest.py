
from generic_trees import GenericTree
import logic

class Premises:
    def __init__(self, premises = []): # the premises can be logic.Tree's or natural strings
        self.set = set()
        for premise in premises:
            self.append(premise)

    def __repr__(self):
        return repr(self.set)

    def get_set(self):
        return self.set

    def append(self, premise):
        if type(premise) is logic.Tree:
            self.set.add(premise)
        elif type(premise) is str:
            self.set.add(logic.Tree(premise))

class GentzenForest: 
    def __init__(self, Premises):
        self.premises = Premises.get_set()
        self.theorems = set()

# TODO, actually i cant check if an tree is already in a set
# this was the main reason to using sets: checking if an theorem was already proofed
# with O(1) ("therem is in self.theorems"). To fix this i must expand
# the structure to store the strings in natrual form. 
# The best way to do this is with a new attribute to the node class (logic.Tree):
#   self.natural_form
#   -----------------

