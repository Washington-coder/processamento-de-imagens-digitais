import cv2
import math

def open_image(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

def find_min(image):
    min_val = 255
    for row in image:
        for pixel in row:
            if pixel < min_val:
                min_val = pixel
    return min_val

def find_max(image):
    max_val = 0
    for row in image:
        for pixel in row:
            if pixel > max_val:
                max_val = pixel
    return max_val

def expand_contrast(image, new_min, new_max):
    old_min = find_min(image)
    old_max = find_max(image)
    result = image.copy()
    for i in range(len(image)):
        for j in range(len(image[0])):
            result[i][j] = int((image[i][j] - old_min) * (new_max - new_min) / (old_max - old_min) + new_min)
    return result

def compress_expand(image, factor):
    result = image.copy()
    for i in range(len(image)):
        for j in range(len(image[0])):
            new_val = int(image[i][j] * factor)
            if new_val > 255:
                new_val = 255
            elif new_val < 0:
                new_val = 0
            result[i][j] = new_val
    return result

def sawtooth_transform(image, period):
    result = image.copy()
    for i in range(len(image)):
        for j in range(len(image[0])):
            result[i][j] = int((image[i][j] % period) * (255 / period))
    return result

def log_transform(image):
    result = image.copy()
    c = 255 / math.log(1 + find_max(image))
    for i in range(len(image)):
        for j in range(len(image[0])):
            result[i][j] = int(c * math.log(1 + image[i][j]))
    return result

def show_multiple_images(images, titles):
    for title, image in zip(titles, images):
        cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image = open_image('../images/lena.png')

if image is None:
    print("Erro ao carregar a imagem. Verifique o caminho.")
    exit()

contrasted_image = expand_contrast(image, 0, 255)
compressed_image = compress_expand(image, 0.5)
sawtooth_image = sawtooth_transform(image, 50)
log_image = log_transform(image)

images = [contrasted_image, compressed_image, sawtooth_image, log_image]
titles = ['Expansão de Contraste', 'Compressão', 'Dente de Serra', 'Transformada Logarítmica']
show_multiple_images(images, titles)
