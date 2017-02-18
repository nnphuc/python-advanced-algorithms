import math

def _lg2(n):
    if n<1:
        return 0
    return int(math.log(n,2))
class RMQ1:
    def __init__(self,a):
        self.a=a
        n=len(a)
        L=_lg2(n)+1
        t=[]
        for i in range(L):
            t.append([])
        t[0]=range(n)
        self.n=n
        for j in range(1,L):
            t[j]=[None]*(n-pow(2,j)+1)
            for i in range(n-pow(2,(j-1))+1):
                if i+pow(2,j-1)>=len(t[j-1]):
                    break
                if a[t[j-1][i]]<a[t[j-1][i+pow(2,j-1)]]:
                    t[j][i]=(t[j-1][i])
                else:
                    t[j][i]=(t[j-1][i+pow(2,j-1)])
        self.t=t
    def query(self,u,v):
        assert(u>=0 and v<self.n and v>=u)
        k=_lg2(v-u+1)
        t=self.t
        if self.a[t[k][u]]<self.a[t[k][v-pow(2,k)+1]]:
            return t[k][u]
        return t[k][v-pow(2,k)+1]

class RMQ:
    def __init__(self,a):
        self.a=a
        self.n=len(a)
        n=self.n

        self.block_size=_lg2(n)//2+1
        self.rmq=[]
        self.ind=[]
        self.min=[]
        st=0
        while st<n:
            nd=min(n,st+self.block_size)
            self.rmq.append(RMQ1(a[st:nd]))
            self.ind.append(self.rmq[-1].query(0,self.rmq[-1].n-1)+st)
            self.min.append(a[self.ind[-1]])
            st+=self.block_size
        self.min_block=RMQ1(self.min)
    def query(self,u,v):
        assert(u>=0 and v<self.n and v>=u)
        bs=u//self.block_size
        be=v//self.block_size
        if bs==be:
            return bs*self.block_size+self.rmq[bs].query(u%self.block_size,v%self.block_size)
        x=bs*self.block_size+self.rmq[bs].query(u%self.block_size,self.rmq[bs].n-1)
        y=be*self.block_size+self.rmq[be].query(0,v%self.block_size)
        if self.a[y]<self.a[x]:
            x,y=y,x
        if bs==be-1:
            return x
        z=self.ind[self.min_block.query(bs+1,be-1)]
        if self.a[z]<self.a[x]:
            return z
        return x

import random
n=200000
a=[]
for i in range(n):
    a.append(random.randint(0,100000))
r=RMQ(a)
#r2=RMQ1(a)

