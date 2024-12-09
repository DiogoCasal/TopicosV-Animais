from cx_Freeze import setup, Executable

executables = [Executable('NeuralNetwork.py')]

setup(name='NeuralNetwork',
      version='1.0',
      description='Programa executavel de uma rede neural treinada para identificacao de alguns animais',
      executables=executables)