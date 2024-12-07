#!/usr/bin/env python
# coding: utf-8

# ## WFM results
# 

# Libraries are imported and program folders and files are defined:

# In[121]:


import math                    
import numpy as np             
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression

folder_base="output-files/"
folder_sol=""
folder_out=folder_base

type_model=1 #1: (T,Y), 2: (H,Y)


# Data is read:

# In[122]:


from glob import glob
import os
import re

files = sorted(glob(folder_out + "/listFire0*.out"), key=lambda x: int(re.findall(r'\d+', os.path.basename(x))[0]))
#files = glob(folder_out+"/listFire0*")
lf=len(files)
print("The number of files is", lf)

#print(files)

file1 = open(files[0], 'r')
line = file1.readline()
line = file1.readline()
cells=re.findall(r'\b\d+\b',line)
xcells=int(cells[0])
ycells=int(cells[1])

print("Mesh dimensions are:",xcells,"x",ycells)
print("\nList of files read:\n")

xc=np.zeros((xcells,ycells))
yc=np.zeros((xcells,ycells))
T=np.zeros((xcells,ycells,lf))
Y=np.zeros((xcells,ycells,lf))
H=np.zeros((xcells,ycells,lf))
Rf=np.zeros((xcells,ycells,lf))


j=0
for fname in files:
    print(fname+" file read")
    data     = np.loadtxt(fname, skiprows=2)
    k=0
    for l in range(0,xcells):   
        for m in range(0,ycells):
            #k = l + m*xcells + n*xcells*ycells
            xc[l,m]=data[k,0]
            yc[l,m]=data[k,1]
            T[l,m,j]=data[k,2]
            Y[l,m,j]=data[k,3]
            Rf[l,m,j]=data[k,4]
            if type_model==2:
                H[l,m,j]=data[k,5]
            k+=1       
    j=j+1   
    
times  = np.loadtxt(folder_out+"/times_fire.out")


# **2D PLOT:**
# 
# This creates a 2D plot, to select the time use `j=...`, the index for the file that takes values from `0` to `lf-1`:

# In[123]:


j=-1 #file number (time)

print("Plot at time:",times[j], "s")

#filename = 

xp = xc[:,0]     #puntos en x
yp = yc[0,:]      #puntos en y
Xp, Yp = np.meshgrid(xp, yp)    #matriz de puntos
ST=np.transpose(T[:,:,j])
SY=np.transpose(Y[:,:,j])
SRf=np.transpose(Rf[:,:,j])
  

fig, ax = plt.subplots(1,2,figsize=(9, 4.5))      #genera el objeto "figura"

levels = np.linspace(np.min(T), np.max(T), 12)
#print(levels)
plot1=ax[0].contour(Xp, Yp, ST, 6,levels=levels,colors="k",linewidths=0.75)  
plot1=ax[0].contourf(Xp, Yp, ST, 200, cmap='YlOrRd')   
ax[0].set_title('T(K)')
ax[0].set_xlabel("x(m)") 
ax[0].set_ylabel("y(m)") 
ax[0].set_aspect('equal', 'box')
#plot1.set_clim( np.min(T), np.max(T) )
plot1.set_clim( 300.0, 1400.0 )
ax[0].plot([100,100],[1,199],'k--')

plot2=ax[1].contourf(Xp, Yp, SY, 200, cmap='Greens' )
plot3=ax[1].contour(Xp, Yp, SY, 6,colors="k",linewidths=0.75) 
plot2.set_clim( 0.0, 1.0 )
ax[1].plot([100,100],[1,199],'k--')

ax[1].set_title('Y')
ax[1].set_xlabel("x(m)") 
ax[1].set_ylabel("y(m)") 
ax[1].set_aspect('equal', 'box')

#plot2=ax[2].contourf(Xp, Yp, SRf, 200, cmap='viridis' )
#plot1=ax[2].contour(Xp, Yp, SRf, 12,colors="k",linewidths=0.75) 
#ax[2].set_title('Rf(x,y)')
#ax[2].set_xlabel("x") 
#ax[2].set_ylabel("y") 
#ax[2].set_aspect('equal', 'box')

print("Max T is: ",np.max(ST))
print("Min T is: ",np.min(ST))

print("Max Y is: ",np.max(SY))
print("Min Y is: ",np.min(SY))

print("Max Rf is: ",np.max(SRf))
print("Min Rf is: ",np.min(SRf))

fig.text(0.15, 0.85, "SC=1.0", fontsize=11)
fig.text(0.35, 0.85, "SC=0.2", fontsize=11)


SRf=np.transpose(Rf[:,:,0])
for j in range(1,lf):
    SY=np.transpose(Y[:,:,j])
    plot4=ax[1].contour(Xp, Yp, SY, [0.99],colors="r",linewidths=0.75) 

fig.tight_layout()

fig.savefig("fig_2D_TY.png",dpi=500)  
  
  
  
j=-1 #file number (time)

#filename = 

xp = xc[:,0]     #puntos en x
yp = yc[0,:]      #puntos en y
Xp, Yp = np.meshgrid(xp, yp)    #matriz de puntos
ST=np.transpose(T[:,:,j])
SY=np.transpose(Y[:,:,j])
SRf=np.transpose(Rf[:,:,j])
  

fig, ax = plt.subplots(1,2,figsize=(10.5, 4.5))      #genera el objeto "figura"


plot2=ax[0].contourf(Xp, Yp, SY, 200, cmap='Greens' )
plot3=ax[0].contour(Xp, Yp, SY, 6,colors="k",linewidths=0.75) 
plot2.set_clim( 0.0, 1.0 )
ax[0].plot([100,100],[1,199],'k--')

ax[0].set_title('Y')
ax[0].set_xlabel("x(m)") 
ax[0].set_ylabel("y(m)") 
ax[0].set_aspect('equal', 'box')


plot2=ax[1].contourf(Xp, Yp, SRf*400.0, 200, cmap='BrBG' )
plot3=ax[1].contour(Xp, Yp, SRf*400.0, 6,colors="k",linewidths=0.75) 
plot2.set_clim( 0.0, 4.00 )
ax[1].plot([100,100],[1,199],'k--')

ax[1].set_title('W')
ax[1].set_xlabel("x(m)") 
ax[1].set_ylabel("y(m)") 
ax[1].set_aspect('equal', 'box')

cbar=fig.colorbar(plot2, ax=ax[1])
cbar.set_label('W(kg/m$^2$)')


fig.text(0.15, 0.85, "SC=1.0", fontsize=11)
fig.text(0.35, 0.85, "SC=0.4", fontsize=11)


SRf=np.transpose(Rf[:,:,0])
for j in range(1,lf):
    SY=np.transpose(Y[:,:,j])
    plot4=ax[0].contour(Xp, Yp, SY, [0.99],colors="r",linewidths=0.75) 
    plot5=ax[1].contour(Xp, Yp, SY, [0.99],colors="r",linewidths=0.75) 

fig.tight_layout()

fig.savefig("fig_2D_YW.png",dpi=500)  
  
  
  
  
  
  

# **1D PLOT (x direction):**
# 
# This creates a 1D plot at different times. Use `it` to select the number of series:

# In[125]:


nfiles=lf
fig, ax  = plt.subplots(2,1,figsize=(10, 5))
it=4
for i in range(0,nfiles,it):
    ax[0].plot(xc[:,m],T[:,m,i],'o-',ms=5,label='Time '+str(float(np.round(times[i],1)))+' s')
    
ax[0].set_xlabel("x(m)") 
ax[0].set_ylabel("T(K)") 
#ax[0].set_ylim([200,np.max(T)])
ax[0].legend()


for i in range(0,nfiles,it):
    ax[1].plot(xc[:,m],Y[:,m,i],'o-',ms=5,label=str((times[i],2)))
ax[1].set_xlabel("x(m)") 
ax[1].set_ylabel("Y") 
ax[1].set_ylim([0,1])



fig.tight_layout()

image_path = "fig_solution.png"
fig.savefig(image_path,dpi=400)

# **Calculation of the Rate of Spread (ROS)**

# In[126]:


frontLoc=np.zeros(nfiles)
vel=np.zeros(nfiles)

Tinf=T[-1,m,0]

for j in range(nfiles):
    Tmax=np.max(T[int(xcells/2):-1,m,j])
    Tmid=0.5*(Tmax+Tinf)
    pospeak=np.argmax(T[int(xcells/2):-1,m,j])+int(xcells/2)
    Tdif=np.abs(T-Tmid)
    posmax=np.argmin(Tdif[pospeak:-1,m,j])+pospeak    
    frontLoc[j]=xc[posmax,m]
    if j>0:
        vel[j]=(frontLoc[j]-frontLoc[j-1])/(times[j]-times[j-1])

frontLoc[0]=xc[int(xcells/2),m]        

j=-1
print('The position of the front at the final time',float(times[j]),'s is', frontLoc[j],'m')

fig, ax  = plt.subplots(figsize=(5, 4))
ax2 = ax.twinx()
ax2.plot(xc[posmax-80:posmax+20,m],Y[posmax-80:posmax+20,m,j],'o-',color="tab:orange",ms=5,label="Y")
ax2.set_xlabel("x (m)") 
ax2.set_ylabel("Y")
ax2.set_ylim([-0.07,1.07])
ax.plot(xc[posmax-80:posmax+20,m],T[posmax-80:posmax+20,m,j],'o-',ms=5,label="T")
ax.plot(frontLoc[j],Tmid,'o')
ax.set_xlabel("x (m)") 
ax.set_ylabel("T (K)") 
ax.set_title("Solution at final time "+str(float(times[j]))+' s') 

image_path = "fig_prfile.png"
fig.savefig(image_path,dpi=400)


fig, (ax,ax2)  = plt.subplots(1,2,figsize=(10, 4))
ax.plot(times,frontLoc,'o-')
ax.set_xlabel("time (s)") 
ax.set_ylabel("$x_{front}$ (m)") 
ax.set_title("Position of the front vs time" )
ax2.plot(times,vel,'-')
ax2.set_xlabel("time (s)") 
ax2.set_ylabel("ROS (m/s)") 
ax2.set_title("Instantaneous ROS" )

image_path = "fig_ROS.png"
fig.savefig(image_path,dpi=400)

times = times.reshape(-1,1)
frontLoc = frontLoc.reshape(-1,1)
regression_model = LinearRegression()
regression_model.fit(times, frontLoc)
print('The ROS is:' ,float(regression_model.coef_), 'm/s')







