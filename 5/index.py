import cv2
import math

def open_image(path):
    return cv2.imread(path)

def get_values_for_overflow(B, G, R):
    if B > 255:
        B = 255
    if G > 255:
        G = 255
    if R > 255:
        R = 255
        
    return B, G, R

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
    old_min = int(find_min(image))
    old_max = int(find_max(image))
    result = image.copy()
    for i in range(len(image)):
        for j in range(len(image[0])):
            pixel = int(image[i][j])
            new_pixel = int((pixel - old_min) * (new_max - new_min) / (old_max - old_min) + new_min)
            if new_pixel >= 255:
                new_pixel = 255
            result[i][j] = new_pixel
    return result

def compress_expand(image, factor):
    result = image.copy()
    
    altura, largura = image.shape[:2]
    
    for i in range(altura):
        for j in range(largura):
            pixel = image[i][j]
            
            B = int(pixel[0]) * factor
            G = int(pixel[1]) * factor
            R = int(pixel[2]) * factor
            
            B, G, R = get_values_for_overflow(B, G, R)
            
            result[i][j] = B, G, R
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

compressed_image = compress_expand(image, 0.5)
# contrasted_image = expand_contrast(compressed_image, 0, 255)
# sawtooth_image = sawtooth_transform(image, 50)
# log_image = log_transform(image)

images = [compressed_image]
titles = ['Compressão']
show_multiple_images(images, titles)
