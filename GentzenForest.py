
from generic_trees import GenericTree
import logic

#TODO add exception handling


class MonadicInference:
    # if out_scheme is None it means that the MonadicInference only will be used
    # to check if formulas follow schemes
    def __init__(self, in_scheme, out_scheme = None): # arguments are natural formulas

        self.in_scheme = in_scheme
        self.in_tree_scheme = logic.Tree(self.in_scheme)
        self.out_scheme = out_scheme
        self.out_tree_scheme = logic.Tree(self.out_scheme) if out_scheme is not None else None
   
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
  
    def get_applied_schemes_map(self, formula_tree):
        aux = {}
        if self._follows_the_scheme(self.in_tree_scheme, formula_tree, aux):
            return aux

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
        if applied is not None:
            return self.apply_out_scheme(applied) 

    def __repr__(self):
        return self.in_scheme + '  |-  ' + self.out_scheme


class NonMonadicInference:
    # premises is a set in natural form, conclusion is a formula in natural form
    def __init__(self, premises, conclusion): 
        self.monadic_inferences = []
        for premise in premises:
            self.monadic_inferences.append(MonadicInference(premise))
        
        self.conclusion_tree = logic.Tree(conclusion)

    def get_maps_from_inferences(self, formula_trees):
        maps = []
        for inference, tree_to_map in zip(self.monadic_inferences, formula_trees):
            aux_map_to_append = inference.get_applied_schemes_map(tree_to_map)
            maps.append(aux_map_to_append)

        return maps
    
    def maps_are_coherent(self, maps): # TODO algorithm too slow
        aux_map = {}
        for _map in maps:
            for elem in _map:
                if elem in aux_map:
                    if _map[elem].formula != aux_map[elem].formula:
                        return False
                aux_map.update({elem : _map[elem]})
        return True



    #final step of the algorithm
    def apply_inferences_from_maps(self, maps):
        if self.maps_are_coherent(maps):
            aux_str = self.conclusion_tree.formula
            for _map in maps:
                for elem in _map:
                    aux_str = aux_str.replace(elem, _map[elem].formula)

            return logic.Tree(aux_str)

    def __call__(self, trees): # trees is an list or set of logic.Tree's
        maps = self.get_maps_from_inferences(trees) 
        return self.apply_inferences_from_maps(maps) 
        # TODO handle exceptions of wrong trees 

premises = {'(X -> Y)', 'X'}
conclusion = 'Y'
implication_elimination = NonMonadicInference(premises, conclusion)

t1 = logic.Tree('(( not p ) -> (q and r))')
t2 = logic.Tree('( not q )')
deduction = implication_elimination([t1, t2]) 


    




   

################## WORKS FINE :) #########################################
#morgan = MonadicInference('( not (X or Y) )','(( not X ) and ( not Y ))') 
#example_tree = logic.Tree('( not ((p -> q) or (q and (p and q))) )')
#example_tree.print_each_node()
#print('----')
#conclusion = morgan(example_tree)
#conclusion.print_each_node()

# TODO should be an lists (or sets) generalization for "MonadicInference" class
#class Inference:   
#    def __init__(self, in_squemes, out_squemes):
#        self.in_squemes = in_squemes
#        self.out_squemes = out_squemes
#        self.calc_squemes_logic_trees()
#
#    def calc_squemes_logic_trees(self):
#        self.in_squeme_trees = {}
#        self.out_squeme_trees = {}
#        for squeme in self.in_squemes:
#            self.in_squeme_trees.update({squeme : logic.Tree(squeme)})
#        for squeme in self.out_squemes:
#            self.out_squeme_trees.update({squeme : logic.Tree(squeme)})
#    
#
#    def __call__(self, inputs):
#        if self.follows_the_squeme(inputs):
#            return self.output_squeme

class GentzenForest:  
    def __init__(self, premises): # premises is a set of trees
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


class MonadicForest:
    and_right_elimination = MonadicInference('(X and Y)', 'X') 
    and_left_elimination = MonadicInference('(X and Y)', 'Y')
    not_elimination = MonadicInference('( not ( not X ) )', 'X')
     
    inferences = [
            and_right_elimination,
            and_left_elimination,
            not_elimination
            ]

    def __init__(self, premises):
        if type(premises) is not logic.Premises:
            premises = logic.Premises(premises)

        self.premises = premises.get_set()
        self.premises = {tree.formula : tree for tree in self.premises}
        self.theorems = self.premises.copy()
        self.inferences = MonadicForest.inferences
    
    def get_theorems(self):
        return self.theorems

    def print_theorems(self):
        for key in self.theorems:
            print(key)
    
    def get_inferences(self):
        return self.inferences

    def print_inferences(self):
        for inference in self.inferences:
            print(inference)

    def add_inference(self, inference, out = None):  
        if out is not None:
            self.inferences.append(MonadicInference(inference, out))
        else:
            self.inferences.append(inference)
    
    def atomize_forest(self):
        MF = MonadicForest
        for key in self.theorems.copy(): # TODO making a copy is slow
            for inference in self.inferences:
                possible_theorem = inference(self.theorems[key])
                if possible_theorem is not None:
                    self.theorems.update({possible_theorem.formula : possible_theorem})



###################### TODO TODO TODO TODO 
#TODO make an interface that would allow to add manually general theorems (like inference rules)
# TODO every inference rule should be alien to the theorems generator,
# make an interface for that





















