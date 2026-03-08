# Melanoma Detection Using Convolutional Neural Network (CNN)

## Overview

Melanoma is one of the most dangerous types of skin cancer. Early detection significantly improves survival rates.
This project uses **Deep Learning with a Convolutional Neural Network (CNN)** to classify skin lesion images as **Benign** or **Malignant**.

The system includes a **Flask web application** that allows users to upload an image and receive a prediction from the trained model.

---

## Features

* Upload skin lesion images
* CNN-based melanoma classification
* Real-time prediction through Flask web application
* Visualization of model performance
* Simple and user-friendly interface

---

## Technologies Used

**Programming Language**

* Python

**Machine Learning / Deep Learning**

* TensorFlow
* Keras
* NumPy
* Scikit-learn

**Web Framework**

* Flask

**Image Processing**

* OpenCV
* Pillow

**Visualization**

* Matplotlib

---

## Project Structure

Melanoma-Detection-Using-Convolutional-Neural-Network-CNN

app.py
melanoma_predictor.py
skin.h5
requirements.txt

dataset/

templates/
index.html
login.html
performance.html
chart.html

static/
css/
js/
images/
fonts/

README.md

---

## Dataset

The CNN model is trained on a dataset containing **skin lesion images**.

Dataset classes:

* Benign
* Malignant

These images help the model learn visual patterns associated with melanoma.

---

## Model

The trained CNN model is stored as:

skin.h5

This model is loaded inside the Flask application for prediction.

---

## Installation

### 1 Clone the repository

git clone https://github.com/Guruprasadhv/Melanoma-Detection-Using-Convolutional-Neural-Network-CNN-.git

### 2 Go to project folder

cd Melanoma-Detection-Using-Convolutional-Neural-Network-CNN-

### 3 Install dependencies

pip install -r requirements.txt

---

## Running the Application

Start the Flask server:

python app.py

After running, the terminal will show something like:

Running on http://127.0.0.1:5001

Open your browser and go to:

http://127.0.0.1:5001

---

## How to Use

1. Open the web application in the browser.
2. Upload a skin lesion image.
3. Click **Predict**.
4. The CNN model analyzes the image.
5. The result will display:

Benign
or
Malignant

---

## Example Commands

pip install -r requirements.txt
python app.py

Open browser → http://127.0.0.1:5001

---

## Future Improvements

* Improve model accuracy using larger datasets
* Deploy application on cloud platforms
* Add patient history management
* Integrate dermatologist assistance system

---

## Author

Guruprasad H V
MCA Student
PES University

GitHub
https://github.com/Guruprasadhv

---

## License

This project is for educational and research purposes.
