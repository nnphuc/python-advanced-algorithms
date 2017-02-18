
def median5(a): #find median size<=5
	n=len(a)
	return sorted(a)[n//2]

def partition(a,L,R,x):
	assert(R>=L)
	i=L
	while i<=R:
		if a[i]==x:
			break
		i+=1
	a[i],a[R]=a[R],a[i]
	i=L
	for j in range(L,R):
		if a[j]<=x:
			a[j],a[i]=a[i],a[j]
			i+=1
	a[i],a[R]=a[R],a[i]
	return i
def kth(a,L,R,k):
	if k>0 and k<=R-L+1:
		n=R-L+1
		median=[]
		i=0
		
		while i<n//5:
			median.append(median5(a[L+i*5:L+i*5+5]))
			i+=1
		if n%5:
			median.append(median5(a[L+i*5:L+i*5+n%5]))
			i+=1
		median_of_median= median[i-1] if i==1 else kth(median,0,i-1,i//2)
		pos=partition(a,L,R,median_of_median)
		if pos-L==k-1:
			return a[pos]
		if pos-L>k-1:
			return kth(a,L,pos-1,k)
		else:
			return kth(a,pos+1,R,k-pos+L-1)
	
