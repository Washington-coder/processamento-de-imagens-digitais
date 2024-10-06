import cv2
import numpy as np

# Função para quantizar a imagem
def quantize_image(image, k):
    data = image.reshape((-1, 3))
    data = np.float32(data)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
    
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)
    quantized_image = centers[labels.flatten()]
    quantized_image = quantized_image.reshape(image.shape)
    
    return quantized_image

# Função para aplicar filtro Gaussiano
def apply_gaussian_blur(image, kernel_size=3):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 1.0)

# Função para calcular gradiente com Sobel
def calculate_gradient(image):
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    
    # Normalizando o gradiente para intensificar bordas
    gradient_magnitude = np.uint8(np.clip(gradient_magnitude * 255.0 / gradient_magnitude.max(), 0, 255))
    
    gradient_direction = np.arctan2(sobel_y, sobel_x)
    return gradient_magnitude, gradient_direction

# Supressão de não-máximos
def non_max_suppression(gradient_magnitude, gradient_direction):
    rows, cols = gradient_magnitude.shape
    suppressed_image = np.zeros((rows, cols), dtype=np.uint8)

    gradient_direction = np.rad2deg(gradient_direction)
    gradient_direction[gradient_direction < 0] += 180

    for i in range(1, rows-1):
        for j in range(1, cols-1):
            angle = gradient_direction[i, j]
            value = gradient_magnitude[i, j]

            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                neighbors = (gradient_magnitude[i, j-1], gradient_magnitude[i, j+1])
            elif 22.5 <= angle < 67.5:
                neighbors = (gradient_magnitude[i-1, j+1], gradient_magnitude[i+1, j-1])
            elif 67.5 <= angle < 112.5:
                neighbors = (gradient_magnitude[i-1, j], gradient_magnitude[i+1, j])
            else:
                neighbors = (gradient_magnitude[i-1, j-1], gradient_magnitude[i+1, j+1])

            if value >= max(neighbors):
                suppressed_image[i, j] = value

    return suppressed_image

# Função para aplicar histerese (thresholding)
def hysteresis_thresholding(image, low_threshold, high_threshold):
    rows, cols = image.shape
    result = np.zeros((rows, cols), dtype=np.uint8)

    strong_pixel = 255
    weak_pixel = 75

    strong_i, strong_j = np.where(image >= high_threshold)
    weak_i, weak_j = np.where((image >= low_threshold) & (image < high_threshold))

    result[strong_i, strong_j] = strong_pixel
    result[weak_i, weak_j] = weak_pixel

    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if result[i, j] == weak_pixel:
                if (result[i+1, j-1] == strong_pixel or result[i+1, j] == strong_pixel or
                    result[i+1, j+1] == strong_pixel or result[i, j-1] == strong_pixel or
                    result[i, j+1] == strong_pixel or result[i-1, j-1] == strong_pixel or
                    result[i-1, j] == strong_pixel or result[i-1, j+1] == strong_pixel):
                    result[i, j] = strong_pixel
                else:
                    result[i, j] = 0

    return result

def canny_edge_detection(image, low_threshold=30, high_threshold=100):
    # Passo 1: Aplicar filtro Gaussiano
    blurred_image = apply_gaussian_blur(image)

    # Passo 2: Calcular gradiente e direção
    gradient_magnitude, gradient_direction = calculate_gradient(blurred_image)

    # Passo 3: Supressão de Não-Máximos
    non_max_image = non_max_suppression(gradient_magnitude, gradient_direction)

    # Passo 4: Aplicar Histerese
    edges = hysteresis_thresholding(non_max_image, low_threshold, high_threshold)

    return edges

# Função principal para detecção de bordas com quantização
def edge_detection_with_quantization(image_path, num_colors=64, low_threshold=30, high_threshold=100):
    
    image = cv2.imread(image_path)
    
    # Reduz a quantidade de cores via quantização
    quantized_image = quantize_image(image, num_colors)
    
    # Converte para escala de cinza (necessário para o algoritmo de Canny)
    gray_image = cv2.cvtColor(quantized_image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar o algoritmo Canny
    edges = canny_edge_detection(gray_image, low_threshold, high_threshold)
    
    cv2.imshow('Original Image', image)
    cv2.imshow('Quantized Image', quantized_image)
    cv2.imshow('Edges Detected', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = '../images/lena.png'
edge_detection_with_quantization(image_path, num_colors=64, low_threshold=20, high_threshold=50)
