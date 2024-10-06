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
                    sum_B += int(pixel[0])
                    sum_G += int(pixel[1])
                    sum_R += int(pixel[2])
                    count += 1

            result[i][j][0] = min(255, max(0, sum_B // count))
            result[i][j][1] = min(255, max(0, sum_G // count))
            result[i][j][2] = min(255, max(0, sum_R // count))

    return result


def median_filter(image, kernel_size):
    pad = kernel_size // 2
    height, width = len(image), len(image[0])
    
    # Inicializando a imagem de resultado com zeros
    result = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]

    # Aplicar o filtro da mediana para cada pixel
    for i in range(height):
        for j in range(width):
            # Listas para armazenar os valores dos canais R, G, B
            red_values = []
            green_values = []
            blue_values = []

            for m in range(-pad, pad + 1):
                for n in range(-pad, pad + 1):
                    # Coordenadas de vizinhança
                    x = min(max(i + m, 0), height - 1)
                    y = min(max(j + n, 0), width - 1)

                    # Adiciona os valores dos canais
                    pixel = image[x][y]
                    blue_values.append(pixel[0])
                    green_values.append(pixel[1])
                    red_values.append(pixel[2])

            # Calcula a mediana para cada canal
            result[i][j][0] = sorted(blue_values)[len(blue_values) // 2] 
            result[i][j][1] = sorted(green_values)[len(green_values) // 2]
            result[i][j][2] = sorted(red_values)[len(red_values) // 2]

    return result


def mode_filter(image, kernel_size):
    pad = kernel_size // 2
    height, width = len(image), len(image[0])
    
    # Inicializando a imagem de resultado
    result = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]

    # Aplicar o filtro da moda para cada pixel
    for i in range(height):
        for j in range(width):
            red_values = []
            green_values = []
            blue_values = []

            for m in range(-pad, pad + 1):
                for n in range(-pad, pad + 1):
                    # Coordenadas de vizinhança
                    x = min(max(i + m, 0), height - 1)
                    y = min(max(j + n, 0), width - 1)

                    # Adiciona os valores dos canais
                    pixel = image[x][y]
                    blue_values.append(pixel[0])
                    green_values.append(pixel[1])
                    red_values.append(pixel[2])

            # Encontrar a moda para cada canal
            result[i][j][0] = max(set(blue_values), key=blue_values.count)
            result[i][j][1] = max(set(green_values), key=green_values.count)
            result[i][j][2] = max(set(red_values), key=red_values.count)

    return result


def show_multiple_images(images, titles):
    for idx, (title, image) in enumerate(zip(titles, images)):
        # Converte a imagem para um array NumPy, se necessário
        if isinstance(image, list):
            image = np.array(image, dtype=np.uint8)
        cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image = open_image('../images/lena.png')
noisy_image = add_salt_and_pepper_noise(image, 0.05, 0.05)

# Aplicar os filtros
mean_filtered_image = mean_filter(noisy_image, 3)
median_filtered_image = median_filter(noisy_image, 3)
mode_filtered_image = mode_filter(noisy_image, 3)

# Mostrar as imagens
images = [noisy_image, mean_filtered_image, median_filtered_image, mode_filtered_image]
titles = ['Imagem original com ruído sal e pimenta', 'Filtro da media', 'Filtro da mediana', 'Filtro da moda']
show_multiple_images(images, titles)
