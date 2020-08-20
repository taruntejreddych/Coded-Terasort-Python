from mpi4py import MPI 
import numpy as np 
import time
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
	y = []
	x = []
	i = 0
	for xb in f.readlines() :
		xb = xb.rstrip('\n')
		var = xb.split(' ')
		x.append(int(var[0]))
		y.append(str(var[1]))

	split=l/n
	x=np.asarray(x)
	y=np.asarray(y)
	x=x.reshape((x.shape[0],1))
	y=y.reshape((y.shape[0],1))
	
	mnx=min(x)
	mxx=max(x)
	datarange=mxx-mnx

	sub = np.zeros((datasplit,l/datasplit,1))
	for i in range(datasplit):
		sub[i] = x[i*(l/datasplit):(i+1)*(l/datasplit)]
	# print(sub[1])

	for i in range(0,4):
		comm.send(mnx,dest=i+1)
		comm.send(datarange,dest=i+1)

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
	n_input=np.zeros((3,l/datasplit,1))
	mnx=comm.recv(source=0)
	datarange=comm.recv(source=0)
	for i in range(3):
		comm.Recv(n_input[i],source=0)
	# print(n_input.shape)

	p=[[],[],[],[]]
	for ia in range(0,3):
		for ib in range(0,l/datasplit):
			if(n_input[ia,ib,0]<=(mnx+datarange/4)):
				p[0].extend([n_input[ia,ib,0]])
			if((n_input[ia,ib,0]>mnx+datarange/4) and n_input[ia,ib,0]<=(mnx+datarange/2)):
				p[1].extend([n_input[ia,ib,0]])
			if((n_input[ia,ib,0]>mnx+datarange/2) and n_input[ia,ib,0]<=(mnx+3*(datarange/4))):
				p[2].extend([n_input[ia,ib,0]])			
			if(n_input[ia,ib,0]>(mnx+3*(datarange/4))):
				p[3].extend([n_input[ia,ib,0]])
	# print(len(p[0]),len(p[1]),len(p[2]),len(p[3]))

	
	if rank==1:
		# comm.Send(p[2],dest=3)
		# print(p[0],len(p[0]))	# comm.Send(p[3],dest=4)
		xo=[[],[]]
		# comm.Recv(xo[1],source=2)

		# comm.Recv(xo[2],dest=3)
	if rank==2:
		# comm.Send(p[0],dest=1)
		# comm.Send(p[3],dest=4)
		xo=[[],[]]
		# comm.Recv(xo[1],dest=3)
		# comm.Recv(xo[2],dest=4)
	# if rank==3:
	# 	comm.Send(p[0],dest=1)
	# 	comm.Send(p[1],dest=2)
	# 	xo=[[],[]]
	# 	comm.Recv(xo[1],dest=4)
	# 	comm.Recv(xo[2],dest=1)
	# if rank==4:
	# 	comm.Send(p[1],dest=2)
	# 	comm.Send(p[2],dest=3)
	# 	xo=[[],[]]
	# 	comm.Recv(xo[1],dest=1)
	# 	comm.Recv(xo[2],dest=2)

	
# comm.Bcast(l,root=0)