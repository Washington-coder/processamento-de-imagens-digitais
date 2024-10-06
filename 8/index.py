import cv2
import numpy as np
import matplotlib.pyplot as plt

# Função para quantizar a imagem (mesma da questão anterior)
def quantize_image(image, k):
    data = image.reshape((-1, 3))
    data = np.float32(data)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
    
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)
    quantized_image = centers[labels.flatten()]
    quantized_image = quantized_image.reshape(image.shape)
    
    return quantized_image

# Função para detectar bordas usando Canny
def detect_edges(image, low_threshold=30, high_threshold=100):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (3, 3), 1.0)
    edges = cv2.Canny(blurred_image, low_threshold, high_threshold)
    return edges

# Função para gerar as imagens de borda e interior
def generate_border_interior_images(image, edges):
    # Expande a máscara de borda para 3 canais
    edges_3ch = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Borda mantém a cor original, interior fica branco
    border_image = np.where(edges_3ch == [255, 255, 255], image, [255, 255, 255]).astype(np.uint8)
    
    # Interior mantém a cor original, borda fica branca
    interior_image = np.where(edges_3ch == [0, 0, 0], image, [255, 255, 255]).astype(np.uint8)
    
    return border_image, interior_image



# Função para calcular histogramas (para borda e interior)
def calculate_histogram(image, mask, num_colors):
    hist = cv2.calcHist([image], [0, 1, 2], mask, [num_colors, num_colors, num_colors], [0, 256, 0, 256, 0, 256])
    return hist.flatten()

# Função principal para extração de propriedades de cor usando BIC
def extract_bic_properties(image_path, num_colors=64, low_threshold=30, high_threshold=100):
    image = cv2.imread(image_path)

    # Reduz a quantidade de cores via quantização
    quantized_image = quantize_image(image, num_colors)

    edges = detect_edges(quantized_image, low_threshold, high_threshold)

    border_image, interior_image = generate_border_interior_images(quantized_image, edges)

    # Máscaras para borda e interior
    mask_border = edges == 255  # Borda
    mask_interior = edges == 0  # Interior

    # Calcula os histogramas de borda e interior
    hist_border = calculate_histogram(quantized_image, mask_border.astype(np.uint8), num_colors)
    hist_interior = calculate_histogram(quantized_image, mask_interior.astype(np.uint8), num_colors)

    # Salvando os histogramas como arquivos
    np.savetxt("hist_border.txt", hist_border, fmt="%.4f")
    np.savetxt("hist_interior.txt", hist_interior, fmt="%.4f")

    # Salvando as imagens de borda e interior
    cv2.imwrite("border_image.jpg", border_image)
    cv2.imwrite("interior_image.jpg", interior_image)

    # Exibe as imagens geradas
    cv2.imshow('Original Image', image)
    cv2.imshow('Quantized Image', quantized_image.astype(np.uint8))  # Certifique-se de que a imagem quantizada seja uint8
    cv2.imshow('Border Pixels Image', border_image)
    cv2.imshow('Interior Pixels Image', interior_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = '../images/lena.png'
extract_bic_properties(image_path, num_colors=64, low_threshold=30, high_threshold=100)