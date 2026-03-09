# AI Powered Pothole Detection System

## Overview
Road potholes are a major cause of traffic accidents, vehicle damage, and poor road conditions. Manual inspection of roads is slow and inefficient. This project presents an **AI-powered pothole detection system** that automatically detects potholes in images and video streams using a deep learning model.

The system uses the **YOLO object detection framework** to identify potholes in real-time. It can detect potholes from images, recorded videos, and live webcam feeds.

---

## Key Features
- Automatic pothole detection using deep learning
- Real-time detection using webcam
- Image and video input support
- Data preprocessing and annotation conversion
- Exploratory Data Analysis (EDA) on dataset
- High-speed object detection using YOLO

---

## Dataset
The dataset used in this project contains:

- **1382 images containing potholes**
- **465 images without potholes**

Annotations were originally in **XML format** and converted to **YOLO format** for training.

Due to GitHub size limitations, only a small sample dataset is included in this repository.

---

## Project Workflow

1. Dataset collection
2. Data cleaning
3. Exploratory Data Analysis (EDA)
4. Annotation conversion (XML → YOLO)
5. Dataset splitting (train / validation)
6. Model training using YOLO
7. Model evaluation
8. Real-time detection

---

## Project Structure

AI-Powered-Pothole-Detection  
│  
├── notebooks  
│ ├── EDA.ipynb  
│ ├── YOLO_Training.ipynb  
│  
├── scripts  
│ ├── xml_to_yolo.py  
│ ├── dataset_split.py  
│  
├── dataset_sample  
│ ├── images  
│ ├── labels  
│  
├── model  
│ ├── best.pt  
│  
├── app  
│ ├── app.py  
│  
├── requirements.txt  
└── README.md  


---

## Technologies Used

- Python
- YOLO (Ultralytics Framework)
- OpenCV
- NumPy
- Pandas
- Matplotlib
- Streamlit

---

## Installation

Clone the repository:  
git clone https://github.com/yourusername/AI-Powered-Pothole-Detection.git

Install required libraries:
pip install -r requirements.txt

## Running the Project

Run the Streamlit application:
- streamlit run streamlit_app.py

## Results

The trained YOLO model can detect potholes accurately in:  
- Road images  
- Video frames  
- Live webcam streams  

The system highlights potholes with bounding boxes for easy identification.

## Future Improvements

- GPS-based pothole location tracking  
- Integration with road maintenance systems  
- Mobile application for real-time road monitoring  
- Larger and more diverse dataset  

## Author

Akash  
Data Science / Machine Learning Enthusiast
