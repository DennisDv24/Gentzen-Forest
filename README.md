# Gentzen-Forest
Gentzen Forest is a system that applies Gentzen demostration system to logic trees

### Example code:
```python
from GentzenForest import NonMonadicGentzenForest, inferences, logic

premises = logic.Premises(['( not ((p and q) or (q -> r)))', '(p or q)'])
premises.append('(p -> (a and b))')
premises.append('(q -> (a and b))')

# Creates an Gentzen system theorems generator with the basic elimination rules
GF = NonMonadicGentzenForest(premises)

# Creates extra inferences for GF
Morgan1 = inferences.NonMonadicInference('( not (X or Y) )', '(( not X ) and ( not Y))')
Morgan2 = inferences.NonMonadicInference('( not (X and Y) )', '(( not X ) or ( not Y))')

# Adds the inferences
GF.add_inference(Morgan1)
GF.add_inference(Morgan2)
GF.print_theorems()
print()
print('Deduced Theorems:')

# Try to apply every inference rule for every theorem 3 times
# (the theorems set will update with every iteration)
GF.apply_inferences_in_order(3)

GF.print_theorems()
```
