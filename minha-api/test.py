# identificar_animal.py
import sys
import json

# Simulação de identificação de animal
animal = "Cachorroaaaa"  # Você pode colocar a lógica de identificação real aqui

# Enviando a resposta como JSON
print(json.dumps({"animal": animal}))
sys.exit(0)