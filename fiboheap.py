from random import randint

class FibonacciHeap:
    
    # internal node class 
    class Node:
        def __init__(self, data):
            self.data = data
            self.parent = self.child = self.left = self.right = None
            self.degree = 0
            self.mark = False
            
    # function to iterate through a doubly linked list
    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right
    
    # pointer to the head and minimum node in the root list
    min_node = None
    
    # maintain total node count in full fibonacci heap
    total_nodes = 0
    
    # return min node in O(1) time
    def find_min(self):
        return self.min_node
         
    # extract (delete) the min node from the heap in O(log n) time
    # amortized cost analysis can be found here (http://bit.ly/1ow1Clm)
    def extract_min(self):
       
        z = self.min_node
        if z is not None:
            if z.child is not None:
                # attach child nodes to root list
                children = [x for x in self.iterate(z.child)]
                for i in xrange(0, len(children)):
                    self.merge_with_min_node(children[i])
                    children[i].parent = None
                
            self.remove_from_min_node(z)
            # set new min node in heap
            if z == z.right:
                self.min_node = self.min_node = None
            else:
                self.min_node = z.right
                self.consolidate()
            self.total_nodes -= 1
        return z
                    
    # insert new node into the unordered root list in O(1) time
    def insert(self, data):
        n = self.Node(data)
        n.left = n.right = n
        self.merge_with_min_node(n)
        if self.min_node is None or n.data < self.min_node.data:
            self.min_node = n
        self.total_nodes += 1
        
    # modify the data of some node in the heap in O(1) time
    def decrease_key(self, x, k):
        if k > x.data:
            return None
        x.data = k
        y = x.parent
        if y is not None and x.data < y.data:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.data < self.min_node.data:
            self.min_node = x
            
    # merge two fibonacci heaps in O(1) time by concatenating the root lists
    # the root of the new root list becomes equal to the first list and the second
    # list is simply appended to the end (then the proper min node is determined)
    def merge(self, h2):
        H = FibonacciHeap()
        H.min_node, H.min_node = self.min_node, self.min_node
        # fix pointers when merging the two heaps
        last = h2.min_node.left
        h2.min_node.left = H.min_node.left
        H.min_node.left.right = h2.min_node
        H.min_node.left = last
        H.min_node.left.right = H.min_node
        # update min node if needed
        if h2.min_node.data < H.min_node.data:
            H.min_node = h2.min_node
        # update total nodes
        H.total_nodes = self.total_nodes + h2.total_nodes
        return H
        
    # if a child node becomes smaller than its parent node we
    # cut this child node off and bring it up to the root list
    def cut(self, x, y):
        self.remove_from_child_list(y, x)
        y.degree -= 1
        self.merge_with_min_node(x)
        x.parent = None
        x.mark = False
    
    # cascading cut of parent node to obtain good time bounds
    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)
    
    # combine root nodes of equal degree to consolidate the heap
    # by creating a list of unordered binomial trees
    def consolidate(self):
        A = {}
        nodes = [w for w in self.iterate(self.min_node)]
        for w in xrange(0,len(nodes)):
            x = nodes[w]
            d = x.degree
            
            while d in A:
                y = A[d] 
                if x.data > y.data:
                    x,y=y,x
                self.heap_link(y, x)
                del A[d]
                d += 1
            A[d] = x
        # find new min node - no need to reconstruct new root list below
        # because root list was iteratively changing as we were moving 
        # nodes around in the above loop
        for x in A.itervalues():
                if x.data < self.min_node.data:
                    self.min_node = x
        
    # actual linking of one node to another in the root list
    # while also updating the child linked list
    def heap_link(self, y, x):
        assert(y)
        assert(x)
        self.remove_from_min_node(y)
        y.left = y.right = y
        self.merge_with_child_list(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False
        
    # merge a node with the doubly linked root list   
    def merge_with_min_node(self, node):
        assert(node)
        if self.min_node is None:
            self.min_node = node
        else:
            node.right = self.min_node.right
            node.left = self.min_node
            self.min_node.right.left = node
            self.min_node.right = node
            
    # merge a node with the doubly linked child list of a root node
    def merge_with_child_list(self, parent, node):
        assert(parent)
        assert(node)
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node
            
    # remove a node from the doubly linked root list
    def remove_from_min_node(self, node):
        if node == self.min_node:
            self.min_node = node.right
        node.left.right = node.right
        node.right.left = node.left
        
    # remove a node from the doubly linked child list
    def remove_from_child_list(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left
        







