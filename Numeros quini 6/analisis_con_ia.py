import pandas as pd
import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

quini_df = pd.read_csv('data/resultados_quini6_completos.csv')

# muestra algunas caracteristicas de los datos
print(quini_df.head(10)) # muestra las primeras 10 filas

x = quini_df['Fecha estándar']
y = quini_df[['Tradicional', 'La Segunda', 'Revancha', 'Siempre Sale']]

# normalized_feature = keras.utils.normalize(x.values)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=101)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

model = keras.models.Sequential()
model.add(keras.layers.Dense(4, activation='relu')) # relu es una función de activación
model.add(keras.layers.Dense(3, activation='relu'))
model.add(keras.layers.Dense(1))

model.compile(optimizer='adam', loss='mse', metrics=['mse'])

history = model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs=32)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss']) 
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper right')
plt.show()
