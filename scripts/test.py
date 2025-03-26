import cv2
import os

# Person
# Head
# Face
# Glasses
# Face-mask-medical
# Face-guard
# Ear
# Earmuffs
# Hands
# Gloves
# Foot
# Shoes
# Safety-vest
# Tools
# Helmet
# Medical-suit
# Safety-suit

# Diretórios das imagens e labels
images_dir = 'data/images/train'
labels_dir = 'data/labels/train'

# Lista de classes (ajuste conforme seu dataset)
classes = ['Person', 'Head', 'Face', 'Glasses', 'Helmet']


def load_annotations(label_path, img_width, img_height):
    """
    Lê o arquivo de anotação no formato YOLO:
    <classe> <x_center> <y_center> <width> <height>
    (valores normalizados) e converte para coordenadas de caixa.
    """
    boxes = []
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 5:
                cls_idx = int(parts[0])
                x_center = float(parts[1]) * img_width
                y_center = float(parts[2]) * img_height
                w = float(parts[3]) * img_width
                h = float(parts[4]) * img_height
                # Converte para coordenadas x, y (top-left) e tamanho (w, h)
                x = int(x_center - w / 2)
                y = int(y_center - h / 2)
                boxes.append((x, y, int(w), int(h), cls_idx))
    return boxes


# Lista de arquivos de imagem
image_files = [f for f in os.listdir(images_dir)]
print(len(image_files))
if not image_files:
    print("Nenhuma imagem encontrada em", images_dir)
    exit(1)

# Índice da imagem atual
current_index = 0

while True:
    # Carrega a imagem atual
    image_file = image_files[current_index]
    print(image_file)
    image_path = os.path.join(images_dir, image_file)
    print(image_path)
    label_path = os.path.join(
        labels_dir, os.path.splitext(image_file)[0] + '.txt')
    print(label_path)

    img = cv2.imread(image_path)
    if img is None:
        print("Erro ao carregar a imagem:", image_path)
        exit(1)

    img_height, img_width = img.shape[:2]

    # Carrega as anotações, se o arquivo existir
    if os.path.exists(label_path):
        boxes = load_annotations(label_path, img_width, img_height)
    else:
        print("Arquivo de anotações não encontrado:", label_path)
        boxes = []

    # Desenha as bounding boxes na imagem
    for (x, y, w, h, cls_idx) in boxes:
        color = (0, 255, 0)  # cor verde para as caixas
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        label = classes[cls_idx] if cls_idx < len(classes) else str(cls_idx)
        cv2.putText(img, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Exibe a imagem com as anotações
    cv2.imshow(image_file, img)

    # Espera por uma tecla pressionada
    key = cv2.waitKey(0) & 0xFF

    if key == ord('q'):  # Pressione 'q' para sair
        break
    elif key == 81:  # Tecla de seta para a esquerda
        current_index = (current_index - 1) % len(image_files)
    elif key == 83:  # Tecla de seta para a direita
        current_index = (current_index + 1) % len(image_files)

    # Fecha a janela
    cv2.destroyAllWindows()

cv2.destroyAllWindows()
