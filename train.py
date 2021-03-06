
"""

#l1= #path to directory where all train images are held

"""##-------------------------Repeating prep labels--------------------##
df1=pd.read_excel("MalePCs.xlsx") # label file1

import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import scandir


folder = 'male' #here your dir path
file_list = []
NewNameMale =[]
OldNameMale= []
#for paths, dirs, files in scandir.walk(folder):
for (paths, dirs, files) in os.walk(folder):
    for file in files:
        if file.endswith(".png"):
            file_list.append(os.path.join(paths, file))
            NewNameMale.append(  file.split("/")[-1].split(".")[0] )
            OldNameMale.append(  file.split("/")[-1].split("-")[0]+".obj" )

OldNameMale

NewNameMale

data = {"NewName": NewNameMale, "Filename":OldNameMale}
df3 = pd.DataFrame(data)
df3

df1

dfMale = df1.merge(df3, how="inner", on="Filename")
dfMale.head(50)

dfMaleFinal = dfMale.drop(columns=["Filename"]).rename(columns={"NewName":"Filename"})
dfMaleFinal

dfMaleFinal.to_csv('male_labels.csv',index=False)
"""##---------------------------------------------------------------------------------------------##""""


df2=pd.read_csv('male_labels.csv')
import cv2
from cv2 import error 
import random 
from PIL import Image
folder = 'Images'

def load_train(df,gender):
  y=0
  x=200
  h=1000
  w=800  
  train_img=[]
  train_label=[]
  if gender=="Male" or gender=="male":
    for i in tqdm(range(len(df))):
        for (paths, dirs, files) in os.walk(folder):
            for file in files:
                if file.endswith(".png"):
                    file_path=os.path.join(paths, file)
                    img=cv2.imread(file_path)
                    crop_img = img[y:y+h, x:x+w]
                    img1=cv2.resize(crop_img,(224,224))
                    train_img.append(img1)
                    train_label.append(np.asarray([df.iloc[i][0],df.iloc[i][3]]))
  return train_img,train_label


  """elif gender=="Female" or gender=="female":
    for i in tqdm(range(len(df))):
        for (paths, dirs, files) in os.walk(folder):
            for file in files:
                if file.endswith(".png"):
                    file_path=os.path.join(paths, file)
                    img=cv2.imread(file_path)
                    img=cv2.resize(img,(224,448))
                    train_img.append(img)
                    train_label.append(np.asarray([df.iloc[i][0],df.iloc[i]

                                                  
""""selecting a sample size ##  was thinking to redefine sample size here"""

train_img,train_label=load_train(df2,"male")

import matplotlib.pyplot as plt
plt.imshow(train_img[1])    ## fails to show image as list is empty, some how the photos were not loaded/saved in the previous loop.

----- ##from here and after I have tested it on a small dataset and it works, but I havent yet tried it on the big dataset##-----------                                                  
train=np.asarray(train_img) #converting to 4d numpy array req for model
train_label=np.asarray(train_label,dtype=np.float32)
plt.imshow(train[3])
train_img[2].size

import gc
gc.collect()
del train_img # deleting unneccesary list to clear ram

from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val=train_test_split(train,train_label,test_size=0.2, random_state=42)
del train
X_train, X_test, y_train, y_test=train_test_split(X_train,y_train,test_size=0.125, random_state=42)
print(X_train.shape)
print(X_test.shape)
print(X_val.shape)
print(y_train.shape)
print(y_test.shape)
print(y_val.shape)

import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers as L
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.inception_v3 import InceptionV3

model_fn=ResNet50(include_top=False, input_shape=(224,224,3),pooling='avg')
model_fn.summary()

model=tf.keras.models.Sequential()
model.add(model_fn)
model.add(L.Dense(256,activation='relu'))
model.add(L.Dense(2,activation='linear'))
model.summary()

from tensorflow.keras.callbacks import ReduceLROnPlateau,ModelCheckpoint,EarlyStopping

rlr=ReduceLROnPlateau(monitor='val_loss', factor=0.1,
                              patience=5, min_lr=0.00001, min_delta=0.001)
ckpt=ModelCheckpoint("checkpointmodelmaleresnet.h5", monitor='val_loss', verbose=1, save_best_only=True, mode='min')
es=EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=20, min_delta=0.0001)

model.compile(optimizer=Adam(lr=0.001),
                loss='mean_squared_error',
                metrics=['mean_absolute_error'])
#onverting your tensor to float data type in this case 64
v = tf.Variable([[1, 2], [3, 4]])   
tf.keras.constraints.UnitNorm(axis=1)(tf.cast(v, tf.float64))

# model fit call with validation
history=model.fit(X_train, y_train,validation_data=(X_test,y_test), batch_size=2,
                    steps_per_epoch=len(X_train) / 2,validation_steps=len(X_test)/2, 
                    epochs=30,callbacks=[rlr,ckpt,es])
#save model weights
model.save_weights('test_male_resnet.h5')
pd.DataFrame(history.history).to_csv("log_resnet_male.csv")


