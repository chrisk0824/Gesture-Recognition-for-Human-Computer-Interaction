# -*- coding: utf-8 -*-
"""BA865_teamproject_load_data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZsEXv0evVVUvx16JEitHGn45cAMmDvp4
"""

# Mount to drive
from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)

# Import necessary libraries
import os
import shutil
import numpy as np
import pandas as pd

def change_value(df,index):
  # df has two columns: 'Name' and 'Label'
  for idx in range(len(df)):
    if idx < len(df)/2:
        df.iloc[idx,0] =  df.iloc[idx,0].replace('devel','')
        df.iloc[idx,0] =  df.iloc[idx,0].split('_')[0] + '_M_' + df.iloc[idx,0].split('_')[1] + '.avi'
    else:
        df.iloc[idx,0] =  df.iloc[idx,0].replace('devel','')
        df.iloc[idx,0] =  df.iloc[idx,0].split('_')[0] + '_K_' + df.iloc[idx,0].split('_')[1] + '.avi'
  df['Label'] = '_' + df['Label'].astype('string').str.strip().replace(' ','')
  df['Label'] = str(index) + df['Label']
  return df

def copy_file(index,df,new_folder,path_folder):
  # Get full video path
  if index < 10:
    video_path = [os.path.join(path_folder+'devel0'+str(index)+'/', f) for f in os.listdir(path_folder+'devel0'+str(index)+'/') if f.endswith(".avi")]
  else:
    video_path = [os.path.join(path_folder+'devel'+str(index)+'/', f) for f in os.listdir(path_folder+'devel'+str(index)+'/') if f.endswith(".avi")]
  # Loop through df to identify video need to be copied
  for name in df['Name']:
    # search_pattern set [3:] when two-digit, set [4:] when three-digit
    search_pattern = name[3:]
    matches = [path for path in video_path if path.endswith(search_pattern)]
    old_path = ' '.join([str(elem) for elem in matches])
    new_path = new_folder + name
    shutil.copy(old_path, new_path)

# Create df_train and df_test that contains filename and labelname (file: folder_num + M + video_num + '.avi', label: folder_num + label)
path_folder = '/content/gdrive/MyDrive/BA865/data/devel01-40/'
train_folder = '/content/gdrive/MyDrive/BA865/data/train_data/'
test_folder = '/content/gdrive/MyDrive/BA865/data/test_data/'

# Check if history train and test csv exists
if os.path.exists('/content/gdrive/MyDrive/BA865/data/test_data/test.csv'):
  df_train_all = pd.read_csv(train_folder +'train.csv')
  df_test_all = pd.read_csv(test_folder +'test.csv')
else:
  df_train_all = pd.DataFrame(columns=['Name','Label'])
  df_test_all = pd.DataFrame(columns=['Name','Label'])

# Loop through the directory: i must put the folder name
for index in range(0,40):
  if index < 10:
    df_train = pd.read_csv(path_folder + 'devel0' + str(index) + '/devel0' + str(index) + '_train.csv',header=None)
    df_test = pd.read_csv(path_folder + 'devel0' + str(index) + '/devel0' + str(index) +'_test.csv',header=None)
  elif index > 9:
    df_train = pd.read_csv(path_folder + 'devel' +str(index) + '/devel' + str(index) + '_train.csv',header=None)
    df_test = pd.read_csv(path_folder + 'devel' + str(index) + '/devel' + str(index) +'_test.csv',header=None)

  # Training data
  df_train = df_train.rename({0:'Name',1:'Label'},axis=1)
  df_train = pd.concat([df_train,df_train],axis=0).reset_index(drop=True)

  # 1. Change Name and Label (first M.avi then K.avi)
  df_train = change_value(df_train,index)
  df_train_all = pd.concat([df_train_all,df_train],axis=0).reset_index(drop=True)
  # 2. Move video to new folder
  copy_file(index,df_train,train_folder)

  # Testing data
  df_test['Value_count'] = df_test[1].apply(lambda x: len(x.split()))
  df_test = df_test[df_test['Value_count'] == 1]
  df_test = df_test.drop('Value_count',axis=1)
  df_test = df_test.rename({0:'Name',1:'Label'},axis=1)
  df_test = pd.concat([df_test,df_test],axis=0).reset_index(drop=True)

  # 1. Change Name and Label (first M.avi then K.avi)
  df_test = change_value(df_test,index)
  df_test_all = pd.concat([df_test_all,df_test],axis=0).reset_index(drop=True)
  # 2. Move video to new folder
  copy_file(index,df_test,test_folder)

# Save csv to drive
df_train_all.to_csv('/content/gdrive/MyDrive/BA865/data/train_data/train.csv')
df_test_all.to_csv('/content/gdrive/MyDrive/BA865/data/test_data/test.csv')
print('CSV files saved to drive')