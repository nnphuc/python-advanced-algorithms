import random


def partition(A,low,high):
	"""
	#for random quick_sort
	index=random.randrange(low,high)
	pivot=A[index]
	A[index],A[high]=A[high],A[index]
	"""
	pivot=A[high]
	i=low
	for j in range(low,high):
		if A[j]<=pivot:
			A[j],A[i]=A[i],A[j]
			i+=1
	A[i],A[high]=A[high],A[i]
	return i

def quick_sort(A,low,high):
	if low<high:
		i=partition(A,low,high)
		quick_sort(A,low,i-1)
		quick_sort(A,i+1,high)

