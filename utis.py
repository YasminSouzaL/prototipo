import cv2
import numpy as np

def stackImages(imgArray, escala, rotulos=[]):
    linhas = len(imgArray)
    colunas = len(imgArray[0])
    linhasDisponiveis = isinstance(imgArray[0], list)

    largura = imgArray[0][0].shape[1]
    altura = imgArray[0][0].shape[0]

    if linhasDisponiveis:
        for x in range(0, linhas):
            for y in range(0, colunas):
                imgArray[x][y] = cv2.resize(imgArray[x][y],
                                            (0, 0), None, escala, escala)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
                if len(imgArray[x][y].shape) == 3:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_RGB2BGR)
        imagemBranca = np.zeros((altura, largura, 3), np.uint8)
        hor = [imagemBranca]*linhas
        hor_con = [imagemBranca]*linhas
        for x in range(0, linhas):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, linhas):
            imgArray[x] = cv2.resize(imgArray[x],
                                     (0, 0), None, escala, escala)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(
                    imgArray[x], cv2.COLOR_GRAY2BGR)
            if len(imgArray[x].shape) == 3:
                imgArray[x] = cv2.cvtColor(
                    imgArray[x], cv2.COLOR_RGB2BGR)
        hor = np.hstack(imgArray)
        hor_con = np.concatenate(imgArray)
        ver = hor
    if len(rotulos) != 0:
        larguraCadaImagem = int(ver.shape[1]/colunas)
        alturaCadaImagem = int(ver.shape[0]/linhas)
        for d in range(0, linhas):
            for c in range(0, colunas):
                cv2.rectangle(ver, (c*larguraCadaImagem, alturaCadaImagem*d),
                              (c*larguraCadaImagem+len(rotulos[d])*13+27, 30+alturaCadaImagem*d), (255, 255, 255), cv2.FILLED)
                cv2.putText(ver, rotulos[d], (larguraCadaImagem*c+10, alturaCadaImagem*d+20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2) 
    return ver

def rectContour(contornos):
    rectCon = []
    max_area = 0
    for i in contornos:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*peri, True) 
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.02*peri, True)
    return approx

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

def splitBoxes(img):
    linhas = np.vsplit(img, 5)
    caixas = []
    for r in linhas:
        colunas = np.hsplit(r, 5)
        for caixa in colunas:
            caixas.append(caixa)
    return caixas

def drawGrid(img, perguntas=5, opcoes=5):
    secW = int(img.shape[1]/perguntas)
    secH = int(img.shape[0]/opcoes)
    for i in range(0, 5):
        pt1 = (0, secH*i)
        pt2 = (img.shape[1], secH*i)
        pt3 = (secW*i, 0)
        pt4 = (secW*i, img.shape[0])
        cv2.line(img, pt1, pt2, (255, 0, 0), 2)
        cv2.line(img, pt3, pt4, (255, 0, 0), 2)
    return img

def showAnswers(img, meuIndice, avaliacao, ans, perguntas=5, opcoes=5):
    secW = int(img.shape[1] / perguntas)
    secH = int(img.shape[0] / opcoes)
    for x in range(0, perguntas):
        minhaResposta = meuIndice[x]
        cX = (minhaResposta * secW) + secW // 2
        cY = (x * secH) + secH // 2
        if avaliacao[x] == 1:
            minhaCor = (0, 255, 0)
        else:
            minhaCor = (0, 0, 255)
            respostaCorreta = ans[x]
            cv2.circle(img, (respostaCorreta * secW + secW // 2, (x * secH) + secH // 2), 30, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (cX, cY), 50, minhaCor, cv2.FILLED)
    return img
