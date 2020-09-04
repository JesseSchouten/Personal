# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
import torch

x = torch.Tensor([5,3])
y = torch.Tensor([2,1])

print("OUTPUT CELL 1:")
print(x*y)

#%%
x = torch.zeros([2,5])
print("OUTPUT CELL 2:")
print(x)
print('shape of object: {}'.format(x.shape))

#%%
y = torch.rand([2,5])
print("OUTPUT CELL 3:")
print(y)

#%%
y.view([1,10])
print("OUTPUT CELL 4:")
print(y)




