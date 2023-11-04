import pytesseract
from PIL import Image


imagem_prova = Image.open('prova.jpg')

# Realizar a extração de texto com Tesseract OCR
texto_extraido = pytesseract.image_to_string(imagem_prova)

# Imprimir o texto extraído
print(texto_extraido)
