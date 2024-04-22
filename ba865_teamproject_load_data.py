# -*- coding: utf-8 -*-
"""BA865_teamproject_Load_data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QEE9n8Rzcbl6IocpmTfIcABbkuxTcUsv
"""

from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)

"""# **Model**

## Version 3 : print loading process
"""

import os
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from natsort import natsorted
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from google.colab import drive
import time

# Mount Google Drive
drive.mount('/content/gdrive', force_remount=True)
# train_folder_path = "/content/gdrive/MyDrive/BA865/data/train_(test_model)"
# test_folder_path = "/content/gdrive/MyDrive/BA865/data/test_(test_model)"
train_folder_path = "/content/gdrive/MyDrive/BA865/data/train_frame_50"
test_folder_path = "/content/gdrive/MyDrive/BA865/data/test_frame_50"
train_label_path = '/content/gdrive/MyDrive/BA865/data/train.csv'
test_label_path = '/content/gdrive/MyDrive/BA865/data/test.csv'

def load_images(folder_path):
    images, filenames, new_filenames = [], [], []
    start_time = time.time() # Start time
    # Iterate through filenames in sorted order
    for i, filename in enumerate(natsorted(os.listdir(folder_path))):
        if filename.endswith(".jpg"):
            img = Image.open(os.path.join(folder_path, filename)).resize((224, 224))
            img_array = np.array(img) / 255.0 # Normalization
            images.append(img_array)
            filenames.append(filename)
            new_filenames.append(filename.split("-")[0] + ".avi") # Modify the file name
            if (i + 1) % 500 == 0:
                print(f"{i + 1} images loaded...")
                duration = time.time() - start_time # Duration
                print(f"It took {duration:.2f} seconds.")
    return np.array(images), pd.DataFrame({"Original Filename": filenames, "New Filename": new_filenames})


def load_data_and_labels(folder_path, label_path):
    start_time = time.time() # Start timce
    # Call the above function to load images and create a DataFrame with filenames
    image, df_filenames = load_images(folder_path)
    # Read label file (train / test)
    labels = pd.read_csv(label_path)
    # Merge the label
    df_filenames = pd.merge(df_filenames, labels[['Name', 'Label']], left_on='New Filename', right_on='Name')
    # Encode the labels using LabelEncoder and extract the label vector
    label = LabelEncoder().fit_transform(df_filenames['Label'])
    df_filenames['label_encode'] = label
    end_time = time.time() # End time
    duration = end_time - start_time # Duration
    print(f"Loading data and labels took {duration:.2f} seconds.")
    return image, label, df_filenames

# Load training and test data
X_train, y_train, df_train_filenames = load_data_and_labels(folder_path = train_folder_path,label_path = train_label_path)
X_test, y_test, df_test_filenames = load_data_and_labels(folder_path = test_folder_path, label_path = test_label_path)
# Drop the duplicate column
df_test_filenames.drop(columns = 'label_encode', inplace = True)
df_test_filenames = pd.merge(df_test_filenames, df_train_filenames[['Label', 'label_encode']], on='Label', how='left')
df_test_filenames = df_test_filenames.drop_duplicates()
y_test = df_test_filenames['label_encode'].values

# Define CNN model
model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train / Validation Split
model.fit(X_train, y_train, epochs=1, validation_split=0.2)

# Evaluate the model
accuracy = model.evaluate(X_test, y_test)
print("Test Accuracy:", accuracy[1] * 100 , "%")

"""## Version 2 : With test"""

import os
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from natsort import natsorted
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from google.colab import drive

# Mount Google Drive
drive.mount('/content/gdrive', force_remount=True)
# train_folder_path = "/content/gdrive/MyDrive/BA865/data/train_(test_model)"
# test_folder_path = "/content/gdrive/MyDrive/BA865/data/test_(test_model)"
train_folder_path = "/content/gdrive/MyDrive/BA865/data/train_frame_50"
test_folder_path = "/content/gdrive/MyDrive/BA865/data/test_frame_50"
train_label_path = '/content/gdrive/MyDrive/BA865/data/train.csv'
test_label_path = '/content/gdrive/MyDrive/BA865/data/test.csv'

def load_images(folder_path):
    images, filenames, new_filenames = [], [], []
    # Iterate through filenames in sorted order
    for filename in natsorted(os.listdir(folder_path)):
        if filename.endswith(".jpg"):
            img = Image.open(os.path.join(folder_path, filename)).resize((224, 224))
            img_array = np.array(img) / 255.0 # Normalization
            images.append(img_array)
            filenames.append(filename)
            new_filenames.append(filename.split("-")[0] + ".avi") # Modify the file name
    return np.array(images), pd.DataFrame({"Original Filename": filenames, "New Filename": new_filenames})

def load_data_and_labels(folder_path, label_path):
    # Call the above function to load images and create a DataFrame with filenames
    image, df_filenames = load_images(folder_path)
    # Read label file (train / test)
    labels = pd.read_csv(label_path)
    # Merge the label
    df_filenames = pd.merge(df_filenames, labels[['Name', 'Label']], left_on='New Filename', right_on='Name')
    # Encode the labels using LabelEncoder and extract the label vector
    label = LabelEncoder().fit_transform(df_filenames['Label'])
    df_filenames['label_encode'] = label
    return image, label, df_filenames

# Load training and test data
X_train, y_train, df_train_filenames = load_data_and_labels(folder_path = train_folder_path,label_path = train_label_path)
X_test, y_test, df_test_filenames = load_data_and_labels(folder_path = test_folder_path, label_path = test_label_path)
# Drop the duplicate column
df_test_filenames.drop(columns = 'label_encode', inplace = True)
df_test_filenames = pd.merge(df_test_filenames, df_train_filenames[['Label', 'label_encode']], on='Label', how='left')
df_test_filenames = df_test_filenames.drop_duplicates()
y_test = df_test_filenames['label_encode'].values

# Define CNN model
model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train / Validation Split
model.fit(X_train, y_train, epochs=1, validation_split=0.2)

# Evaluate the model
accuracy = model.evaluate(X_test, y_test)
print("Test Accuracy:", accuracy[1] * 100 , "%")

"""## Version 1 : without x_test , y_test"""

import os
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from natsort import natsorted
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)
folder_path = "/content/gdrive/MyDrive/BA865/data/train_(test_model)"
test_folder_path = "/content/gdrive/MyDrive/BA865/data/train_frame"

def load_images(folder_path):
    images, filenames, new_filenames = [], [], []
    for filename in natsorted(os.listdir(folder_path)):
        if filename.endswith(".jpg"):
            img = Image.open(os.path.join(folder_path, filename)).resize((224, 224))
            img_array = np.array(img) / 255.0 # Normalization
            images.append(img_array)
            filenames.append(filename)
            new_filenames.append(filename.split("-")[0] + ".avi")
    return np.array(images), pd.DataFrame({"Original Filename": filenames, "New Filename": new_filenames})

# Return Images & Dataframe with original and ne filename
X_train, df_filenames = load_images(folder_path)

# Get labels
Label = pd.read_csv('/content/gdrive/MyDrive/BA865/data/train.csv')
df_filenames = pd.merge(df_filenames, Label[['Name', 'Label']], left_on='New Filename', right_on='Name')
y_train = df_filenames['Label']

# Define CNN model
model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Transform y_label from string to float
y_train = LabelEncoder().fit_transform(y_train)

# Train / Test Split
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))