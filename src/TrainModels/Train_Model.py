import time
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import datetime
from keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint

current_time = str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))

fig, loss_ax = plt.subplots()
acc_ax = loss_ax.twinx()

tensorboard = TensorBoard(log_dir='./Logs/{}'.format(current_time))
earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
mcp_save = ModelCheckpoint('./Models/Trained-Model-ML-' + current_time + '/best_model.h5', save_best_only=True, monitor='val_loss', mode='min')

data = pd.read_excel('./Datasets/Full-Data-Set-UnderOver-2020-22.xlsx')
scores = data['Score']
margin = data['Home-Team-Win']
data.drop(['Score', 'Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU', 'OU-Cover'], axis=1, inplace=True)

data = data.values
data = data.astype(float)

x_train = tf.keras.utils.normalize(data, axis=1)
y_train = np.asarray(margin)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(512, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=50, validation_split=0.1, batch_size=32,
          callbacks=[
                    tensorboard,
                    earlyStopping,
                    mcp_save
                    ]
          )

# loss_ax.plot(history.history['loss'], 'y', label='train loss')
# loss_ax.plot(history.history['val_loss'], 'r', label='val loss')
# acc_ax.plot(history.history['accuracy'], 'b', label='train accuracy')
# acc_ax.plot(history.history['val_accuracy'], 'g', label='val accuracy')

# loss_ax.set_xlabel('epoch')
# loss_ax.set_ylabel('loss')
# acc_ax.set_xlabel('accuracy')

# loss_ax.legend(loc = 'upper left')
# acc_ax.legend(loc = 'lower left')

# plt.show()

print('Done')
