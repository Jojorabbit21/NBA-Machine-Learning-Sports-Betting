import time
import numpy as np
import pandas as pd
import tensorflow as tf
import datetime
from keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint


current_time = str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))

tensorboard = TensorBoard(log_dir='./Logs/{}'.format(current_time))
earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
mcp_save = ModelCheckpoint('./Models/Trained-Model-OU-' + current_time + '/best_model.h5', save_best_only=True, monitor='val_loss', mode='min')

data = pd.read_excel('./Datasets/Full-Data-Set-UnderOver-2021-22.xlsx')
OU = data['OU-Cover']
data.drop(['Score', 'Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU-Cover'], axis=1, inplace=True)

data = data.values
data = data.astype(float)

x_train = tf.keras.utils.normalize(data, axis=1)
y_train = np.asarray(OU)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(1024, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(3, activation=tf.nn.softmax))

adam = tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
sgd = tf.keras.optimizers.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)

model.compile(optimizer=adam, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=200, validation_split=0.1, batch_size=32, verbose=2,
          callbacks=[
            tensorboard, 
            earlyStopping, 
            mcp_save
            ])

print('Done')
