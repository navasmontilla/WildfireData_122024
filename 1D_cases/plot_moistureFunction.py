#!/usr/bin/env python
# coding: utf-8

# ## WFM results
# 

# Libraries are imported and program folders and files are defined:

# In[121]:


import math                    
import numpy as np             
import matplotlib.pyplot as plt 


import numpy as np
import matplotlib.pyplot as plt

# Define the functions for W, K, K1, and K2
def W(T):
    return 349 + 1.29 * T + 0.0135 * T**2

def K(T):
    return 0.805 + 0.000736 * T - 0.00000273 * T**2

def K1(T):
    return 6.27 - 0.00938 * T - 0.000303 * T**2

def K2(T):
    return 1.91 + 0.0407 * T - 0.000293 * T**2

# Define the function for M based on T and h
def M(T, h):
    w = W(T)
    k = K(T)
    k1 = K1(T)
    k2 = K2(T)
    
    numerator = (k * h / (1 - k * h)) + ((k1 * k * h + 2 * k1 * k2 * k**2 * h**2) / (1 + k1 * k * h + k1 * k2 * k**2 * h**2))
    return (18 / w) * numerator

# Define the range of T and h values
T_values = np.linspace(0, 60, 100)  
h_values = np.linspace(0.0, 1.0, 100)  

# Create a meshgrid for T and h
T_grid, h_grid = np.meshgrid(T_values, h_values)

# Calculate M for each combination of T and h
M_values = M(T_grid, h_grid)

# Plotting
fig, ax = plt.subplots(figsize=(6, 4))
cp = ax.contourf(T_grid, h_grid, M_values, levels=256, cmap="cividis_r")  # Convert h to percentage for y-axis
cp2 = ax.contour(T_grid, h_grid, M_values, levels=np.linspace(0.02, 0.28, 14)  ,colors="k",linewidths=0.5)  # Convert h to percentage for y-axis
fig.colorbar(cp, label="Md")
ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("RH")

ax.clabel(cp2, inline=1, fontsize=7)

plt.tight_layout()

image_path = "fig_rhmoisture.png"
fig.savefig(image_path,dpi=350)