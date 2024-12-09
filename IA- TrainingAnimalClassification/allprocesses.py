# Common
from multiprocessing import Pool
import os
import time
from glob import glob
import tensorflow as tf
from IPython.display import clear_output as cls
from keras.preprocessing.image import ImageDataGenerator
# Modelo
from keras.models import Sequential
from keras.layers import GlobalAvgPool2D as GAP, Dense, Dropout
# Callbacks
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.applications import ResNet50V2

def ProcessinPlusTraining(args):
    # Nome das Classes
    root_path = 'S:/Desktop/TrainingAnimalClassification/data/Training_Data/'
    class_names = sorted(os.listdir(root_path))
    n_classes = len(class_names)

    # Nome das Classes
    valid_path = 'S:/Desktop/TrainingAnimalClassification/data/Validation_Data/'

    # Inicializa o gerador e aplica o preprocessamento na base de treinamento
    preproceessedtrain = ImageDataGenerator(
        rescale=1/255.,
        rotation_range=args[0],
        horizontal_flip=True,
        shear_range=args[1],
        zoom_range=args[2],
        width_shift_range=args[3],
        height_shift_range=args[4],
        brightness_range=[0.8, 1.2],
        channel_shift_range=args[5],
    )

    validationdata = ImageDataGenerator(rescale=1/255.)

    # Carregar os dados preprocessados para a database de treinamento
    train_ds = preproceessedtrain.flow_from_directory(
        root_path, class_mode='binary', target_size=(256, 256), shuffle=True, batch_size=32)
    valid_ds = validationdata.flow_from_directory(
        valid_path, class_mode='binary', target_size=(256, 256), shuffle=True, batch_size=32)

    with tf.device("/GPU:0"):
        base_model = ResNet50V2(input_shape=(256, 256, 3), include_top=False)
        base_model.trainable = False
        cls()

        # Arquitetura do modelo ResNet50
        name = args[6]
        model = Sequential([
            base_model,
            GAP(),
            Dense(256, activation='relu', kernel_initializer='he_normal'),
            Dropout(0.2),
            Dense(n_classes, activation='softmax')
        ], name=name)

        # Callbacks
        cbs = [EarlyStopping(patience=3, restore_best_weights=True), ModelCheckpoint(
            name + ".h5", save_best_only=True)]

        # Modelo
        opt = tf.keras.optimizers.Adam(learning_rate=2e-3)
        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer=opt, metrics=['accuracy'])

        # Treinamento
        history = model.fit(
            train_ds, validation_data=valid_ds, callbacks=cbs, epochs=1)
if __name__ == '__main__':
    

    # Chama a funcao de preprocessamento e treino com os parametros diferentes para preprocessar
    matrixArgs = [
        [30, 0.1, 0.2, 0.1, 0.1, 20, "V1Resnet50"],
        [60, 0.25, 0.6, 0.3, 0.3, 30, "V2Resnet50"],
        [90, 0.4, 0.2, 0.8, 0.8, 40, "V3Resnet50"]
    ]

    with Pool(5) as p:
        print(p.map(ProcessinPlusTraining, matrixArgs))
    # ProcessinPlusTraining(10, 0.2, 0.2, 0.2, 0.2, 20)
