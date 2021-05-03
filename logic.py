
from generic_trees import GenericTree

class Formulas:

    natural_connectors = ['not','and','or','->']
    connectors = ['!','&','|','>']
    connectors_translator = dict(zip(natural_connectors, connectors))


    def translate_string(string): # it assumes that string is well formed
        out = ''
        for elem in string.split():
            if elem in Formulas.connectors_translator:
                out += Formulas.connectors_translator[elem]
            else:
                out += elem
        return out

    def get_binary_components(phi): # it assumes that phi is translated and well formed
        l = len(phi) - 1
        if phi[0] == '(' and phi[l] == ')':
            phi = phi[1:l]
            aux_stack = []
            for i in range(l):
                if phi[i] == '(':
                    aux_stack.append(0)
                elif phi[i] == ')' and len(aux_stack) > 0:
                    aux_stack.pop()

                if phi[i] in Formulas.connectors and len(aux_stack) == 0:
                    return (phi[:i],phi[i],phi[i+1:])
        else: return False

class Tree(GenericTree):
    
    def __init__(self, premise, is_natural = True): # it assumes that the premise is natural and well formed
        self.value = None
        self.left = None # main
        self.right = None
        
        if is_natural:
            premise = Formulas.translate_string(premise)
        self.translate_to_tree(premise)

    def translate_to_tree(self, premise): # it assumes that the premise is translated and well formed 
        if premise[0] == '(':
            if premise[1] == '!': # is negation
                self.value = '!'
                self.left = Tree(premise[2:len(premise)-1])

            else: # is binary
                components = Formulas.get_binary_components(premise)
                self.value = components[1]
                self.left = Tree(components[0], is_natural = False)
                self.right = Tree(components[2], is_natural = False)

        else: # is atom
            self.value = premise



