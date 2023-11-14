## Descrição

Este projeto utiliza Python, OpenCV, MediaPipe e a biblioteca pydirectinput para criar um sistema de controle de jogo baseado no rastreamento de pose do usuário. O software usa a câmera para detectar a pose do jogador e traduzir movimentos específicos (como pular e agachar) em comandos de teclado para controlar um jogo.

## Funcionalidades

- **Rastreamento de Movimento**: Utiliza a câmera para rastrear a pose do jogador em tempo real.
- **Controle de Jogo**: Traduz movimentos do corpo em comandos de teclado.
- **Calibração Dinâmica**: Permite ao usuário calibrar os limiares de detecção de movimento (pulo e agachamento).

## Requisitos

- Python 3.x
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)
- pydirectinput

## Instalação

Assegure-se de ter o Python 3 instalado em sua máquina. Instale as dependências utilizando pip:

```bash
pip install opencv-python mediapipe pydirectinput
```

## Uso

Para executar o programa, inicie o script Python. O programa utilizará a câmera padrão do sistema para rastrear a pose do usuário. Movimentos específicos serão traduzidos em comandos de teclado para controlar um jogo.

- **Pular**: Detectado quando o nariz do usuário fica abaixo de um certo limiar de altura.
- **Agachar**: Detectado quando o nariz do usuário ultrapassa um certo limiar de altura.
- **Movimento Lateral**: Detectado pelo posicionamento das mãos em relação aos ombros.

Use a tecla 'q' para recalibrar a altura do nariz durante o uso.

## Configuração

Você pode ajustar as constantes no início do script para calibrar a sensibilidade e os limiares de detecção de movimento.

## Contribuições

- https://github.com/NoxusJr
- https://github.com/KeaKzinho
- https://github.com/FernandoIzidio

## Licença

Este projeto está sob licença MIT. 
