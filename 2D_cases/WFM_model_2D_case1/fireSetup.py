#!/usr/bin/env python
# coding: utf-8

# ## WFM setup
# 

# In[121]:


import math                    
import numpy as np             
import matplotlib.pyplot as plt 

folder_case="case"
folder_out="output-files"

fname_config="configure.input"
fname_configF="configureFire.input"
fname_initialF="initialFire.out"
fname_landscapeF="landscapeFire.out"


# Global configuration

# In[122]:


#Simulation setup - Global settings
FinalTime = 1400.0  #this is the final time before 800
SizeX = 200.0      #this is the domain size in X
SizeY = 200.0      #this is the domain size in Y
SizeZ = 100.0

#Fire model setup
DumpTime = 200.0    #time period to write output files
CFL = 0.4          #Courant-Friedrichs-Lewy stability criterion. Must be <0.5
Order = 7          #Order of accuracy for advection. Should be 5 or 7.

#Mesh setup
xcells = 400       #number of cells in X
ycells = 400       #number of cells in Y

#Boundary conditions (do not modify them!)
Face_1 = 3 #-y
Face_2 = 3 #+x
Face_3 = 3 #+y
Face_4 = 3 #-x

#Other parameters (constant in the domain)
u_x = 0.25000000000  #m/s
u_y = 0.25000  #m/s
K   = 0.00010   #kW/(m·K)
h   = 0.05   #kW/(m^3·K)
Tinf= 300.0 #K
RH  = 0.10   #aodim (relative humidity)
L   = 1.0   #m


# No need to modify the following cell

# In[123]:


dx=SizeX/xcells
dy=SizeY/ycells

T=np.zeros((xcells,ycells))
Y=np.zeros((xcells,ycells))
rhof=np.zeros((xcells,ycells))
Cf=np.zeros((xcells,ycells))
H=np.zeros((xcells,ycells))
Z=np.zeros((xcells,ycells))
alpha=np.zeros((xcells,ycells))
Tpc=np.zeros((xcells,ycells))
SC=np.zeros((xcells,ycells))
Rfmax=np.zeros((xcells,ycells))
Mg=np.zeros((xcells,ycells))
A=np.zeros((xcells,ycells))
    
x=np.arange(0+dx/2.0, SizeX, dx)
y=np.arange(0+dy/2.0, SizeY, dy)

xc, yc= np.meshgrid(x,y,indexing='ij')


# The **initial condition** and other properties are set here:

# In[124]:


xcenter=100
ycenter=100

#example of a circular initial fire with radius r=15 and random initial biomass with maximum Y=0.75
for l in range(0,xcells):   
    for m in range(0,ycells):
        #r=np.sqrt((xc[l,m]-xcenter)**2+(yc[l,m]-ycenter)**2)  
        r=np.sqrt((xc[l,m]-xcenter)**2+(yc[l,m]-ycenter)**2)
        if r<5:
            T[l,m]=670.0
        else:
            T[l,m]=300.0
        
        Y[l,m]=1.0
        
#landscape properties         

        Rfmax[l,m]=0.0100   #maximum volumetric porosity
        SC[l,m]=1.0#-0.5*np.random.rand(1) #surface coverage
        Z[l,m]=0.0#50.0*np.exp(-((xc[l,m]-150)**2+(yc[l,m]-100)**2)/4000) #topography
        rhof[l,m]=400.0 #solid fuel density
        Cf[l,m]=1.00 #solid fuel specific heat
        H[l,m]=4000 #solid fuel heat power
        Mg[l,m]=0.6000 #green wood water content
        alpha[l,m]=1.0 #ratio between green and season wood
        Tpc[l,m]=600.0 #pirolisis temperature
        A[l,m]=0.01 #reaction rate
        #if xc[l,m]>120:
        #    SC[l,m]=0.5



f = open(folder_case+"/"+fname_config, "w")
f.write("/////SIMULATION_SETUP////// \n")
f.write("FinalTime    "+str(FinalTime)+"\n")
f.write("SizeX    "+str(SizeX)+"\n")
f.write("SizeY    "+str(SizeY)+"\n")
f.write("SizeZ    "+str(SizeZ)+"\n")
f.close()

f = open(folder_case+"/"+fname_configF, "w")
f.write("/////SIMULATION_SETUP////// \n")
f.write("DumpTime    "+str(DumpTime)+"\n")
f.write("CFL    "+str(CFL)+"\n")
f.write("Order    "+str(Order)+"\n")
f.write("////////MESH_SETUP/////////\n")
f.write("xcells    "+str(xcells)+"\n")
f.write("ycells    "+str(ycells)+"\n")
f.write("///////BOUNDARY_COND///////\n")
f.write("Face_1    "+str(Face_1)+"\n")
f.write("Face_2    "+str(Face_2)+"\n")
f.write("Face_3    "+str(Face_3)+"\n")
f.write("Face_4    "+str(Face_4)+"\n")
f.write("/////////PARAMETERS////////\n")
f.write("u_x(m/s)    "+str(u_x)+"\n")
f.write("u_y(m/s)    "+str(u_y)+"\n")
f.write("rho(kg/m^3)    40.0 \n") #40
f.write("C(kJ/(kg·K))   1.0 \n") #1.0
f.write("H(kJ/kgFuel)   4000.0\n") #4000
f.write("K(kW/(m·K))    "+str(K)+"\n")
f.write("h(kW/(m^3·K))    "+str(h)+"\n")
f.write("Tinf(K)    "+str(Tinf)+"\n") 
f.write("Tpc(K)    400\n") #400
f.write("RH    "+str(RH)+"\n") 
f.write("L(m)    "+str(L)+"\n")
f.close()

f = open(folder_case+"/"+fname_initialF, "w")
f.write("VARIABLES = X, Y, T, Y \n")
f.write("CELLS = "+str(xcells)+", "+str(ycells)+"\n")
for l in range(0,xcells):   
    for m in range(0,ycells):
        f.write(str(xc[l,m])+" "+str(yc[l,m])+" "+str(T[l,m])+" "+str(Y[l,m])+"\n")
f.close()  


f = open(folder_case+"/"+fname_landscapeF, "w")
f.write("VARIABLES = X, Y, Z, Rfmax, SC, rhof, Cf, Mg, alpha, Tp, H, A \n")
f.write("CELLS = "+str(xcells)+", "+str(ycells)+"\n")
for l in range(0,xcells):   
    for m in range(0,ycells):
        f.write(str(xc[l,m])+" "+str(yc[l,m])+" "+str(Z[l,m])+" "+str(Rfmax[l,m])+" "+str(SC[l,m])+" "+str(rhof[l,m])+" "+str(Cf[l,m])+" "+str(Mg[l,m])+" "+str(alpha[l,m])+" "+str(Tpc[l,m])+" "+str(H[l,m])+" "+str(A[l,m])+"\n")
f.close()  

print("Files written")


# In[ ]:




