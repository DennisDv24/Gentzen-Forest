from GentzenForest import *

premises = logic.Premises(['( not ((p and q) or (q -> r)))', '(p or q)'])
premises.append('(p -> (a and b))')
premises.append('(q -> (a and b))')

GF = NonMonadicGentzenForest(premises)
Morgan1 = NonMonadicInference('( not (X or Y) )', '(( not X ) and ( not Y))')
Morgan2 = NonMonadicInference('( not (X and Y) )', '(( not X ) or ( not Y))')

GF.add_inference(Morgan1)
GF.add_inference(Morgan2)
GF.print_theorems()
print()
print('Deduced Theorems:')
GF.apply_inferences_in_order(3)
GF.print_theorems()




