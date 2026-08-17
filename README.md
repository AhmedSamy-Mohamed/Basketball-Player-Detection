# 🏀 Basketball Player Detection

A real-time basketball object detection application built with **YOLO11m** and **Streamlit**.

The system detects and classifies multiple basketball-related objects and actions from images and videos, then displays the detection results through an interactive web interface.

## 🚀 Live Demo

**Streamlit App:**
https://basketball-player-detection-pt5zwq8fqexxj2dhjgnevb.streamlit.app/

## 🎯 Project Overview

This project uses a trained YOLO11m object detection model to identify basketball-related objects and events.

The application supports:

* Image object detection
* Video object detection
* Multiple image uploads
* Multiple video uploads
* Adjustable confidence threshold
* Adjustable IoU threshold
* Adjustable video frame processing
* Adjustable output video resolution
* Detection result visualization
* Downloadable detected images
* Browser-compatible detected videos
* Online deployment using Streamlit Community Cloud

## 🧠 Model

The project uses **YOLO11m** from Ultralytics.

The trained model contains the following classes:

| Class                | Description                    |
| -------------------- | ------------------------------ |
| ball                 | Basketball                     |
| ball-in-basket       | Ball inside the basket         |
| number               | Player jersey number           |
| player               | Basketball player              |
| player-in-possession | Player possessing the ball     |
| player-jump-shot     | Player performing a jump shot  |
| player-shot-block    | Player performing a shot block |
| referee              | Referee                        |
| rim                  | Basketball rim                 |

## 📊 Model Performance

The model was evaluated on the test dataset.

| Metric    |  Score |
| --------- | -----: |
| Precision | 0.7650 |
| Recall    | 0.6915 |
| mAP@50    | 0.7532 |
| mAP@50-95 | 0.5315 |

### Per-Class Performance

| Class                | Precision | Recall | mAP@50 | mAP@50-95 |
| -------------------- | --------: | -----: | -----: | --------: |
| Ball                 |     0.837 |  0.585 |  0.684 |     0.386 |
| Ball-in-basket       |     0.517 |  0.500 |  0.560 |     0.426 |
| Number               |     0.796 |  0.894 |  0.902 |     0.484 |
| Player               |     0.915 |  0.970 |  0.966 |     0.761 |
| Player-in-possession |     0.522 |  0.425 |  0.449 |     0.363 |
| Player-jump-shot     |     0.732 |  0.500 |  0.699 |     0.500 |
| Player-shot-block    |     0.633 |  0.371 |  0.533 |     0.379 |
| Referee              |     0.961 |  0.979 |  0.991 |     0.806 |
| Rim                  |     0.972 |  1.000 |  0.995 |     0.679 |

## 🖼️ Image Detection

The application allows users to upload one or more basketball images.

The YOLO model detects the objects and displays the annotated image together with:

* Number of detected objects
* Inference time
* Download option

### Example

![Detected Image](screenshots/Detected_Image.jpg)

## 🎥 Video Detection

Users can upload basketball videos and run object detection frame by frame.

The application provides:

* Video information
* Detection progress
* Processing FPS
* Configurable frame skipping
* Configurable output resolution
* H.264 video conversion
* Direct browser playback
* Downloadable detection video

### Demo Video

The processed demonstration video is available in:

`demo/Detected_Video.mp4`

## 🖥️ Application Interface

![Application Interface](screenshots/Interface.PNG)

## ⚙️ Detection Settings

The application provides several configurable settings.

### Confidence Threshold

Controls the minimum confidence required for a detection to be displayed.

### IoU Threshold

Controls the Intersection over Union threshold used during Non-Maximum Suppression.

### Frame Skip

Users can choose to process:

* Every frame
* Every second frame
* Every third frame

This can reduce processing time for longer videos.

### Output Width

The output video can be generated at:

* Original resolution
* 640 px
* 768 px
* 960 px
* 1280 px

## 🛠️ Technologies Used

* Python
* YOLO11m
* Ultralytics
* OpenCV
* Streamlit
* Pillow
* NumPy
* FFmpeg
* Git
* GitHub
* Streamlit Community Cloud

## 📁 Project Structure

```text
Basketball-Player-Detection/
│
├── app.py
├── best.pt
├── requirements.txt
├── packages.txt
├── README.md
├── .gitignore
│
├── screenshots/
│   ├── Detected_Image.jpg
│   └── Interface.PNG
│
├── demo/
│   └── Detected_Video.mp4
│
└── outputs/
    ├── images/
    └── videos/
```

## 💻 Run Locally

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
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Make sure FFmpeg is installed and available on your system.

Run the application:

```bash
streamlit run app.py
```

The application will then be available locally through the Streamlit server.

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

The deployment uses:

* `requirements.txt` for Python dependencies
* `packages.txt` for system dependencies such as FFmpeg
* `app.py` as the Streamlit entry point
* `best.pt` as the trained YOLO model

## 📦 Requirements

Main Python dependencies:

* Streamlit
* Ultralytics
* OpenCV
* Pillow
* NumPy

## 🔗 Links

**Live Application:**
https://basketball-player-detection-pt5zwq8fqexxj2dhjgnevb.streamlit.app/

**GitHub Repository:**
https://github.com/AhmedSamy-Mohamed/Basketball-Player-Detection

## 👨‍💻 Author

**Ahmed Samy Mohamed**

Mechatronics Engineering Student
Tanta University

## ⭐ Project Highlights

This project demonstrates an end-to-end Computer Vision workflow:

**Dataset → YOLO Training → Model Evaluation → Streamlit Application → GitHub → Cloud Deployment**

The final system provides an interactive interface for applying the trained object detection model to real basketball images and videos.
