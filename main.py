from GentzenForest import *

t1 = logic.Tree('(( not p ) or (q -> r))')
t2 = logic.Tree('(( not p ) -> (a and b))')
t3 = logic.Tree('((q -> r) -> (a and b))')

deduced = NonMonadicGentzenForest.or_elimination([t1,t2,t3])

#and_elim = NonMonadicInference('(X and Y)','X')
#t = logic.Tree('(( not p ) and (q or r))')
#
#
#
#premises = {'(X -> Y)', 'X'}
#conclusion = 'Y'
#implication_elimination = NonMonadicInference(premises, conclusion)
#
#t1 = logic.Tree('(( not p ) -> (q and r))')
#t2 = logic.Tree('( not q )')
#deduction = implication_elimination([t1, t2]) 




