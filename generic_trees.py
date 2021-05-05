
class GenericTree: # interface for binary trees

    def summary(self, title = 'Tree'):
        print('--------'+('-'*len(title)))
        print('---',title,'---')
        print('--------'+('-'*len(title)))

        print('Root: ', self.value)
        if not self.left is None: print('Left: ', self.left.value)
        if not self.right is None: print('Right: ',self.right.value)
        print('Nodes count: ', self.count_nodes())
        print('Tree height: ', self.calc_height())
        print()
    
    def has(self, value):
        if self.value == value:
            return True
        if value < self.value:
            if self.left is None: return False
            else: return self.left.has(value)
        if self.right is None: return False
        else: return self.right.has(value)
        

    def count_nodes(self):
        l, r = 0, 0
        if not self.left is None: l = self.left.count_nodes()
        if not self.right is None: r = self.right.count_nodes()
        return 1 + l + r
    
    def calc_height(self):
        l, r = 0, 0
        if not self.left is None: l = self.left.calc_height()
        if not self.right is None: r = self.right.calc_height()
        return 1 + max(l, r)
    
    def calc_height(node):
        if node is None: return 0
        return 1 + max(GenericTree.calc_height(node.left), GenericTree.calc_height(node.right))

    def preorder(self):
        print(self.value)
        if not self.left is None: self.left.preorder()
        if not self.right is None: self.right.preorder()

    def inorder(self):
        if self is None: return
        if not self.left is None: self.left.inorder()
        print(self.value)
        if not self.right is None: self.right.inorder()

    def postorder(self):
        if self is None: return
        if not self.left is None: self.left.postorder()
        if not self.right is None: self.right.postorder()
        print(self.value)

    def print_node(self):
        print('  ', self.value)
        spaces = ' ' * len(str(self.value))
        print(' /', spaces, '\ ')
        if self.left is not None: aux_left = self.left.value
        else: aux_left = 'N'
        if self.right is not None: aux_right = self.right.value
        else: aux_right = 'N'
        print(aux_left, spaces + '  ', aux_right)

    def print_ez_each_node(self):
        self.print_node()
        if self.left is not None: self.left.print_each_node()
        if self.right is not None: self.right.print_each_node()
        
    def print_each_node(self):
        self.print_node()
        if self.left is not None:
            if self.left.right is not None or self.left.left is not None:
                self.left.print_each_node()
        if self.right is not None:
            if self.right.right is not None or self.right.left is not None:
                self.right.print_each_node()




