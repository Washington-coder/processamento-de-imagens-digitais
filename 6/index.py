import cv2
import numpy as np

def open_image(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

def add_salt_and_pepper_noise(image, salt_prob, pepper_prob):
    noisy_image = np.copy(image)
    total_pixels = image.size

    # Adiciona sal
    num_salt = round(salt_prob * total_pixels)
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 255  # Pixels brancos (sal)

    # Adiciona pimenta
    num_pepper = round(pepper_prob * total_pixels)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 0  # Pixels pretos (pimenta)
    
    return noisy_image

def mean_filter(image, kernel_size):
    pad = kernel_size // 2
    height, width = image.shape
    result = np.zeros((height, width), dtype=np.uint8)

    # Aplicar o filtro da média
    for i in range(height):
        for j in range(width):
            sum_pixels = 0
            count = 0
            for m in range(-pad, pad + 1):
                for n in range(-pad, pad + 1):
                    x = min(max(i + m, 0), height - 1)
                    y = min(max(j + n, 0), width - 1)
                    pixel = int(image[x, y])
                    sum_pixels += pixel
                    count += 1
            if sum_pixels // count > 255:
                result[i, j] = 255
            else:
                result[i, j] = sum_pixels // count  # Média
                    

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
        cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Carregar a imagem e adicionar ruído
image = open_image('../images/lena.png')  # Substitua pelo caminho da sua imagem
noisy_image = add_salt_and_pepper_noise(image, 0.01, 0.01)

# Aplicar os filtros
mean_filtered_image = mean_filter(noisy_image, 3)
median_filtered_image = median_filter(noisy_image, 3)
mode_filtered_image = mode_filter(noisy_image, 3)

# Mostrar as imagens
images = [noisy_image, mean_filtered_image, median_filtered_image, mode_filtered_image]
titles = ['Imagem Original com Ruído', 'Filtro da Média', 'Filtro da Mediana', 'Filtro da Moda']
show_multiple_images(images, titles)
