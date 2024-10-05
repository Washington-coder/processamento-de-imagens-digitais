import cv2
import numpy as np
import matplotlib.pyplot as plt

# Carregar a imagem em escala de cinza
imagem = cv2.imread('../images/low_contrast_lena.png')

# Encontrar o valor mínimo e máximo dos pixels da imagem
min_val = np.min(imagem)
max_val = np.max(imagem)

# Definir novos limites (0 a 255 para imagens de 8 bits)
L_min = 0
L_max = 255

# Aplicar a fórmula de expansão de contraste
imagem_expandida = (imagem - min_val) * ((L_max - L_min) / (max_val - min_val)) + L_min
imagem_expandida = imagem_expandida.astype(np.uint8)  # Converter para tipo uint8

# Exibir a imagem original e a imagem com contraste expandido
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(imagem)
plt.title('Imagem Original')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(imagem_expandida)
plt.title('Imagem com Contraste Expandido')
plt.axis('off')

plt.show()
