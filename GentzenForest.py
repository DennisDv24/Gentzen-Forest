
from generic_trees import GenericTree
import logic

class MonadicInference:
    def __init__(self, in_scheme, out_scheme): # arguments are translated formulas

        self.in_scheme = in_scheme
        self.in_tree_scheme = logic.Tree(self.in_scheme)
        self.out_scheme = out_scheme
        self.out_tree_scheme = logic.Tree(self.out_scheme)
   
    def _follows_the_scheme(self, scheme, tree, applied_schemes = {}): # (scheme, tree) are trees
        if logic.Formulas.is_atom(scheme.formula): 
            applied_schemes.update({scheme.formula : tree})
            return True

        if scheme.value in logic.Formulas.binary_connectors:
            if scheme.value == tree.value:
                l = self._follows_the_scheme(scheme.left, tree.left, applied_schemes)
                r = self._follows_the_scheme(scheme.right, tree.right, applied_schemes)
                return l and r
                    
            else: return False
        
        elif scheme.value in logic.Formulas.dyadic_connectors:
            if scheme.value == tree.value:
                return self._follows_the_scheme(scheme.left, tree.left, applied_schemes)
            else: return False

    def follows_the_scheme(self, formula_tree):
        return self._follows_the_scheme(self.in_tree_scheme, formula_tree)
        
    def apply_in_scheme(self, formula_tree):
        applied_schemes_map = {}
        if self._follows_the_scheme(self.in_tree_scheme, formula_tree, applied_schemes_map):
            return applied_schemes_map
   
    def apply_out_scheme(self, applied_map):
        aux_str = self.out_tree_scheme.formula
        for elem in applied_map:
            aux_str = aux_str.replace(elem, applied_map[elem].formula)

        return logic.Tree(aux_str)

    def __call__(self, formula_tree): 
        applied = self.apply_in_scheme(formula_tree)
        return self.apply_out_scheme(applied)

morgan = MonadicInference('( not (X or Y) )','(( not X ) and ( not Y ))')
example_tree = logic.Tree('( not ((p -> q) or (q and (p and q))) )')
example_tree.print_each_node()
print('----')
conclusion = morgan(example_tree)
conclusion.print_each_node()

class Inference:
    def __init__(self, in_squemes, out_squemes):
        self.in_squemes = in_squemes
        self.out_squemes = out_squemes
        self.calc_squemes_logic_trees()

    def calc_squemes_logic_trees(self):
        self.in_squeme_trees = {}
        self.out_squeme_trees = {}
        for squeme in self.in_squemes:
            self.in_squeme_trees.update({squeme : logic.Tree(squeme)})
        for squeme in self.out_squemes:
            self.out_squeme_trees.update({squeme : logic.Tree(squeme)})
    

    def __call__(self, inputs):
        if self.follows_the_squeme(inputs):
            return self.output_squeme

#implication_elimination = Inference(['(X -> Y)', 'X'], 'Y') # inference squeme
#keys = ['( ( not p ) -> ' + t.formula + ' ) ', '( not p )'] # example
#                        # type(t) is logic.Treee
#self.theorems.update(Inference(keys)) # apply the inference for specific formule
#            # new theorem would be added: 't.formula'

class GentzenForest: 
    def __init__(self, premises):
        if type(premises) is not set():
            premises = set(premises)
        self.premises = premises
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

