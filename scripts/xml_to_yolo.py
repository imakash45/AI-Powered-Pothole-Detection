"""
XML to YOLO Conversion Script
Project: AI-Powered Pothole Detection

This script:
- Reads Pascal VOC XML annotations
- Converts all pothole-related classes into a single class (class_id = 0)
- Saves YOLO format labels into data/labels/all/

"""

import os
import xml.etree.ElementTree as ET

# ==========================
# Define Robust Paths
# ==========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_IMAGES_PATH = os.path.join(BASE_DIR, "data", "raw", "images", "potholes")
ANNOTATIONS_PATH = os.path.join(BASE_DIR, "data", "raw", "annotations")
OUTPUT_LABELS_PATH = os.path.join(BASE_DIR, "data", "labels", "all")

os.makedirs(OUTPUT_LABELS_PATH, exist_ok=True)

# ==========================
# Conversion Function
# ==========================

def convert_xml_to_yolo(xml_file):
    xml_path = os.path.join(ANNOTATIONS_PATH, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Get image width and height
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    yolo_lines = []

    for obj in root.findall("object"):
        # Convert ALL classes to single class (0)
        class_id = 0

        bbox = obj.find("bndbox")
        xmin = float(bbox.find("xmin").text)
        ymin = float(bbox.find("ymin").text)
        xmax = float(bbox.find("xmax").text)
        ymax = float(bbox.find("ymax").text)

        # Convert to YOLO format
        x_center = ((xmin + xmax) / 2) / width
        y_center = ((ymin + ymax) / 2) / height
        bbox_width = (xmax - xmin) / width
        bbox_height = (ymax - ymin) / height

        yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"
        yolo_lines.append(yolo_line)

    return yolo_lines


# ==========================
# Process All XML Files
# ==========================

xml_files = [f for f in os.listdir(ANNOTATIONS_PATH) if f.endswith(".xml")]

print(f"Total XML files found: {len(xml_files)}")

for xml_file in xml_files:
    yolo_data = convert_xml_to_yolo(xml_file)

    # Save as .txt file with same base name
    txt_filename = os.path.splitext(xml_file)[0] + ".txt"
    txt_path = os.path.join(OUTPUT_LABELS_PATH, txt_filename)

    with open(txt_path, "w") as f:
        for line in yolo_data:
            f.write(line + "\n")

print("Conversion completed successfully.")
print(f"YOLO labels saved to: {OUTPUT_LABELS_PATH}")