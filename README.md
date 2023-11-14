# prototipo

## Optical Mark Recognition (OMR) MCQ Automated Grading - OpenCV with Python

Este projeto utiliza técnicas de reconhecimento óptico de marcas (OMR) para automatizar a correção de questões de múltipla escolha (MCQ) em imagens, implementado em Python com a biblioteca OpenCV.

### Descrição

O sistema é projetado para processar imagens contendo folhas de respostas de questões de múltipla escolha. Ele realiza as seguintes etapas principais:

1. **Pré-processamento da Imagem:**
   - Redimensionamento da imagem.
   - Conversão para escala de cinza.
   - Aplicação de desfoque gaussiano.
   - Detecção de bordas usando o algoritmo Canny.

2. **Localização dos Contornos e Retângulo Envolvente:**
   - Identificação dos contornos presentes na imagem.
   - Filtragem dos contornos com base na área e na forma.
   - Ordenação dos contornos encontrados.

3. **Transformação de Perspectiva:**
   - Identificação dos pontos de canto no retângulo envolvente.
   - Reordenação dos pontos de canto para garantir a correta transformação de perspectiva.
   - Aplicação da transformação de perspectiva para obter uma visão frontal da folha de respostas.

4. **Segmentação das Caixas de Respostas:**
   - Aplicação de limiar para segmentar as caixas de respostas.
   - Divisão da imagem em regiões correspondentes às diferentes caixas de resposta.

5. **Avaliação Automática:**
   - Contagem dos pixels não nulos em cada caixa de resposta.
   - Identificação da opção escolhida em cada questão com base na contagem de pixels.
   - Comparação com as respostas corretas para calcular a pontuação.

6. **Visualização dos Resultados:**
   - Destaque das respostas corretas e incorretas na imagem original.
   - Geração de uma imagem final com as marcações de correção.

### Como Usar

1. Certifique-se de ter o Python instalado em seu sistema.
2. Instale as bibliotecas necessárias usando o seguinte comando:

   ```bash
   pip install opencv-python numpy
   ```

3. Execute o script Python fornecido:

   ```bash
   python nome_do_script.py
   ```

4. Siga as instruções na interface do usuário para usar a câmera ou fornecer o caminho para a imagem.

5. A pontuação e as marcações de correção serão exibidas na imagem final.

### Estrutura do Projeto

- **`nome_do_script.py`**: O script principal que implementa o processo de OMR.
- **`utils.py`**: Módulo contendo funções utilitárias, como a organização de pontos, detecção de contornos, entre outras.
- **`form.js`**: [REMOVIDO] Módulo não utilizado no projeto.

### Requisitos do Sistema

- Python 3.x
- OpenCV
- NumPy

### Contribuições e Melhorias

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas, fornecer feedback ou enviar solicitações de pull para melhorar este projeto.

Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).
