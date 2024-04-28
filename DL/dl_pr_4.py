# -*- coding: utf-8 -*-
"""DL_PR_4

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HQ-9uIPi1O7ClrbuDlMQp9my_KQwfXq1
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Step 1: Load and preprocess the data
data = pd.read_csv('GOOGL.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Normalize the data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Step 2: Split the data
train_size = int(len(data_scaled) * 0.8)
train_data, test_data = data_scaled[:train_size], data_scaled[train_size:]

# Step 3: Prepare the data for RNNs
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

seq_length = 30
X_train, y_train = create_sequences(train_data, seq_length)
X_test, y_test = create_sequences(test_data, seq_length)

# Step 4: Define the RNN model
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
    tf.keras.layers.LSTM(50, return_sequences=False),
    tf.keras.layers.Dense(1)
])

# Step 5: Compile the model
model.compile(loss='mean_squared_error', optimizer='adam')

# Step 6: Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Step 7: Evaluate the model
test_loss = model.evaluate(X_test, y_test)
print("Test loss:", test_loss)

# Step 8: Make predictions
predictions = model.predict(X_test)