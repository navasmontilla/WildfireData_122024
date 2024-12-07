#!/usr/bin/env python
# coding: utf-8

# ## WFM results
# 

# Libraries are imported and program folders and files are defined:

# In[121]:


import math                    
import numpy as np             
import matplotlib.pyplot as plt 


xpt=500
Tmax=1600
Tpc=600

tp=np.linspace(300,Tmax,xpt)
psi1=np.ones(xpt)
psi2=np.zeros(xpt)
psi1b=np.ones(xpt)
psi2b=np.zeros(xpt)

psi1=psi1*0.01
psi2=0.0173*np.exp(-Tpc/tp)

for ii in range(len(tp)):
    if tp[ii]>Tpc:
        psi1b[ii]=0.01
        psi2b[ii]=0.0173*np.exp(-Tpc/tp[ii])
    else:
        psi1b[ii]=0.0
        psi2b[ii]=0.0

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(tp, psi1, '--',color="tab:green")
ax.plot(tp, psi1b, '-',color="tab:green",label='Constant ($A_c=0.01$)')
ax.plot(tp, psi2, '--',color="tab:red")
ax.plot(tp, psi2b, '-',color="tab:red",label='Arrhenius ($A_a=0.0173$)')
ax.legend()
ax.set_xlabel("T (K)") 
ax.set_ylabel("$ψ$")
ax.set_title('Combustion functions')

image_path = "fig_arrhenius.png"
fig.savefig(image_path,dpi=350)


# In[ ]:





# In[ ]:




