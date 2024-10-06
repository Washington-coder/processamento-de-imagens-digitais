import cv2

def clarear_imagem(caminho_imagem):
    img = cv2.imread(caminho_imagem)
    
    img_original = img.copy()

    if img is None:
        print("Erro: Não foi possível carregar a imagem.")
        return

    altura, largura = img.shape[:2]
    
    clarity = int(input("Digite um valor para clarear a imagem: "))

    for x in range(largura):
        for y in range(altura):            
            pixel = img[x, y]
            
            B = int(pixel[0])
            G = int(pixel[1])
            R = int(pixel[2])
            
            
            # Adiciona o valor de claridade a cada canal
            B += clarity
            G += clarity
            R += clarity
            
            # Condições para evitar o overflow das cores
            if (R) > 255:
                R = 255
            if (G) > 255:
                G = 255
            if (B) > 255:
                B = 255
                
            img[x,y] = (B,G,R)

    cv2.imshow('Imagem original', img_original)
    cv2.imshow('Imagem Clareada', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

caminho_imagem = '../images/lena.png'

clarear_imagem(caminho_imagem)
