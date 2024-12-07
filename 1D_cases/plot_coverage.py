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


data = np.loadtxt("coverageresults.txt", skiprows=1)
meshes = data[:, 0]
velocs = data[:, 1]

data = np.loadtxt("coverage1results.txt", skiprows=1)
meshes1 = data[:, 0]
velocs1 = data[:, 1]

data = np.loadtxt("coverage2results.txt", skiprows=1)
meshes2 = data[:, 0]
velocs2 = data[:, 1]

fig, ax  = plt.subplots(figsize=(5, 3.5))
ax.plot(meshes,velocs,'o-',label="Only fuel")
ax.plot(meshes1,velocs1,'o-',label="Mixture (constant in time)")
ax.plot(meshes2,velocs2,'o-',label="Mixture (time varying)")
ax.set_xlabel("SC(%)") 
ax.set_ylabel("ROS(m/s)") 


fig.tight_layout()

ax.legend()

fig.savefig("fig_ROS_vs_SC.png",dpi=350)



# ### 
