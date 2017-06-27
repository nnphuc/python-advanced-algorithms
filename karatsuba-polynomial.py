import math
import itertools
import operator

def mul_x_k(x,k):  # return P(x)*x^k
    return [0]*k+x

def add(a,b):  #return a(x)+b(x)
    return list(map(lambda x:(x[1] or 0)+(x[0] or 0),itertools.zip_longest(a,b)))

def sub(a,b): #return a(x)-b(x)
    return list(map(lambda x:-(x[1] or 0)+(x[0]or 0),itertools.zip_longest(a,b)))

def mul_w(x,w): #return P(x)*w
    return list(map(lambda t:t*w,x))

def mul_naive(x,y):

    ans=[0]
    for i,w in enumerate(y):
        t=mul_w(x,w)
        t=mul_x_k(t,i)
        ans=add(ans,t)
    return ans

def mul_karatsuba(x,y):

    m=max(len(x),len(y))
    if m<3:
        return mul_naive(x,y)
    m2=m//2
    lo1=x[:m2]
    lo2=y[:m2]
    hi1=x[m2:]
    hi2=y[m2:]
    z0=mul_karatsuba(lo1,lo2)   
    z1=mul_karatsuba(add(lo1,hi1),add(lo2,hi2))
    z2=mul_karatsuba(hi1,hi2)
    a=mul_x_k(z2,2*m2)
    t=sub(z1,z2)
    t=sub(t,z0)
    b=mul_x_k(t,m2)
    ans= add(add(a,b),z0)
    while len(ans)>1 and ans[-1]==0:
        ans.pop()
    return ans
    
