import os
import random
import shutil

# ---------------- BASE PATH ----------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "data"))

POTHOLE_IMAGES = os.path.join(BASE_PATH, "raw", "images", "potholes")
NORMAL_IMAGES = os.path.join(BASE_PATH, "raw", "images", "normal")
LABELS_PATH = os.path.join(BASE_PATH, "labels", "all")

YOLO_IMAGES = os.path.join(BASE_PATH, "yolo_dataset", "images")
YOLO_LABELS = os.path.join(BASE_PATH, "yolo_dataset", "labels")

# ---------------- SPLIT RATIO ----------------
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

# ---------------- CREATE SUBFOLDERS ----------------
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(YOLO_IMAGES, split), exist_ok=True)
    os.makedirs(os.path.join(YOLO_LABELS, split), exist_ok=True)

# ---------------- GET IMAGE LIST ----------------
pothole_images = os.listdir(POTHOLE_IMAGES)
normal_images = os.listdir(NORMAL_IMAGES)

# Combine all images
all_images = []

for img in pothole_images:
    all_images.append(("pothole", img))

for img in normal_images:
    all_images.append(("normal", img))

# Shuffle to avoid bias
random.seed(42)
random.shuffle(all_images)

total = len(all_images)
train_end = int(total * TRAIN_RATIO)
val_end = train_end + int(total * VAL_RATIO)

splits = {
    "train": all_images[:train_end],
    "val": all_images[train_end:val_end],
    "test": all_images[val_end:]
}

# ---------------- COPY FILES ----------------
for split_name, split_data in splits.items():
    for img_type, img_name in split_data:

        name_without_ext = os.path.splitext(img_name)[0]

        if img_type == "pothole":
            src_img = os.path.join(POTHOLE_IMAGES, img_name)
            src_label = os.path.join(LABELS_PATH, name_without_ext + ".txt")
        else:
            src_img = os.path.join(NORMAL_IMAGES, img_name)
            src_label = None

        dst_img = os.path.join(YOLO_IMAGES, split_name, img_name)
        dst_label = os.path.join(YOLO_LABELS, split_name, name_without_ext + ".txt")

        shutil.copy(src_img, dst_img)

        if src_label and os.path.exists(src_label):
            shutil.copy(src_label, dst_label)
        else:
            open(dst_label, "w").close()
            
print("Dataset split completed successfully.")