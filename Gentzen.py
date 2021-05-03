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
    connectors = monadic_connectors + dyadic_connectors

                
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

    
    def get_binary_components(phi):
        l = len(phi) - 1
        if phi[0] == '(' and phi[l] == ')':
            phi = phi[1:l]
            aux_stack = []
            for i in range(l):
                if phi[i] == '(':
                    aux_stack.append(0)
                elif phi[i] == ')' and len(aux_stack) > 0:
                    aux_stack.pop()

                if phi[i] in Gentzen.connectors and len(aux_stack) == 0:
                    return (phi[:i],phi[i],phi[i+1:])
        else: return False

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


    def and_introduction(phi, psi):
        return '(' + phi + '&' + psi + ')'
    
    def and_right_elimination(phi):
        components = Gentzen.get_binary_components(phi)
        if components[1] == '&':
            return components[0]
        else: return False
    def and_left_elimination(phi):
        components = Gentzen.get_binary_components(phi)
        if components[1] == '&':
            return components[2]
        else: return False
    
    def or_right_introduction(premise, formule_to_introduce):
        return '(' + premise + '|' + formule_to_introduce + ')'
    def or_left_introduction(premise, formule_to_introduce):
        return '(' + formule_to_introduce + '|' + premise + ')'
   
    def or_elimination(premise, implication1, implication2):
        phi, _or, psi = Gentzen.get_binary_components(premise)
        if _or == '|':
            i1 = Gentzen.get_binary_components(implication1)
            i2 = Gentzen.get_binary_components(implication2)
            
            if i1[1:] == i2[1:] and ((phi == i1[0] and psi == i2[0]) or
                    (phi == i2[0] and psi == i1[0])):
                return i1[2]

        return False

    def not_introduction(implication1, implication2): # reductio ad absurdum: difficult to compute
        phi1, im1, psi = Gentzen.get_binary_components(implication1)
        phi2, im2, not_psi = Gentzen.get_binary_components(implication2)

        if phi1 == phi2 and im1 == im2 and not_psi[1:] == psi:
            return '!' + phi1
        else: return False

    def not_elimination(premise):
        return premise[2:] if premise[0] == '!' == premise[1] else False
    
    def implication_introduction(aux_premise):
        # premises.append(aux_premise)
        # return aux_premise -> phi
        # where phi is any new formule generated with the new premises
        pass # difficult to compute

    def implication_elimination(phi, implication):
        aux_phi, im, psi = Gentzen.get_binary_components(implication)
        return psi if aux_phi == phi and im == '>' else False

    rules = [and_introduction,
             and_right_elimination,
             and_left_elimination,
             or_right_introduction,
             or_left_introduction,
             or_elimination,
             not_introduction,
             not_elimination,
             implication_introduction,
             implication_elimination]
    
    ez_rules = [and_introduction,
                and_right_elimination,
                and_left_elimination,
                or_right_introduction,
                or_left_introduction,
                or_elimination,
                not_elimination,
                implication_elimination]

    ezez_rules = [and_introduction,
                  and_right_elimination,
                  and_left_elimination,
                  or_right_introduction,
                  or_left_introduction,
                  not_elimination]

    atomic_rules = [and_left_elimination,
                    and_right_elimination,
                    not_elimination]

    def atomic_generator(premises, theorems = []):
        try:
            for premise in premises:
                neg_atom = Gentzen.not_elimination(premise)
                atom1 = Gentzen.and_left_elimination(premise)
                atom2 = Gentzen.and_right_elimination(premise)
                theorems.append(neg_atom)
                theorems.append(atom1)
                theorems.append(atom2)
                print(theorems)
                
                Gentzen.atomic_generator(atom1, theorems)
                Gentzen.atomic_generator(atom2, theorems)
                Gentzen.atomic_generator(neg_atom, theorems)
        except: print('idk lol')


    # TODO the generator would try to apply every rule to every
    # formule. To generate INF formules just aply the 
    # generator to previosuly generated formules recursively
    
    def generate_theorems(premises): # type(premises) = list
        if type(premises) is str:
            pass



                    














