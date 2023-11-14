# Reconhecimento Óptico de Marcas (OMR) Avaliação Automática de Múltipla Escolha - OpenCV com Python
import cv2
import numpy as np
import utis  # Importe corrigido

###################################
# import form.js as form  # Importe removido, pois não está sendo utilizado
caminho = "cap1.png"
larguraImg = 700
alturaImg = 700
perguntas = 5
opcoes = 5
respostas_corretas = [1, 2, 0, 1, 4]
pontuacao = 0
webCamFeed = True
numero_camera = 1
###################################
cap = cv2.VideoCapture(numero_camera)
cap.set(10, 160)
while True:
    if webCamFeed:
        sucesso, img = cap.read()
    else:
        img = cv2.imread(caminho)

    img = cv2.imread(caminho)

    # Pré-processamento
    img = cv2.resize(img, (larguraImg, alturaImg))
    imgContornos = img.copy()
    imgFinal = img.copy()
    imgMaioresContornos = img.copy()
    imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgDesfoque = cv2.GaussianBlur(imgCinza, (5, 5), 1)
    imgCanny = cv2.Canny(imgDesfoque, 10, 50)
    # Encontrar Contornos
    contornos, hierarquia = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContornos, contornos, -1, (0, 255, 0), 10)

    # Encontrar Retângulo
    retanguloContorno = utis.rectContour(contornos)
    maiorContorno = utis.getCornerPoints(retanguloContorno[0])
    pontosNota = utis.getCornerPoints(retanguloContorno[1])

    if maiorContorno.size != 0 and pontosNota.size != 0:
        cv2.drawContours(imgMaioresContornos, maiorContorno, -1, (0, 255, 0), 20)
        cv2.drawContours(imgMaioresContornos, pontosNota, -1, (255, 0, 0), 20)
        maiorContorno = utis.reorder(maiorContorno)
        pontosNota = utis.reorder(pontosNota)

        pt1 = np.float32(maiorContorno)
        pt2 = np.float32([[0, 0], [larguraImg, 0], [0, alturaImg], [larguraImg, alturaImg]])
        matriz = cv2.getPerspectiveTransform(pt1, pt2)
        imgWarpColorida = cv2.warpPerspective(img, matriz, (larguraImg, alturaImg))

        ptG1 = np.float32(pontosNota)
        ptG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
        matrizG = cv2.getPerspectiveTransform(ptG1, ptG2)
        imgGradeDisplay = cv2.warpPerspective(img, matrizG, (325, 150))
        # cv2.imshow("Grade", imgGradeDisplay)

        # Aplicar Limiar
        imgWarpCinza = cv2.cvtColor(imgWarpColorida, cv2.COLOR_BGR2GRAY)
        imgLimiar = cv2.threshold(imgWarpCinza, 170, 255, cv2.THRESH_BINARY_INV)[1]

        caixas = utis.splitBoxes(imgLimiar)
        # cv2.imshow("Test", caixas[0])

        # Encontrar o número de cada caixa
        countR = 0
        countC = 0
        meuValorPixel = np.zeros((perguntas, opcoes))

        for imagem in caixas:
            totalPixels = cv2.countNonZero(imagem)
            meuValorPixel[countR][countC] = totalPixels
            countC += 1
            if (countC == opcoes): countR += 1; countC = 0

        # print(meuValorPixel)
        # Encontrar índice
        meuIndice = []
        for x in range(0, perguntas):
            arr = meuValorPixel[x]
            # print('arr',arr)
            meuIndiceVal = np.where(arr == np.amax(arr))
            # print('meuIndiceVal',meuIndiceVal[0])
            meuIndice.append(meuIndiceVal[0][0])
        # print(meuIndice)

        # Avaliação
        avaliacao = []
        for x in range(0, perguntas):
            if respostas_corretas[x] == meuIndice[x]:
                avaliacao.append(1)
            else:
                avaliacao.append(0)
        # print(avaliacao)
        pontuacao = (sum(avaliacao) / perguntas) * 100
        # print(pontuacao)

        # Mostrar Respostas
        imgResultado = imgWarpColorida.copy()
        imgResultado = utis.showAnswers(imgResultado, meuIndice, avaliacao, respostas_corretas, perguntas, opcoes)
        imgDesenhosCrus = np.zeros_like(imgWarpColorida)
        imgDesenhosCrus = utis.showAnswers(imgDesenhosCrus, meuIndice, avaliacao, respostas_corretas, perguntas, opcoes)
        invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
        imgInvWarp = cv2.warpPerspective(imgDesenhosCrus, invMatrix, (larguraImg, alturaImg))

        imgNotaCrus = np.zeros_like(imgGradeDisplay, np.uint8)
        cv2.putText(imgNotaCrus, str(int(pontuacao)) + "%", (70, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 3)
        imgNotaCrus = cv2.bitwise_not(imgNotaCrus)
        # cv2.imshow("Grade", imgNotaCrus)
        invMatrixG = cv2.getPerspectiveTransform(ptG2, ptG1)
        imgGradeDisplay = cv2.warpPerspective(imgNotaCrus, invMatrixG, (larguraImg, alturaImg))

        imgFinal = cv2.addWeighted(imgInvWarp, 1, img, 1, 0)
        imgFinal = cv2.addWeighted(imgFinal, 1, imgGradeDisplay, 1, 0)

    # Dividir a imagem
    imgVazia = np.zeros_like(img)
    imageArray = ([img, imgCinza, imgDesfoque, imgCanny],
                   [imgContornos, imgMaioresContornos, imgWarpColorida, imgResultado],
                   [imgContornos, imgMaioresContornos, imgInvWarp, imgFinal])
    labels = [["Original", "Cinza", "Desfoque", "Canny"],
              ["Contornos", "Maior Contorno", "Warp", "Limiar"],
              ["Resultado", "Maior Contorno", "Warp", "Resultado Final"]]

    imgEmpilhada = utis.stackImages(imageArray, 0.3, labels)

    cv2.imshow("Empilhamento de Imagens", imgEmpilhada)
    # cv2.imshow("Final", imgFinal)
    cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("TrabalhoFinal.jpg", imgFinal)
        cv2.waitKey(300)
