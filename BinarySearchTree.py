class Node:
    def __init__(self,data):
        self.left=None
        self.right=None
        self.parent=None
        self.key=data
        self.count=1
        
    def __repr__(self):
        return repr(self.key)

    def size(self):
        return self.count

def TreeSearch(x,k):
    if x is None or k==x.key:
        return x
    if k<x.key:
        return TreeSearch(x.left,k)
    return TreeSearch(x.right,k)

def TreeMinimum(x):
    while x.left is not  None:
        x=x.left
    return x

def TreeMaximum(x):
    while x.right is not None:
        x=x.right
    return x

def TreeSuccessor(x):
    if x.right is not None:
        return TreeMinimum(x.right)
    y=x.parent
    while y is not None and x==y.right:
        x=y
        y=y.parent
    return y

def TreePredecessor(x):
    if x.left is not None:
        return TreeMaximum(x.left)
    y=x.parent
    while y is not None and x==y.left:
        x=y
        y=y.parent
    return y


def TreeInsert(T,z):
    y=None
    x=T.root
    while x is not None:
        y=x
        if z.key<x.key:
            x=x.left
        else:
            x=x.right
    z.parent=y
    if y is None:
        T.root=z
    else:
        if z.key<y.key:
            y.left=z
        else:
            y.right=z

def TreeTransplant(T,u,v):
    if u.parent is None:
        T.root=v
    elif u==u.parent.left:
        u.parent.left=v
    else:
        u.parent.right=v
    if v is not None:
        v.parent=u.parent

def TreeDelete(T,z):
    if z.left is None:
        TreeTransplant(T,z,z.right)
    elif z.right is None:
        TreeTransplant(T,z,z.left)
    else:
        y=TreeMinimum(z.right)
        if y.parent!=z:
            TreeTransplant(T,y,y.right)
            y.right=z.right
            y.right.parent=y
        TreeTransplant(T,z,y)
        y.left=z.left
        y.left.parent=y

class BinarySearchTree:

    def __init__(self):
        self.root=None
        
    def _inorder(self,node,func):
        if node is None:
            return
        self._inorder(node.left,func)
        func(node)
        self._inorder(node.right,func)
        
    def inorder(self,func=print):
        self._inorder(self.root,func)

    def insert(self,key):
        node=Node(key)
        TreeInsert(self,node)
        return node
    
    def search(self,key):
        ans=TreeSearch(self.root,key)
        return ans

    def deleteKey(self,key):
        node=self.search(key)
        if node is not None:
            TreeDelete(self,node)

    def deleteNode(self,node):
        if node is not None:
            TreeDelete(self,node)
    
    def min(self):
        return TreeMinimum(self.root)

    def max(self):
        return TreeMaximum(self.root)
