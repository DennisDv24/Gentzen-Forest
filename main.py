from GentzenForest import GentzenForest as GF

premises = [
        '( not ( not (( not ( not (r and (r and s)) ) ) and (p and q)) ) )',
        '(q -> (r and (s -> w)))'
       ]

premises2 = [
        '(p or q)',
        '(p -> y)',
        '(q -> y)'
        ]


demostrator = GF(premises2)
demostrator.atomize_forest()
demostrator.print_theorems()

print('Es y un teorema?', 'y' in demostrator.get_theorems())



