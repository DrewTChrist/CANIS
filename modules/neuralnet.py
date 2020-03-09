"""Module for building, training, and loading project neural networks."""
import os
import tensorflow.keras as keras


class Evaluator:

    def __init__(self, model):
        self.path = os.path.join(os.path.curdir, "./saved_models/" + model)
        self.model = keras.models.Sequential()

        # If an existing model of the same name is found, automatically load it
        if os.path.isfile(self.path):
            self.model = keras.models.load_model(self.path)
        else:
            self.model = keras.models.Sequential([
                keras.layers.Flatten(),
                keras.layers.Dense(1000, activation='relu'),
                keras.layers.Dense(1000, activation='relu'),
                keras.layers.Dense(1000, activation='relu'),
                keras.layers.Dense(2, activation='softmax')
            ])
            self.model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    #def __del__(self):
        # This is meant to auto-save the model upon quitting the program.
        # However, until the model is able to be trained, this code must stay
        # commented, otherwise Tensorflow throws an exception. An empty,
        # untrained model is not allowed to be saved.
        #self.model.save(self.path)

    def train(self, plot, fitness):
        # TODO: Prepare training data, or a method for manual user training
        self.model.fit(plot, fitness)

    def predict(self, candidate):
        # Returns a probability between 0 and 1 that the candidate represents
        # a good pattern to use
        return self.model.predict(candidate)
