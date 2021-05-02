class Alphabet:
    def __init__(self, atoms, dyadics_connectors, monadic_connectors, parenthesis):
        self.atoms = atoms
        self.dyadics_connectors = dyadics_connectors
        self.monadic_connectors = monadic_connectors
        self.parenthesis = parenthesis

class System:
    def __init__(self, A, F, X, R):
        self.alphabet = A
        self.well_formed_strings = F # is a recursive function
        self.axioms = X
        self.inference_rules = R

class Gentzen:
    atoms = ['p', 'q', 'r', 's', 't']
    open_parenthesis = ['(','{','[']
    closed_parenthesis = [')','}',']']

    dyadic_connectors = ['&','|','>']
    natural_dyadic_connectors = ['and','or','->']
    monadic_connectors = ['!']
    natural_monadic_connectors  = ['not']

                
    connector_translator = dict(zip(
        natural_dyadic_connectors + natural_monadic_connectors,
        dyadic_connectors + monadic_connectors))

    def translate_char(c):
        if (c in Gentzen.atoms
        or c in Gentzen.open_parenthesis
        or c in Gentzen.closed_parenthesis): 
               return c
        return Gentzen.connector_translator[c]
        
    def translate_string(c):
        out = ''
        for elem in c.split():
            if elem in Gentzen.connector_translator:
                out += Gentzen.connector_translator[elem]
            else:
                out += elem
    
        return out


    def is_well_formed(string):    
        string = Gentzen.translate_string(string)

        def recursive_comprobation(string):
            if string in Gentzen.atoms: return True
            elif string[0] in Gentzen.monadic_connectors:
                if len(string) > 1:
                    return recursive_comprobation(string[1:])
                else: 
                    return False

            last_i = len(string) - 1
            if (string[0] == '(' and string[last_i] == ')'):
                string = string[1:last_i]
                left_subformule = ''
                right_subformule = ''
                
                if string[0] in Gentzen.monadic_connectors:
                    return recursive_comprobation(string)
                
                aux_stack = []
                for i in range(len(string)):
                    if string[i] == '(':
                        aux_stack.append(0)
                    elif string[i] == ')' and len(aux_stack) > 0:
                        aux_stack.pop()
                    
                    if (string[i] in Gentzen.dyadic_connectors 
                    and len(aux_stack) == 0):
                        left_subformule = string[:i]
                        right_subformule = string[i+1:]
                        return (recursive_comprobation(left_subformule)
                           and recursive_comprobation(right_subformule))


            else: return False

        return recursive_comprobation(string)
            

                    




















