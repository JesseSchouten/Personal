# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 20:02:44 2020

@author: Jesse
"""
#%%
import torch
import torchvision
from torchvision import transforms, datasets

print('Download data: \n')
train = datasets.MNIST("",train=True,download=True
                      ,transform=transforms.Compose([transforms.ToTensor()])
                      )

test = datasets.MNIST("",train=False,download=True
                      ,transform=transforms.Compose([transforms.ToTensor()])
                      )
print('Data downloaded. \n')
#%%
print("Set loaded data to DataLoader types.\n")
trainset = torch.utils.data.DataLoader(train,batch_size=10,shuffle=True)
testset = torch.utils.data.DataLoader(test,batch_size=10,shuffle=True)

#%%

print("Iterate over first batch in training data:\n")
for data in trainset:
    print(data)
    break

x,y = data[0][0],data[1][0]



#%%
import matplotlib.pyplot as plt

print("Reshape current shape of {}.\n".format(x.shape))
plt.imshow(data[0][0].view([28,28]))
print("We validated that the first row is actually a 3.")

#%%
print("Check if dataset is balanced.\n")
total = 0
counter_dict = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}


for data in trainset:
    Xs, ys = data 
    for y in ys:
        counter_dict[int(y)] +=1
        total+=1

print(counter_dict)

for i in counter_dict:
    print(f"{i}: {counter_dict[i]/total*100}")
    
print("We conclude the data is balanced enough.")