
from generic_trees import GenericTree
import logic
from itertools import product

class MonadicInference:
    # if out_scheme is None it means that the MonadicInference only will be used
    # to check if formulas follow schemes
    def __init__(self, in_scheme, out_scheme = None): # arguments are natural formulas

        self.in_scheme = in_scheme
        self.in_tree_scheme = logic.Tree(self.in_scheme)
        self.out_scheme = out_scheme
        self.out_tree_scheme = logic.Tree(self.out_scheme) if out_scheme is not None else None

    # (scheme, tree) are trees
    def _follows_the_scheme(self, scheme, tree, applied_schemes = {}): 
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
    
    def get_in_scheme(self):
        return self.in_scheme

    def __repr__(self):
        return self.in_scheme + '  |-  ' + self.out_scheme


# TODO TODO TODO
#   The non monadic inferences work only if the input is ordered.
#   Should work with an set as an input, but the order matters
class NonMonadicInference:  
    # premises is a list of formulas or a formula in natural form
    # conclusion is a formula in natural form
    def __init__(self, premises, conclusion): 
        if type(premises) is str:
            premises = [premises]

        self.monadic_inferences = []
        for premise in premises:
            self.monadic_inferences.append(MonadicInference(premise))
        
        self.conclusion_tree = logic.Tree(conclusion)

    def get_monadic_inferences(self):
        return self.monadic_inferences

    # FIXME before updating te maps check if the key is already and try to update the maps logically
    # REF to the last TODO
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
    
    def apply_inferences_from_maps(self, maps):
        if self.maps_are_coherent(maps):
            aux_str = self.conclusion_tree.formula
            for _map in maps:
                for elem in _map:
                    aux_str = aux_str.replace(elem, _map[elem].formula)

            return logic.Tree(aux_str)
    
    def __call__(self, trees): # trees is an list of logic.Trees or an logic.Tree
        if type(trees) is logic.Tree:
            trees = [trees]
        if len(trees) == len(self.monadic_inferences):
            maps = self.get_maps_from_inferences(trees) 
            return self.apply_inferences_from_maps(maps) # returns an tree

    def __repr__(self):
        out_str = '{ '
        for monadic_inference in self.monadic_inferences:
            out_str += monadic_inference.get_in_scheme() + ', '

        out_str = out_str[:len(out_str)-2] + ' } |- '
        out_str += self.conclusion_tree.formula
        return out_str
        
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

class NonMonadicGentzenForest:

    and_right_elimination = NonMonadicInference('(X and Y)', 'X') 
    and_left_elimination = NonMonadicInference('(X and Y)', 'Y')
    not_elimination = NonMonadicInference('( not ( not X ) )', 'X')
    implication_elimination = NonMonadicInference(['(X -> Y)', 'X'], 'Y')
    or_elimination = NonMonadicInference(['(X or Y)','(X -> Z)','(Y -> Z)'],'Z')
        
    inferences = [
            and_right_elimination, 
            and_left_elimination, 
            not_elimination,
            implication_elimination,
            or_elimination
            ]

    def __init__(self, premises):
        if type(premises) is not logic.Premises:
            premises = logic.Premises(premises)

        self.premises = premises.get_set()
        self.premises = {tree.formula : tree for tree in self.premises}
        self.theorems = self.premises.copy()
        self.inferences = NonMonadicGentzenForest.inferences

    def get_theorems(self):
        return self.theorems

    def print_theorems(self):
        for key in self.theorems:
            print(key)
    
    def get_inferences(self):
        return self.inferences
    
    def add_inference(self, inference):
        if type(inference) is NonMonadicInference:
            self.inferences.append(inference)

    def print_inferences(self):
        for inference in self.inferences:
            print(inference)

    
    def get_matrix_of_keys_that_follow_the_schemes(self, inference):
        keys_that_follow_the_schemes = []
        monadic_inferences = inference.get_monadic_inferences()
        for i in range(len(monadic_inferences)):
            keys_that_follow_the_schemes.append([])
            for key in self.theorems: # possible copy?
                if monadic_inferences[i].follows_the_scheme(self.theorems[key]):
                    keys_that_follow_the_schemes[i].append(self.theorems[key])
                    
        return keys_that_follow_the_schemes
    
    def get_all_combinations_from_keys(self, keys_matrix):
        return list(product(*keys_matrix))

    def try_to_apply_inference(self, inference):
        matrix_of_keys_to_combine = self.get_matrix_of_keys_that_follow_the_schemes(inference)
        combinations_of_keys = self.get_all_combinations_from_keys(matrix_of_keys_to_combine)

        for combination in combinations_of_keys:
            possible_theorem = inference(combination)
            if possible_theorem is not None:
                self.theorems.update({possible_theorem.formula : possible_theorem})



    def apply_inferences_in_order(self, iterations = 1):
        for i in range(iterations):
            for inference in self.inferences:
                self.try_to_apply_inference(inference) 
                

