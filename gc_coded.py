from mpi4py import MPI 
import numpy as np 
from itertools import combinations

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
N=12
M=12
n = size-1
A=np.matrix('0 2 1;1 1 0;2 0 -1')
B=np.matrix('0.5 1 0;0.5 0 1;0 1 -1')


if rank==0:
	C=np.ones((N,M))
	x=np.ones((M,1))
	datasplit = list(combinations(list(range(n)),2))
	D = np.zeros((3,N,M/n))
	z = np.zeros((3,M/n,1))
	for i in range(n):
		D[i] = C[:,i*(M/n):(i+1)*(M/n)]
		z[i] = x[i*M/n:(i+1)*(M/n),:]
	D=np.ascontiguousarray(D)
	k=1
	for arr in datasplit:
		comm.Send(D[arr[0]],dest=k)
		comm.Send(D[arr[1]],dest=k)
		comm.Send(z[arr[0]],dest=k)
		comm.Send(z[arr[1]],dest=k)
		arr=np.ascontiguousarray(arr)
		print arr
		comm.Send(arr[0],dest=k)
		comm.Send(arr[1],dest=k)
		k=k+1
	arr1=[]
	E = np.zeros((3,N,1))
	for i in range(2):
		temp = np.zeros((N,1))
		info=MPI.Status()
		comm.Recv(temp,source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG,status=info)
		E[info.Get_tag()-1]=temp
		arr1.append(info.Get_tag())
	a = set(range(n))
	arr1 = set(arr1)
	k=list(a.difference(arr1))
	y = A[k[0]][0]*E[0]+A[k[0]][1]*E[1]+A[k[0]][2]*E[2]
	print y


if rank!=0:
	C1=np.zeros((N,M/n))
	comm.Recv(C1,source=0)
	C2=np.zeros((N,M/n))
	comm.Recv(C2,source=0)
	x1=np.zeros((M/n,1))
	comm.Recv(x1,source=0)
	x2=np.zeros((M/n,1))
	comm.Recv(x2,source=0)
	arr=np.zeros((2))
	#print arr
	comm.Recv(arr,source=0)
	g1=np.dot(C1,x1)
	g2=np.dot(C2,x2)
	print arr
	res = B[rank-1][arr[0]]*g1 + B[rank-1][arr[1]]*g2
	comm.send(res,dest=0,tag=rank)