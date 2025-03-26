import os
import shutil
from tqdm import tqdm

# Diretórios base
base_dir = "data"
original_data_dir = "original_dataset"

# Cria os diretórios base se não existirem
os.makedirs(base_dir, exist_ok=True)
os.makedirs(os.path.join(base_dir, "images"), exist_ok=True)

# Define os diretórios de imagens e labels
images_dir = {
    "base": os.path.join(original_data_dir, "images"),
    "train": os.path.join(base_dir, "images", "train"),
    "val": os.path.join(base_dir, "images", "val"),
}
os.makedirs(images_dir["train"], exist_ok=True)
os.makedirs(images_dir["val"], exist_ok=True)

labels_dir = {
    "base": os.path.join(original_data_dir, "labels"),
    "train": os.path.join(base_dir, "labels", "train"),
    "val": os.path.join(base_dir, "labels", "val"),
}
os.makedirs(labels_dir["train"], exist_ok=True)
os.makedirs(labels_dir["val"], exist_ok=True)

# Caminhos dos arquivos de lista
train_list_path = os.path.join(original_data_dir, "train_files.txt")
val_list_path = os.path.join(original_data_dir, "val_files.txt")


def copy_files(file_names, split):
    """
    Copia os arquivos de imagem e seus labels do dataset original para os diretórios de treino ou validação,
    exibindo uma barra de progresso.
    """
    for img_name in tqdm(file_names, desc=f"Copiando arquivos para {split}"):
        # Define o nome do arquivo de label substituindo a extensão da imagem
        label_name = img_name.replace(".jpg", ".txt").replace(
            ".png", ".txt").replace(".jpeg", ".txt")
        img_path = os.path.join(images_dir["base"], img_name)
        label_path = os.path.join(labels_dir["base"], label_name)

        if not os.path.exists(img_path):
            print(f"Arquivo ausente: {img_path}")
        else:
            shutil.copy(img_path, images_dir[split])
            if os.path.exists(label_path):
                shutil.copy(label_path, labels_dir[split])
            else:
                print(f"Label ausente: {label_path}")


# Lê os arquivos de lista
with open(train_list_path, "r") as f:
    train_files_name = [line.strip() for line in f if line.strip()]

with open(val_list_path, "r") as f:
    val_files_name = [line.strip() for line in f if line.strip()]

# Copia os arquivos para os diretórios correspondentes com progress bar
copy_files(train_files_name, "train")
copy_files(val_files_name, "val")

# 0: Person
# 1: Ear
# 3: Face
# 5: Mask
# 7: Hammer
# 8: Glasses
# 9: Gloves
# 10: Helmet
# 11: Hands
# 12: Head
# 14: Shoes
# Mapeamento: índice original -> novo índice (apenas para as classes desejadas)
mapping = {
    0: 0,
    3: 1,
    8: 2,
    10: 3,
    12: 4
}


def filter_label_file(filepath):
    """
    Lê o arquivo de label, filtra as linhas que não pertencem às classes desejadas,
    re-mapeia o índice das classes mantidas e sobrescreve o próprio arquivo.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue  # Ignora linhas com formato inesperado
        cls = int(parts[0])
        if cls not in mapping:
            continue  # Remove classes indesejadas
        parts[0] = str(mapping[cls])  # Re-mapeia o índice
        new_lines.append(" ".join(parts) + "\n")
    # Sobrescreve o mesmo arquivo com as linhas filtradas
    with open(filepath, 'w') as f:
        f.writelines(new_lines)


def process_labels(label_dir):
    """
    Processa todos os arquivos de label dentro de 'train' e 'val' e aplica a filtragem, com progress bar.
    """
    for split in ['train', 'val']:
        split_dir = os.path.join(label_dir, split)
        files = [file for file in os.listdir(
            split_dir) if file.endswith('.txt')]
        for file in tqdm(files, desc=f"Filtrando labels em {split}"):
            filepath = os.path.join(split_dir, file)
            filter_label_file(filepath)


print()

# Aplica o filtro de labels nos diretórios de treino e validação com progress bar
process_labels(os.path.join(base_dir, "labels"))
