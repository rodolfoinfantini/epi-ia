import os

base_dir = "data"

images_dir = {
    "base": os.path.join(base_dir, "images"),
    "train": os.path.join(base_dir, "images", "train"),
    "val": os.path.join(base_dir, "images", "val"),
}
labels_dir = {
    "base": os.path.join(base_dir, "labels"),
    "train": os.path.join(base_dir, "labels", "train"),
    "val": os.path.join(base_dir, "labels", "val"),
}

train_list_path = os.path.join(base_dir, "train_files.txt")
val_list_path = os.path.join(base_dir, "val_files.txt")

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
        os.system(f"cp {img_path} {images_dir['train']}")
        print(f"cp {label_path} {labels_dir['train']}")
        os.system(f"cp {label_path} {labels_dir['train']}")

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
        os.system(f"cp {img_path} {images_dir['val']}")
        print(f"cp {label_path} {labels_dir['val']}")
        os.system(f"cp {label_path} {labels_dir['val']}")
