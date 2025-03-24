import os

base_dir = "datasets"  # conforme definido no settings.json
images_dir = os.path.join(base_dir, "images")
train_list_path = os.path.join(base_dir, "train_files.txt")

with open(train_list_path, "r") as f:
    image_files = [line.strip() for line in f if line.strip()]

missing = []
for img_path in image_files:
    full_path = os.path.join(base_dir, img_path)
    if not os.path.exists(full_path):
        missing.append(full_path)

if missing:
    print("Arquivos ausentes:")
    for m in missing:
        print(m)
else:
    print("Todos os arquivos de imagem foram encontrados.")
