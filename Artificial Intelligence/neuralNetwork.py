import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# One-hot encode the labels
y = tf.keras.utils.to_categorical(y)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Create a neural network model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(16, input_dim=4, activation='relu'))
model.add(tf.keras.layers.Dense(3, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32)

# Evaluate the model
_, test_acc = model.evaluate(X_test, y_test, verbose=0)
print("Test accuracy: {:.2f}%".format(test_acc * 100))