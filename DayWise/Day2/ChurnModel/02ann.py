# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 22:48:52 2019

@author: TSE
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Churn Modelling-Bank Customers.csv')
X = dataset.iloc[:, 3:13].values
y = dataset.iloc[:, 13].values

from sklearn.preprocessing import LabelEncoder,OneHotEncoder
labelEncoderObj = LabelEncoder()
X[:,1] = labelEncoderObj.fit_transform(X[:,1])

labelEncoderObj_X2 = LabelEncoder()
X[:,2] = labelEncoderObj_X2.fit_transform(X[:,2])

onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:]

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, 
                                                    random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# Importing the Keras libraries and packages
import keras
from keras.models import Sequential  # used to intiliazie nueral networks
from keras.layers import Dense       # used to create layers

# Initialising the ANN
classifier = Sequential()   

# Adding the input layer and the first hidden layer
# output_dim is the nueron nodes in the hidden layer , we are using 6 , average of (input layer +output layer)
#Dense will initialize the weights to a small number , init (initialize the weights with 'uniform' function)
# 11 input nodes as 11 independent variables
# rectifier(relu) activation function for input and hidden layer  

classifier.add(Dense(output_dim = 6, 
                     init = 'uniform', 
                     activation = 'relu', input_dim = 11))

# Adding the second hidden layer, optional for this example
classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu'))

# Adding the output layer
#sigmoid activation function for output layer

classifier.add(Dense(output_dim = 1, init = 'uniform', 
                     activation = 'sigmoid'))

# Compiling the ANN
#optimizer is the algorith that we want to use to find the optimal weights
# adam => Stochastic gradient algorithm 
# loss function is same as ordinary least squared 
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', 
                   metrics = ['accuracy'])


# Fitting the ANN to the Training set
# epoch number of iterations for adjusting weights to achive accuraccy
classifier.fit(X_train, y_train, batch_size = 10, nb_epoch = 100) 


# Predicting the Test set results
y_pred = classifier.predict(X_test)

y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

from sklearn.metrics import accuracy_score
acc=accuracy_score(y_test, y_pred)

# Predicting a single new observation
"""Predict if the customer with the following informations will leave the bank:
Geography: France
Credit Score: 600
Gender: Male
Age: 30
Tenure: 5
Balance: 45000
Number of Products: 2
Has Credit Card: Yes
Is Active Member: Yes
Estimated Salary: 55000"""
new_prediction = classifier.predict(sc.transform(np.array([[0.0, 0, 600, 1, 30, 5, 45000, 2, 1, 1, 55000]])))
new_prediction = (new_prediction > 0.5)
