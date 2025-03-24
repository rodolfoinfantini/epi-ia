import os
import shutil

base_dir = "data"
original_data_dir = "original_dataset"

os.mkdir(base_dir)
os.mkdir(os.path.join(base_dir, "images"))

images_dir = {
    "base": os.path.join(original_data_dir, "images"),
    "train": os.path.join(base_dir, "images", "train"),
    "val": os.path.join(base_dir, "images", "val"),
}
os.makedirs(images_dir["train"])
os.makedirs(images_dir["val"])
labels_dir = {
    "base": os.path.join(original_data_dir, "labels"),
    "train": os.path.join(base_dir, "labels", "train"),
    "val": os.path.join(base_dir, "labels", "val"),
}
os.makedirs(labels_dir["train"])
os.makedirs(labels_dir["val"])

train_list_path = os.path.join(original_data_dir, "train_files.txt")
val_list_path = os.path.join(original_data_dir, "val_files.txt")

with open(train_list_path, "r") as f:
    train_files_name = [line.strip() for line in f if line.strip()]

for img_name in train_files_name:
    label_name = img_name.replace(".jpg", ".txt").replace(
        ".png", ".txt").replace(".jpeg", ".txt")
    img_path = os.path.join(images_dir["base"], img_name)
    label_path = os.path.join(labels_dir["base"], label_name)

    if not os.path.exists(img_path):
        print(f"Arquivo ausente: {img_path}")
    else:
        # copy image to image train folder
        # copy label to label train folder
        print(f"cp {img_path} {images_dir['train']}")
        shutil.copy(img_path, images_dir['train'])
        print(f"cp {label_path} {labels_dir['train']}")
        shutil.copy(label_path, labels_dir['train'])

with open(val_list_path, "r") as f:
    val_files_name = [line.strip() for line in f if line.strip()]

for img_name in val_files_name:
    label_name = img_name.replace(".jpg", ".txt").replace(
        ".png", ".txt").replace(".jpeg", ".txt")
    img_path = os.path.join(images_dir["base"], img_name)
    label_path = os.path.join(labels_dir["base"], label_name)

    if not os.path.exists(img_path):
        print(f"Arquivo ausente: {img_path}")
    else:
        # copy image to image val folder
        # copy label to label val folder
        print(f"cp {img_path} {images_dir['val']}")
        shutil.copy(img_path, images_dir['val'])
        print(f"cp {label_path} {labels_dir['val']}")
        shutil.copy(label_path, labels_dir['val'])


# 0 → 0 (Person)
# 1 → 1 (Head)
# 2 → 2 (Face)
# 3 → 3 (Glasses)
# 14 → 4 (Helmet)
mapping = {0: 0, 1: 1, 2: 2, 3: 3, 14: 4}
