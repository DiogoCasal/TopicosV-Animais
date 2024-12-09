const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const { exec } = require('child_process');

// Inicializando o Express
const app = express();

app.use(cors());

const PORT = 5000;

// Função para rodar o arquivo Python e pegar a resposta
function executarPython() {
  return new Promise((resolve, reject) => {
    // Caminho para o script Python
    const pythonScriptPath = './NeuralNetwork.py';
    
    // Comando para executar o Python com o arquivo
    exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
      if (error) {
        reject(`Erro ao executar o script Python: ${error.message}`);
        return;
      }
      if (stderr) {
        reject(`Erro no script Python: ${stderr}`);
        return;
      }
      
      // Se tudo correr bem, resolvemos a promessa com a saída do script
      try {
        const result = JSON.parse(stdout);  // O stdout será o JSON gerado pelo Python
        resolve(result);
      } catch (err) {
        reject('Erro ao processar a resposta do Python');
      }
    });
  });
}

// Configuração do Multer para salvar as imagens
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // Caminho onde a imagem será salva no servidor
    cb(null, './');
  },
  filename: (req, file, cb) => {
    // Nome do arquivo (aqui renomeamos a imagem para garantir que seja única)
    cb(null, "processImage.jpg");
  },
});

// Configuração do multer para aceitar apenas imagens
const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Arquivo não é uma imagem'), false);
    }
  },
});

// Rota para receber o upload da imagem
app.post('/upload', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('Nenhum arquivo foi enviado.');
  }

  try {
    // Chama a função para executar o script Python e espera o resultado
    const responsePython = await executarPython();

    // Envia uma resposta confirmando que a imagem foi recebida e salva, junto com a resposta do Python
    res.status(200).json({
      message: 'Imagem enviada e script Python executado com sucesso!',
      file: req.file,
      pythonResult: responsePython,  // Envia o resultado do Python
    });
  } catch (error) {
    console.error('Erro ao executar o Python:', error);
    res.status(500).json({ message: 'Erro ao processar a imagem e o script Python' });
  }
});

// Rota para lidar com erros do multer
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    return res.status(500).send('Erro ao processar o arquivo');
  }
  res.status(500).send(err.message);
});

// Inicializando o servidor
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});