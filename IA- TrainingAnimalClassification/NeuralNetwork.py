import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Carregar o modelo salvo
model = load_model('V1Resnet50.h5')

# Definir as classes
class_names = ["Besouro", "Borboleta", "Gato", "Vaca", "Cachorro", "Elefante", "Gorila", 
               "Hipopótamo", "Lagarto", "Macaco", "Rato", "Panda", "Aranha", "Tigre", "Zebra"]

# Função para carregar e pré-processar a imagem
def preprocess_image(image_path, target_size):
    """
    Carrega uma imagem, redimensiona e normaliza para o modelo.
    Args:
        image_path (str): Caminho da imagem.
        target_size (tuple): Tamanho para redimensionamento (altura, largura).
    Returns:
        np.ndarray: Imagem pré-processada.
    """
    img = load_img(image_path, target_size=target_size)  # Carrega a imagem no tamanho especificado
    img_array = img_to_array(img)                       # Converte para array numpy
    img_array = img_array / 255.0                       # Normaliza os valores para [0, 1]
    img_array = np.expand_dims(img_array, axis=0)       # Adiciona uma dimensão para lote
    return img_array

# Função para fazer a previsão
def classify_image(image_path):
    """
    Classifica a imagem usando o modelo treinado.
    Args:
        image_path (str): Caminho da imagem.
    Returns:
        str: Classe prevista.
    """
    # Pré-processar a imagem
    img_array = preprocess_image(image_path, target_size=(224, 224))  # Ajustar o tamanho conforme o modelo

    # Fazer a previsão
    predictions = model.predict(img_array)
    
    # Obter a classe prevista
    predicted_label = class_names[np.argmax(predictions)]
    return predicted_label

# Caminho da imagem a ser classificada
image_path = 'processImage.jpeg'

# Classificar a imagem
predicted_class = classify_image(image_path)
print(f"A classe prevista é: {predicted_class}")
