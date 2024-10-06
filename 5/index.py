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
            # Acessa cada canal (B, G, R) do pixel
            for channel in pixel:
                if channel < min_val:
                    min_val = channel
    return min_val

def find_max(image):
    max_val = 0
    for row in image:
        for pixel in row:
            # Acessa cada canal (B, G, R) do pixel
            for channel in pixel:
                if channel > max_val:
                    max_val = channel
    return max_val


def expand_contrast(image, new_min, new_max):
    altura, largura = image.shape[:2]
    
    # Encontrar o valor mínimo e máximo de todos os canais
    old_min = find_min(image)
    old_max = find_max(image)
    
    old_min = int(old_min)
    old_max = int(old_max)
    
    result = image.copy()
    
    for i in range(altura):
        for j in range(largura):
            pixel = image[i][j]
            
            B = int(pixel[0])
            G = int(pixel[1])
            R = int(pixel[2])
            
            # Expande o contraste para cada canal
            B = int((B - old_min) * (new_max - new_min) / (old_max - old_min) + new_min)
            G = int((G - old_min) * (new_max - new_min) / (old_max - old_min) + new_min)
            R = int((R - old_min) * (new_max - new_min) / (old_max - old_min) + new_min)
            
            B, G, R = get_values_for_overflow(B, G, R)
            
            result[i][j] = [B, G, R]
    
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
    altura, largura = image.shape[:2]
    
    for i in range(altura):
        for j in range(largura):
            
            pixel = image[i][j]
            
            B = int(pixel[0])
            G = int(pixel[1])
            R = int(pixel[2])
            
            # Aplicando a transformação dente de serra para cada canal
            B = int((B % period) * (255 / period))
            G = int((G % period) * (255 / period))
            R = int((R % period) * (255 / period))
            
            B,G,R = get_values_for_overflow(B,G,R)
            
            result[i][j] = [B, G, R]
    
    return result

def log_transform(image):
    result = image.copy()
    altura, largura = image.shape[:2]
    
    max_val = int(find_max(image))
    
    c = 255 / math.log(1 + max_val)
    
    for i in range(altura):
        for j in range(largura):
            
            pixel = image[i][j]
            
            B = int(pixel[0])
            G = int(pixel[1])
            R = int(pixel[2])
            
            # Aplicando a transformação logarítmica para cada canal
            B = int(c * math.log(1 + B))
            G = int(c * math.log(1 + G))
            R = int(c * math.log(1 + R))
            
            result[i][j] = [B, G, R]
    
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
contrasted_image = expand_contrast(compressed_image, 0, 255)
sawtooth_image = sawtooth_transform(image, 50)
log_image = log_transform(image)

images = [image, compressed_image, contrasted_image, sawtooth_image, log_image]
titles = ['Imagem original', 'Compressão de contraste linear', 'Expansão de contraste linear', 'Dente de serra', 'Transformada logaritmo']
show_multiple_images(images, titles)
