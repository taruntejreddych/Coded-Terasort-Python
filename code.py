from mpi4py import MPI 
import numpy as np 
import time
start = time.time()

f = open("new.txt", "r")
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
print("vars1 shape",vars1.shape)
# print vars1[0][0]
# print vars1[0][1]
# x=vars1[1][0]
# print(x)
# vars1=np.matrix(np.array(vars1))
# print(size(vars1))
end = time.time()
time_taken=end-start
# print('Time: ',time_taken)

# print(type(vars1))
# x=vars1[:,0]
# print(vars1)
# print(x)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
n = size-1
l=len(vars1)
split=l/n
# print((vars1[2])[0])

x=vars1[:,0]
print("before",x.shape)
x=x.reshape((x.shape[0],1))
print("after",x.shape)
if rank==0:
	node_input=np.zeros((l/n,1))
	y=0
	for i in range(n):
		node_input=x
		# node_input=np.array(node_input)
		node_input=np.ascontiguousarray(node_input)

		# print (np.size((node_input)))

		comm.Send(node_input,dest=i+1)
		y += l/n


if rank!=0:
	# n_input=[None]*(l/n)
	n_input=np.zeros((l/n,1))
	# print(len(n_input))
	comm.Recv(n_input,source=0)
	# print (len(n_input))
