#!/usr/bin/env python
# coding: utf-8

# ## WFM setup
# 

import math                    
import numpy as np             
import matplotlib.pyplot as plt 
import os
from sklearn.linear_model import LinearRegression
from glob import glob
import re
import shutil
import subprocess


data = np.loadtxt("porosityresults.txt", skiprows=1)
meshes = data[:, 0]
velocs = data[:, 1]

data = np.loadtxt("porosity1results.txt", skiprows=1)
meshes1 = data[:, 0]
velocs1 = data[:, 1]

data = np.loadtxt("porosity2results.txt", skiprows=1)
meshes2 = data[:, 0]
velocs2 = data[:, 1]


fig, ax  = plt.subplots(figsize=(5, 3.5))
ax.plot(meshes*0.01*0.01,velocs,'o-',label="Only fuel")
ax.plot(meshes1*0.01*0.01,velocs1,'o-',label="Mixture (constant in time)")
ax.plot(meshes2*0.01*0.01,velocs2,'o-',label="Mixture (time varying)")
ax.set_xlabel("R$_{f,0}$") 
ax.set_ylabel("ROS(m/s)") 

# Add a secondary x-axis on the top
def forward_transform(x):
    return x *400  # Example transformation

def inverse_transform(x):
    return x /400

secax = ax.secondary_xaxis('top', functions=(forward_transform, inverse_transform))
secax.set_xlabel("Fuel bulk density (kg/m$^3$)")  # Label for the secondary axis


fig.tight_layout()

ax.legend()
plt.show()

fig.savefig("fig_ROS_vs_BD.png",dpi=350)



# ### 
