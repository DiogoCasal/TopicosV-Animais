#Teste para uma imagem
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import json
import sys

# Class Names
class_names = ["Besouro","Borboleta","Gato","Vaca","Cachorro","Elefante","Gorila","Hipopótamo","Lagarto","Macaco","Rato","Panda","Aranha","Tigre","Zebra"]

# Carrega a imagem e redimensiona
img = image.load_img('processImage.jpg', target_size=(256, 256, 3))

# Normaliza a imagem
img_array = image.img_to_array(img)
img_array /= 255.

# Cria um objeto EagerTensor a partir da imagem normalizada
img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)

# Adiciona uma dimensão extra para o modelo
img_tensor = tf.expand_dims(img_tensor, axis=0)

# Carrega o modelo
model = load_model('./ResNet50V2.h5')

# Faz a predição na imagem
predictions = model.predict(img_tensor, verbose=0)

# Converte a saída para um rótulo de texto
predicted_label = class_names[np.argmax(predictions)]


# result = "O animal é um(a) " + predicted_label

print(json.dumps({"animal": predicted_label}))
sys.exit(0)