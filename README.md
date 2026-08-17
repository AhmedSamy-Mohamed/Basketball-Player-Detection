# 🏀 Basketball Player Detection

A computer vision project for detecting basketball players in images and videos using **YOLO11m**.

The project includes a trained YOLO11m object detection model and an interactive **Streamlit web application** that supports both image and video detection.

---

## 🚀 Project Overview

Basketball Player Detection is designed to automatically detect basketball players in basketball scenes using deep learning and computer vision.

The system can process:

* 🖼️ Single or multiple images
* 🎥 Single or multiple videos
* 🔍 Real-time-style frame-by-frame video detection
* 📊 Configurable confidence and IoU thresholds
* ⚡ Configurable video frame processing
* 🖥️ Interactive Streamlit demo

---

## 🎯 Objective

The main objective of this project is to build an end-to-end object detection system capable of identifying basketball players in different basketball scenes.

The complete workflow includes:

```text
Dataset
   ↓
Data Preparation
   ↓
YOLO Training
   ↓
Model Evaluation
   ↓
Best Model Selection
   ↓
Streamlit Deployment
   ↓
Image & Video Detection
```

---

## 🤖 Model

The project uses:

**YOLO11m**

The final trained model is stored as:

```text
best.pt
```

Model size:

```text
~40.5 MB
```

The model is loaded directly by the Streamlit application and used for inference on uploaded images and videos.

---

## 🖼️ Image Detection

The Streamlit application supports uploading:

* JPG
* JPEG
* PNG
* WEBP

Multiple images can be uploaded at the same time.

For each image, the application:

1. Loads the image.
2. Runs YOLO inference.
3. Draws bounding boxes.
4. Displays the detection result.
5. Reports the number of detected objects.
6. Measures inference time.
7. Provides an option to download the result.

---

## 🎥 Video Detection

The application supports:

* MP4
* AVI
* MOV
* MKV
* WEBM

Multiple videos can also be processed.

The video pipeline performs:

```text
Input Video
     ↓
Frame Extraction
     ↓
YOLO11m Detection
     ↓
Bounding Box Rendering
     ↓
Video Reconstruction
     ↓
H.264 Conversion
     ↓
Browser-Compatible MP4
     ↓
▶️ Streamlit Video Player
```

The processed video can be played directly inside the Streamlit application without requiring the user to download it first.

---

## ⚙️ Detection Settings

The application provides configurable detection parameters.

### Confidence Threshold

Controls the minimum confidence required for a detection to be displayed.

### IoU Threshold

Controls the Intersection over Union threshold used during Non-Maximum Suppression.

### Frame Skip

For videos, users can select:

```text
1 → Process every frame
2 → Process every second frame
3 → Process every third frame
```

This provides a trade-off between processing speed and temporal detection detail.

---

## 🖥️ Streamlit Demo

The project includes an interactive Streamlit interface with two main sections:

### Image Detection

Upload one or multiple basketball images and run detection directly from the browser.

### Video Detection

Upload one or multiple basketball videos, process them with YOLO11m, and preview the detected video directly inside Streamlit.

---

## 📸 Demo

### Image Detection

Add screenshots of the application here:

```text
screenshots/
```

Example:

```markdown
![Image Detection](screenshots/image_detection.png)
```

### Video Detection

A screen recording of the Streamlit demo can also be added to demonstrate the complete detection workflow.

---

## 📁 Project Structure

```text
Basketball-Player-Detection/
│
├── app.py
├── best.pt
├── requirements.txt
├── .gitignore
│
├── screenshots/
│
└── outputs/
    ├── images/
    └── videos/
```

### Main Files

| File               | Description                 |
| ------------------ | --------------------------- |
| `app.py`           | Streamlit application       |
| `best.pt`          | Trained YOLO11m model       |
| `requirements.txt` | Python dependencies         |
| `.gitignore`       | Git ignored files           |
| `screenshots/`     | Project screenshots         |
| `outputs/`         | Generated detection results |

---

## 🛠️ Technologies

The project was developed using:

* Python
* PyTorch
* Ultralytics YOLO
* YOLO11m
* OpenCV
* Streamlit
* Pillow
* NumPy
* FFmpeg

---

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/AhmedSamy-Mohamed/Basketball-Player-Detection.git
```

Move into the project directory:

```bash
cd Basketball-Player-Detection
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

## 🔍 Using the Demo

### Image Detection

1. Open the **Image Detection** tab.
2. Upload one or more basketball images.
3. Adjust the confidence threshold if needed.
4. Click **Run Image Detection**.
5. View the detected players.
6. Download the results if required.

### Video Detection

1. Open the **Video Detection** tab.
2. Upload one or more basketball videos.
3. Select the desired frame processing mode.
4. Click **Run Video Detection**.
5. Wait for YOLO processing to finish.
6. The processed video appears directly inside Streamlit.
7. Press ▶️ to play the detection result.
8. Download the processed video if required.

---

## 📊 Model Evaluation

The final model was trained and evaluated as part of the project development pipeline.

Detailed evaluation metrics, including:

* Precision
* Recall
* mAP@50
* mAP@50:95
* Validation results

can be added here based on the final evaluation results.

---

## 🔮 Future Improvements

Potential future improvements include:

* Tracking individual players across frames
* Real-time webcam detection
* Basketball detection
* Team classification
* Player counting
* Jersey number recognition
* Court detection
* Player trajectory analysis
* GPU-accelerated inference
* Cloud deployment
* Real-time analytics dashboard

---

## 👨‍💻 Author

**Ahmed Samy Mohamed**

Mechatronics Engineering Student
Faculty of Engineering — Tanta University

Interested in:

* Computer Vision
* Machine Learning
* Robotics
* AI
* Mechatronics

---

## ⭐ Project

If you find this project useful, feel free to ⭐ the repository.

**GitHub Repository:**

https://github.com/AhmedSamy-Mohamed/Basketball-Player-Detection
