
from generic_trees import GenericTree
import logic

class GentzenForest: 
    def __init__(self, premises):
        if type(premises) is not logic.Premises:
            premises = logic.Premises(premises)
        self.premises = premises.get_set()
        self.premises = {tree.formula : tree for tree in self.premises}
        self.theorems = self.premises.copy()

    def get_premises(self):
        return self.premises
   
    def get_theorems(self):
        return self.theorems

    def print_premises(self):
        for elem in self.premises:
            print(elem)

    def print_theorems(self):
        for elem in self.theorems:
            print(elem)
   
    def not_and_tree_atomization(self, key):
        if not logic.Formulas.is_atom(key):
            t = self.theorems[key]
            if t.value == t.left.value == '!':
                t = t.left.left
                self.theorems.update({t.formula : t})
                self.not_and_tree_atomization(t.formula)
            elif t.value == '&':
                self.theorems.update({t.left.formula : t.left})
                self.theorems.update({t.right.formula : t.right})
                self.not_and_tree_atomization(t.left.formula)
                self.not_and_tree_atomization(t.right.formula)
    
    def implication_forest_atomization(self):
        for key in self.theorems.copy(): # TODO provisional .copy(), should be a easier way
            t = self.theorems[key]
            if t.value == '>':
                if t.left.formula in self.theorems:
                    self.theorems.update({t.right.formula : t.right})


    def search_for_or_possible_atomization(self, key1, key2): # TODO too slow, could be better
        for i in self.theorems.copy():
            t1 = self.theorems[i]
            if t1.value == '>' and t1.left.formula == key1:
                for j in self.theorems.copy():
                    t2 = self.theorems[j]
                    if t2.value == '>' and t2.left.formula == key2:
                        if t1.right.formula == t2.right.formula:
                            self.theorems.update({t1.right.formula : t1.right})


    def or_forest_atomization(self):
        for key in self.theorems.copy(): # TODO, ref implication_forest_atomization
            t = self.theorems[key]
            if t.value == '|':
                self.search_for_or_possible_atomization(t.left.formula, t.right.formula)



    def atomize_forest(self, iterations = 10): # deduce all possible theorems from elimination rules
        for i in range(iterations): # TODO this should be changed to an inteligent while
            for key in self.theorems.copy(): # TODO implication_forest_atomizatio
                self.not_and_tree_atomization(key)
            self.implication_forest_atomization()
            self.or_forest_atomization()

class GentzenHardcoreForest(GentzenForest):
    # new inferences for extensions (infinite (and redundant) theorems machine)
    pass


#TODO make an interface that would allow to add manually general theorems (like inference rules)
# TODO every inference rule should be alien to the theorems generator,
# make an interface for that

