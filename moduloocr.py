import pytesseract
from PIL import Image

'''Usando o pytesseract para ler o texto da imagem, e o PIL para abrir a imagem e transformar em texto e salvar em um arquivo de texto, crier um metodo que recebe o caminho da imagem e retorna o texto da imagem em um arquivo de texto corrigido '''

def ocr(path):
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang='por')
    return text

def save_text(text):
    with open('text.txt', 'w') as f:
        f.write(text)
    return 'text.txt'

def main():
    path = 'img.png'
    text = ocr(path)
    save_text(text)
    print('Texto salvo em text.txt')

if __name__ == '__main__':
    main()
