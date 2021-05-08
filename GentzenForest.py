
import logic
from itertools import product
import inferences

# NOTE in disuse
''' 
class MonadicForest:
    and_right_elimination = inferences.MonadicInference('(X and Y)', 'X') 
    and_left_elimination = inferences.MonadicInference('(X and Y)', 'Y')
    not_elimination = inferences.MonadicInference('( not ( not X ) )', 'X')
    
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
            self.inferences.append(inferences.MonadicInference(inference, out))
        else:
            self.inferences.append(inference)
    
    def atomize_forest(self):
        MF = MonadicForest
        for key in self.theorems.copy(): # TODO making a copy is slow
            for inference in self.inferences:
                possible_theorem = inference(self.theorems[key])
                if possible_theorem is not None:
                    self.theorems.update({possible_theorem.formula : possible_theorem})
'''

class NonMonadicGentzenForest:

    and_right_elimination = inferences.NonMonadicInference('(X and Y)', 'X') 
    and_left_elimination = inferences.NonMonadicInference('(X and Y)', 'Y')
    not_elimination = inferences.NonMonadicInference('( not ( not X ) )', 'X')
    implication_elimination = inferences.NonMonadicInference(['(X -> Y)', 'X'], 'Y')
    or_elimination = inferences.NonMonadicInference(['(X or Y)','(X -> Z)','(Y -> Z)'],'Z')
        
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
        if type(inference) is inferences.NonMonadicInference:
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
                

class GentzenForestWithoutSubdedutions(NonMonadicGentzenForest):
    
    and_introduction = inferences.NonMonadicInference(['X','Y'],'(X and Y)')
    inferences = NonMonadicGentzenForest.inferences + [and_introduction]

    def __init__(self, premises):
        super().__init__(premises)
        self.inferences = GentzenForestWithoutSubdedutions.inferences























