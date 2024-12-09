import React, { useState } from 'react';
import { Container, Typography, Box, Button, CircularProgress, Card, CardMedia } from '@mui/material';
import axios from 'axios';

function AnimalIdentifier() {
  const [image, setImage] = useState(null); // Armazena a imagem carregada
  const [animal, setAnimal] = useState(''); // Resultado do animal identificado
  const [loading, setLoading] = useState(false); // Controle de carregamento
  const [responseData, setResponseData] = useState(null); // Estado para armazenar o resultado da API

  // Função para enviar a imagem para o backend
  const handleSubmit = async () => {
    if (!image) {
      alert('Por favor, selecione uma imagem!');
      return;
    }

    // Cria um FormData para enviar a imagem
    const formData = new FormData();
    formData.append('image', image);

    try {
      // Envia a imagem para o servidor via POST
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Resposta da API:', response.data);
      //setResponseData(); // Armazena os dados da resposta no estado
      
      // Simula a identificação de um animal a partir da resposta da API
      setAnimal(response.data.pythonResult.animal); // Aqui você deve atualizar com o resultado real da sua API
    } catch (error) {
      console.error('Erro ao enviar a imagem:', error);
      setAnimal('Erro ao identificar o animal');
    }
  };

  // Manipula a seleção de arquivo
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImage(file); // Salva o arquivo selecionado
    }
  };

  // Função para identificar o animal (chama o handleSubmit para o upload)
  const identifyAnimal = async () => {
    setLoading(true);
    setAnimal(''); // Limpa o resultado anterior

    try {
      await handleSubmit(); // Chama o handleSubmit para enviar a imagem

      // Aqui você pode adicionar a lógica real de identificação, 
      // se necessário, após a imagem ser processada no backend.
    } catch (error) {
      setAnimal('Erro ao identificar o animal');
    }

    setLoading(false);
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Identificador de Animais 🐾
      </Typography>

      <Typography variant="body1" gutterBottom>
        Carregue uma imagem do animal que deseja identificar.
      </Typography>

      <Box sx={{ mt: 3, textAlign: 'center' }}>
        <Button
          variant="contained"
          component="label"
          sx={{ mb: 2 }}
        >
          Carregar Imagem
          <input
            type="file"
            accept="image/*"
            hidden
            onChange={handleImageUpload}
          />
        </Button>

        {image && (
          <Card sx={{ maxWidth: 300, mx: 'auto', mb: 2 }}>
            <CardMedia
              component="img"
              height="300"
              image={URL.createObjectURL(image)} // Cria uma URL temporária para a imagem
              alt="Imagem carregada"
            />
          </Card>
        )}

        <Box>
          <Button
            variant="contained"
            color="primary"
            onClick={identifyAnimal}
            disabled={!image || loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Identificar'}
          </Button>
        </Box>

        {animal && (
          <Typography variant="h6" color="secondary" sx={{ mt: 3 }}>
            Animal Identificado: {animal}
          </Typography>
        )}
      </Box>
    </Container>
  );
}

export default AnimalIdentifier;
