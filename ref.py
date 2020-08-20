from mpi4py import MPI 
import numpy as np 
import time
from natsort import natsorted 
# start = time.time()


# end = time.time()
# time_taken=end-start
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n = size-1
r=3
k=4
datasplit=6  #kCr
l=30000		#change accordingly to test file or else need to broadcast


if rank==0:
	f = open("new2.txt", "r")
	vars1 = []
	i = 0
	for x in f.readlines() :
		x = x.rstrip('\n')
		var = x.split(' ')
		arr = []
		arr.append(int(var[0]))
		arr.append(str(var[1]))
		vars1.append(arr)

	vars1=np.array(vars1)
	# l=len(vars1)
	split=l/n
	x=vars1[:,0]
	x=x.reshape((x.shape[0],1))
	# x=np.array(x)
	# x=np.zeros((np.size(xn),1))
 	h=[]
 	for i in range(0,len(x)):
		h.append(int(x[i]))
	# x=np.asarray(x)
	# x=x.reshape((x.shape[0],1))
	print(np.size(h))
	print(min(h),max(h))
	print(int(min(x)),int(max(x)))
	x=natsorted(x)
	print(x[0],x[-1])

	# print('---->',len(xn),max(xn),min(xn))
	# vars1=np.array(vars1)  
	# l=len(vars1)
	# x=vars1[0]		#why is vars1[:,0] a string?
	# print('===>',len(x),max(x),min(x))
	# x=x.astype(int)
	# x=x.reshape((x.shape[0],1))
	# print(x[0],int(x[0]))
	# print(datarange)
	# y=y.reshape((y.shape[0],1))
	# y=np.array(y)
	# print(y[0])
	# range=int(max(xn))-int(min(xn))
	# range=max(x)-min(x)
	# print(range)

	y=vars1[:,1]
	y=y.reshape((y.shape[0],1))
	y=np.array(y)

	sub = np.zeros((datasplit,l/datasplit,2))
	for i in range(datasplit):
		sub[i] = x[i*(l/datasplit):(i+1)*(l/datasplit),:]
	sub=np.ascontiguousarray(sub)
	comm.Send(sub[0],dest=1)
	comm.Send(sub[0],dest=2)

	comm.Send(sub[1],dest=1)
	comm.Send(sub[1],dest=3)

	comm.Send(sub[2],dest=1)
	comm.Send(sub[2],dest=4)

	comm.Send(sub[3],dest=2)
	comm.Send(sub[3],dest=3)

	comm.Send(sub[4],dest=2)
	comm.Send(sub[4],dest=4)

	comm.Send(sub[5],dest=3)
	comm.Send(sub[5],dest=4)

if rank!=0:
	n_input=np.zeros((3,l/datasplit,2))
	l=0
	for i in range(3):
		comm.Recv(n_input[i],source=0)
		# print(n_input[i].shape)
	# q=0
	# p=np.zeros((4,10000,1))
	# for ia in range(0,3):
	# 	for ib in range(0,l/datasplit)
	# 		if(n_input[ia,ib,0]<=(min(x)+datarange/4))
	# 			p[1,q,0]=n_input[ia,ib,0]
	# 			q=q+1
	# 		if(n_input[ia,ib,0]<=(min(x)+datarange/4))
	# 			p[1,q,0]=n_input[ia,ib,0]
	# 			q=q+1

# comm.Bcast(l,root=0)