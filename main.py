from Gentzen import *
example_formules = [
    '((p and (p -> r)) or (q -> t))',
    '(p and not not ((q -> r) -> (p or not r)))',
    '(p -> (q -> r))',
    'not not not',
    'not b',
    'not',
    'p',
    '(not p and (not r)',
    '(not p and (not r))',
    '( not p and ( not r))',
    '(( not p) and ( not r))',

    ]

for formule in example_formules:
    print(Gentzen.translate_string(formule))
    print(Gentzen.is_well_formed(formule))
    





