import cv2

def calcular_histograma_local(image_path, output_file, num_particoes=3):
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        return
    
    height, width, _ = image.shape

    blocos = []
    bloco_altura = height // num_particoes
    
    for i in range(num_particoes):
        start_row = i * bloco_altura
        end_row = (i + 1) * bloco_altura if i != num_particoes - 1 else height
        bloco = image[start_row:end_row, :]
        blocos.append(bloco)
    
    histograma_concatenado = []

    for bloco in blocos:
        hist_r = [0] * 256
        hist_g = [0] * 256
        hist_b = [0] * 256

        bloco_height, bloco_width, _ = bloco.shape

        for i in range(bloco_height):
            for j in range(bloco_width):
                blue, green, red = bloco[i, j]
                
                hist_b[blue] += 1
                hist_g[green] += 1
                hist_r[red] += 1

        histograma_concatenado.extend(hist_b + hist_g + hist_r)
    
    with open(output_file, 'w') as f:
        for value in histograma_concatenado:
            f.write(f"{value} ")
    
    print(f"Histograma local armazenado no arquivo: {output_file}")

image_path = '../images/lena.png'
output_file = 'histograma_local.txt'

calcular_histograma_local(image_path, output_file, num_particoes=3)
