import cv2
import numpy as np
import random
import copy

def open_image(path):
    return cv2.imread(path)


def add_salt_and_pepper_noise(image, salt_prob, pepper_prob):
    noisy_image = copy.deepcopy(image)
    height, width = len(image), len(image[0])
    total_pixels = height * width

    # Adiciona sal
    num_salt = round(salt_prob * total_pixels)
    for _ in range(num_salt):
        i = random.randint(0, height - 1)
        j = random.randint(0, width - 1)
        noisy_image[i][j] = [255, 255, 255]  # Branco (sal)

    # Adiciona pimenta
    num_pepper = round(pepper_prob * total_pixels)
    for _ in range(num_pepper):
        i = random.randint(0, height - 1)
        j = random.randint(0, width - 1)
        noisy_image[i][j] = [0, 0, 0]  # Preto (pimenta)
    
    return noisy_image

def mean_filter(image, kernel_size):
    pad = kernel_size // 2
    height, width = len(image), len(image[0])
    
    # Inicializando a imagem de resultado com zeros
    result = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]

    # Aplicar o filtro da média para cada pixel
    for i in range(height):
        for j in range(width):
            sum_B, sum_G, sum_R = 0, 0, 0
            count = 0

            for m in range(-pad, pad + 1):
                for n in range(-pad, pad + 1):
                    # Coordenadas de vizinhança
                    x = min(max(i + m, 0), height - 1)
                    y = min(max(j + n, 0), width - 1)

                    # Somar os valores dos canais B, G, R
                    pixel = image[x][y]
                    sum_B += int(pixel[0])  # Canal B
                    sum_G += int(pixel[1])  # Canal G
                    sum_R += int(pixel[2])  # Canal R
                    count += 1

            result[i][j][0] = min(255, max(0, sum_B // count))  # Canal B
            result[i][j][1] = min(255, max(0, sum_G // count))  # Canal G
            result[i][j][2] = min(255, max(0, sum_R // count))  # Canal R

    return result


def median_filter(image, kernel_size):
    pad = kernel_size // 2
    height, width = image.shape
    result = np.zeros((height, width), dtype=np.uint8)

    # Aplicar o filtro da mediana
    for i in range(height):
        for j in range(width):
            values = []
            for m in range(-pad, pad + 1):
                for n in range(-pad, pad + 1):
                    x = min(max(i + m, 0), height - 1)
                    y = min(max(j + n, 0), width - 1)
                    values.append(image[x, y])
            result[i, j] = int(np.median(values))  # Mediana

    return result

def mode_filter(image, kernel_size):
    pad = kernel_size // 2
    height, width = image.shape
    result = np.zeros((height, width), dtype=np.uint8)

    # Aplicar o filtro da moda
    for i in range(height):
        for j in range(width):
            values = []
            for m in range(-pad, pad + 1):
                for n in range(-pad, pad + 1):
                    x = min(max(i + m, 0), height - 1)
                    y = min(max(j + n, 0), width - 1)
                    values.append(image[x, y])
            # Encontrar o valor da moda (mais frequente)
            mode_value = max(set(values), key=values.count)
            result[i, j] = mode_value
            
    return result

def show_multiple_images(images, titles):
    for idx, (title, image) in enumerate(zip(titles, images)):
        # Converte a imagem para um array NumPy, se necessário
        if isinstance(image, list):  # Se for uma lista, converta para NumPy
            image = np.array(image, dtype=np.uint8)
        
        cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Carregar a imagem e adicionar ruído
image = open_image('../images/lena.png')  # Substitua pelo caminho da sua imagem
noisy_image = add_salt_and_pepper_noise(image, 0.1, 0.1)

# Aplicar os filtros
mean_filtered_image = mean_filter(noisy_image, 3)
# median_filtered_image = median_filter(noisy_image, 3)
# mode_filtered_image = mode_filter(noisy_image, 3)

# Mostrar as imagens
images = [noisy_image, mean_filtered_image]
titles = ['Imagem original com uuído sal e pimenta', 'mean_filtered_image']
show_multiple_images(images, titles)
