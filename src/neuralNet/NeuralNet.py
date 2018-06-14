import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.layers import Dense, LSTM, Embedding
from keras.models import Sequential
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

trainFilename = 'C:\\Users\\David\\PycharmProjects\\BitcoinAlchemist\\src\\database\\train.csv'
targetFilename = 'C:\\Users\\David\\PycharmProjects\\BitcoinAlchemist\\src\\database\\target.csv'

np.random.seed(69)

trainData = pd.read_csv(trainFilename)
trainColumns = trainData.columns.values
targetData = pd.read_csv(targetFilename)
targetColumns = targetData.columns.values


predictors = (trainData[trainColumns[3:7]]).values
target = (targetData[targetColumns[3]]).values

X_train, X_test, y_train, y_test = train_test_split(predictors, target, test_size=0.2)

batch_size = int(len(X_train) / 1000)

print('Loading data...')
print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')


print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)

print('Build model...')
model = Sequential()
model.add(Dense(1000, activation='relu', input_shape=X_train.shape[1:]))
model.add(Dense(100, activation='relu'))
model.add(Dense(10, activation='relu'))

# Output layer
model.add(Dense(1))



model.compile(
                loss='mse',
                optimizer='adam'
             )

print("Train...")
model.fit(
                X_train, y_train,
                batch_size=batch_size,
                epochs=3,
                validation_data=(X_test, y_test)
          )

score = model.evaluate(
                            X_test, y_test,
                            batch_size=batch_size, verbose=1
                      )

print('Test score: ', score)













#n_cols = predictors.shape[1] # Size of columns in the input

#def get_new_model():
    # Specify the model
#    model = Sequential()
#    model.add(Dense(100, activation='relu', input_shape=(n_cols, )))
#    model.add(Dense(100, activation='relu'))

    # Output layer
#    model.add(Dense(1))
#    return model



# TODO Optimize better





# Define early_stopping_monitor
#early_stopping_monitor = EarlyStopping(patience=2)

#model_1 = get_new_model()

#model_1.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

# Fit model_1
#model_1_training = model_1.fit(predictors, target, epochs=3, validation_split=0.2) #, callbacks=[early_stopping_monitor])

# Create the plot
#plt.plot(model_1_training.history['val_acc'], 'r')
#plt.xlabel('Epochs')
#plt.ylabel('Validation score')
#plt.show()

#x = predictors[0]
#print(model_1.predict(np.array([x]))[0][0])






# Create list of learning rates: lr_to_test
#lr_to_test = [.000001, 0.01, 1]

# Loop over learning rates
#for lr in lr_to_test:
    #print('\n\nTesting model with learning rate: %f\n'%lr)

    # Build new model to test, unaffected by previous models
    #model = get_new_model()

    # Create SGD optimizer with specified learning rate: my_optimizer
    #my_optimizer = SGD(lr=lr)

    # Compile the model
    #model.compile(optimizer=my_optimizer, loss='mse', metrics=['accuracy'])

    # Fit the model
    #model.fit(predictors, target, validation_split=0.3)
























# Compile the model
#model.compile(optimizer='adam', loss='mean_squared_error')

# Fit the model
#model.fit(predictors, target, epochs=100, batch_size=500)
#x = predictors[0]

#print(x)
#print(model.predict(np.array([x]))[0][0])
