import collections
import bisect

def Z(s):
	n=len(s)
	z=[0]*n
	L=0
	R=0
	for i in range(1,n):
		if i>R:
			L=i
			R=i
			while R<n and s[R-L]==s[R]:
				R+=1
			z[i]=R-L
			R-=1
		else:
			k=i-L
			if z[k]<R-i+1:
				z[i]=z[k]
			else:
				L=i
				while R<n and s[R-L]==s[R]:
					R+=1
				z[i]=R-L
				R-=1
	return z
	
def preKMP(p):
    m = len(p)        # p is the input pattern
    map = [-1]*(m+1)  # map[0..m], the Knuth-Morris-Pratt border map
    i = 1; map[i] = 0; j = map[i]
    while (i < m):
        # at this point, j is MP_map[i], which is not necessarily KMP_map[i]
        if (p[i] == p[j]):
            map[i] = map[j]
        else:
            map[i] = j
            while ( (j >= 0) and (p[i] != p[j]) ):
                j = map[j]
        j = j+1; i = i+1
    map[m] = j
    return map
def KMP(s, p): # print all occurrences of pattern p in string s
    map = preKMP(p)
    occ=[]
    i = 0; j = 0
    n = len(s); m = len(p)
    for j in range(n):
        while ( (i >= 0) and (s[j] != p[i]) ):
            i = map[i]
        i = i+1
        if (i == m):
            occ.append(j-m+1)
            i = map[i]
    return occ
def lcs(a,b):
    p=collections.defaultdict(list)

    for i,v in enumerate(b):
        p[b[i]].append(i)

    ans=[-1]
    out=[None]
    for i in xrange(len(a)):
        index=a[i]
        for j in xrange(len(p[index])-1,-1,-1):
            n=p[index][j]
            if n>ans[-1]:
                ans.append(n)
                out.append(index)
            else:
                out[bisect.bisect_left(ans,n)]=index
                ans[bisect.bisect_left(ans,n)]=n
                
    
    return out

