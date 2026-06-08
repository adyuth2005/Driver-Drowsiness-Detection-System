# 🚗 Driver Drowsiness Detection System

Real-time driver drowsiness detection using **MediaPipe Face Mesh**, **OpenCV**, and **Pygame**. This application monitors the driver's eyes through a webcam stream, calculates the **Eye Aspect Ratio (EAR)**, and triggers a warning alarm when signs of drowsiness (prolonged eye closure) are detected.

---

## 🌟 Features

- **Real-Time Landmark Tracking**: Employs MediaPipe's lightweight and high-fidelity FaceMesh model to track facial features at high frame rates.
- **Precise Eye State Analysis**: Calculates the Eye Aspect Ratio (EAR) for both eyes to accurately determine if they are open or closed.
- **Audio Alerts & Visual Feedback**: Displays real-time state overlay texts (`EYES OPEN`, `EYES CLOSED`, `DRIVER IS SLEEPY`) and plays an audible alarm (`warning.wav`) when the driver remains sleepy.
- **Responsive Controls**: Easily exit the application by pressing the `ESC` key.

---

## 📐 How It Works

### 1. Eye Landmark Extraction
Using MediaPipe Face Mesh, the system tracks specific coordinate indices for both eyes:
- **Left Eye Indices**: `[33, 160, 158, 133, 153, 144]`
- **Right Eye Indices**: `[362, 385, 387, 263, 373, 380]`

### 2. Eye Aspect Ratio (EAR) Calculation
The Eye Aspect Ratio is calculated using the distance between vertical eye landmarks divided by the distance between horizontal landmarks.

For 6 landmarks representing an eye:
- $p_1$ (inner corner), $p_4$ (outer corner)
- $p_2, p_6$ and $p_3, p_5$ (vertical points)

```
        p2     p3
      •------•
p1  •          •  p4
      •------•
        p6     p5
```

The EAR formula used is:

$$\text{EAR} = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2 \times ||p_1 - p_4||}$$

Where $||p_i - p_j||$ is the Euclidean distance between points.

### 3. Drowsiness Decision Logic
- **EAR Threshold**: If the average EAR of both eyes drops below **`0.20`**, the eyes are considered **closed**.
- **Consecutive Frames (Drowsiness)**: A counter tracks the consecutive number of frames the eyes remain closed. If this counter exceeds **`30 frames`** (approximately 1.0 to 1.5 seconds, depending on camera framerate), the alarm sound (`warning.wav`) is triggered, and a **`DRIVER IS SLEEPY`** alert is displayed.
- **Reset**: If the average EAR goes above `0.20`, the counter resets back to `0` immediately.

---

## 📁 Project Structure

```text
driver_drowsiness/
├── detect.py            # Main application entry point containing detection logic
├── requirements.txt     # Python dependency configuration file
├── warning.wav          # Alarm sound triggered during drowsiness detection
├── alarm.wav            # Alternative alarm audio asset
├── model/               # Model assets folder
│   └── shape_predictor_68_face_landmarks.dat  # Unused dlib landmark model (kept for legacy support)
└── README.md            # Project documentation (this file)
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- A working webcam

### 1. Clone/Navigate to the Project Directory
Open your terminal and navigate to the project directory:
```bash
cd driver_drowsiness
```

### 2. Set Up a Virtual Environment (Recommended)
Creating a virtual environment ensures dependencies do not conflict with system-level packages:

**On Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install the required packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the main application script:
```bash
python detect.py
```

### Controls & Interactions:
- **Visual Overlays**:
  - Top-left displays current calculated **EAR**.
  - Status indicator displays **`EYES OPEN`** (green text) or **`EYES CLOSED`** (red text).
  - Red warning overlay displays **`DRIVER IS SLEEPY`** when drowsiness is detected.
- **Audio Warnings**: The alert sound (`warning.wav`) plays continuously while the driver is sleepy.
- **Termination**: Press the **`ESC`** key with the webcam window focused to cleanly exit the application.

---

## ⚙️ Configuration & Customization

You can calibrate and optimize detection sensitivity directly in the [detect.py](file:///c:/Users/ADYUTH/OneDrive/Desktop/driver_drowsiness/detect.py) file:

- **Adjusting Eye Closed Threshold**:
  In line 94, modify the EAR threshold:
  ```python
  if avg_EAR < 0.20:  # Increase value (e.g., 0.22) if too sensitive; decrease if not responsive
  ```
- **Adjusting Drowsiness Trigger Frame Count**:
  In line 101, modify the consecutive frames count:
  ```python
  if counter > 30:  # Set to a lower number (e.g., 20) for faster triggers, or higher for fewer false alarms
  ```
