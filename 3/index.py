import cv2

def calcular_histograma_global(image_path, output_file):
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        return
    
    hist_r = [0] * 256
    hist_g = [0] * 256
    hist_b = [0] * 256

    height, width, _ = image.shape

    for i in range(height):
        for j in range(width):
            
            blue, green, red = image[i, j]
            
            hist_b[blue] += 1
            hist_g[green] += 1
            hist_r[red] += 1

    histograma_global = hist_b + hist_g + hist_r

    with open(output_file, 'w') as f:
        for value in histograma_global:
            f.write(f"{value} ")                            
    
    print(f"Histograma global armazenado no arquivo: {output_file}")

image_path = '../images/lena.png'
output_file = 'histograma_global.txt'

calcular_histograma_global(image_path, output_file)