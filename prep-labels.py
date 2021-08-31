# -*- coding: utf-8 -*-
"""
Created on Tue May 11 14:31:51 2021

@author: u567351
 """
"""
"""

import pandas as pd
import numpy as np
from tqdm.notebook import tqdm

import os
import scandir

folder = 'Images' #here your dir path
file_list = []

for paths, dirs, files in scandir.walk(folder):
#for (paths, dirs, files) in os.walk(folder):
    for file in files:
        if file.endswith(".png"):
            file_list.append(os.path.join(paths, file))

print (len(file_list))
l1=file_list

df1=pd.read_excel("MalePCs.xlsx") # label file1
df2=pd.read_excel("FemalePCs.xlsx") # label file2
df2.head()

folder = 'female' #here your dir path
file_list1 = []
NewNameFemale =[]
OldNameFemale= []
#for paths, dirs, files in scandir.walk(folder):
for (paths, dirs, files) in os.walk(folder):
    for file in files:
        if file.endswith(".png"):
            file_list1.append(os.path.join(paths, file))
            NewNameFemale.append(  file.split("/")[-1].split(".")[0] )
            OldNameFemale.append(  file.split("/")[-1].split("-")[0]+".obj" )

file_list1

OldNameFemale

NewNameFemale

data = {"NewName": NewNameFemale, "Filename":OldNameFemale}
NewFemaleDf = pd.DataFrame(data)
NewFemaleDf

df2

dfFemale = df2.merge(NewFemaleDf, how="inner", on="Filename")
dfFemale.head(50)

dfFemaleFinal = dfFemale.drop(columns=["Filename"]).rename(columns={"NewName":"Filename"})
dfFemaleFinal
dfFemaleFinal.to_csv('labels_female.csv',index=False)
##-----------------------##

folder = 'male' #here your dir path
file_list2 = []
NewNameMale =[]
OldNameMale= []
#for paths, dirs, files in scandir.walk(folder):
for (paths, dirs, files) in os.walk(folder):
    for file in files:
        if file.endswith(".png"):
            file_list1.append(os.path.join(paths, file))
            NewNameMale.append(  file.split("/")[-1].split(".")[0] )
            OldNameMale.append(  file.split("/")[-1].split("-")[0]+".obj" )

OldNameMale

NewNameMale
print(len(OldNameMale))
data = {"NewName": NewNameMale, "Filename":OldNameMale}
df3 = pd.DataFrame(data)
df3

df1

dfMale = df1.merge(df3, how="inner", on="Filename")
dfMale.head(50)

dfMaleFinal = dfMale.drop(columns=["Filename"]).rename(columns={"NewName":"Filename"})
dfMaleFinal

dfMaleFinal.to_csv('labels_male.csv',index=False)
