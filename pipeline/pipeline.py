# import library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow
from tensorflow import keras
from keras.callbacks import Callback, EarlyStopping
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense
import time, os

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from keras.regularizers import l2

def new_data():
    # Import path gambar
    train_dir = r"model/Face Images/Final Training Images"
    test_dir = r"model/Face Images/Final Testing Images"

    ### TRAIN MODEL ##
    # Praproses & augmentasi
    # Data augmentation dan data generator
    train_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='categorical'
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='categorical'
    )
    #-----------------------
    # Bangun model
    # Definisikan callback kustom untuk menghentikan pelatihan ketika akurasi > 96%
    class CustomEarlyStopping(Callback):
        def on_epoch_end(self, epoch, logs=None):
            if logs.get('val_accuracy') >= 0.96:
                print(f"\nAkurasi validasi mencapai {logs.get('val_accuracy') * 100:.2f}%, menghentikan pelatihan!")
                self.model.stop_training = True

    # Membangun model CNN
    Model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),  # Regularisasi L2
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.3),  # Dropout layer untuk mengurangi overfitting
        Dense(train_generator.num_classes, activation='softmax')
    ])


    # Kompilasi model
    Model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Menggunakan Early stopping untuk mengurangi waktu pelatihan
    call = CustomEarlyStopping()

    # Mengukur waktu yang dibutuhkan oleh model untuk melatih
    StartTime = time.time()

    # Melatih model
    history = Model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        validation_data=test_generator,
        validation_steps=test_generator.samples // test_generator.batch_size,
        epochs=20,
        callbacks=[call])

    Endtime = time.time()
    print('Total Training Time taken: ', round((Endtime - StartTime) / 60), 'Minutes')
    #######
    # Simpan model
    Model.save('../model/Model_Face_Recognition.h5')