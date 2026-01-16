# 🚗 VigilDrive AI

**AI‑Powered Driver Fatigue Detection & Governance Platform**

VigilDrive AI is a real‑time driver safety system that uses computer vision to detect early signs of driver fatigue (eye closure, reduced blinking, PERCLOS) and trigger escalating alerts — all while emphasizing **privacy‑by‑design** and **responsible AI**, aligned with the **IBM Track**.

This project was built for a hackathon by a team of 3 and is designed to be demo‑friendly, modular, and enterprise‑ready.

---

## 🎯 Problem Statement

Drowsy driving causes thousands of accidents every year. Existing solutions are often reactive or intrusive. VigilDrive AI provides a **proactive**, **privacy‑aware**, and **explainable AI** system that detects fatigue *before* it becomes dangerous.

---

## ✅ Key Features

### 🧠 Real‑Time AI Detection

* Webcam‑based driver monitoring
* Eye Aspect Ratio (EAR)
* **PERCLOS** (Percentage of Eye Closure)
* Fatigue classification (LOW / MEDIUM / HIGH)

### 🚨 Smart Alert System

* Escalating alerts based on fatigue level
* Audio alerts (cross‑platform)
* Alert logging with timestamps

### 📊 Analytics Dashboard

* Fatigue timeline visualization
* Alert frequency analysis
* Historical trend tracking

### 🔐 Privacy & Governance (IBM Track)

* On‑device processing (no cloud video storage)
* Optional face blurring
* Audit logging
* Model transparency & limitations

---

## 🧩 Project Structure

```
Vigildrive-ai/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
│
├── src/
│   ├── detector.py        # Computer vision & fatigue detection
│   ├── alert_system.py    # Alert logic (audio + escalation)
│   ├── database.py        # SQLite logging
│   ├── dashboard.py       # Analytics visualizations
│
├── governance/
│   └── privacy.py         # Privacy & audit utilities
│
├── data/
│   └── vigildrive.db      # SQLite database
│
├── assets/
│   ├── logo.png           # App & sidebar logo
│   └── demo_images/
│
└── venv/                  # Python virtual environment
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/Vigildrive-ai.git
cd Vigildrive-ai
```

### 2️⃣ Create & activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Upgrade pip

```bash
pip install --upgrade pip
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

Then open your browser at:

```
http://localhost:8501
```

---

## 🧪 Testing Alerts (Optional)

To test the alert system without the camera:

```bash
python test_person_b.py
```

---

## 🖥️ Tech Stack

* **Python 3.11**
* **Streamlit** — Web UI
* **OpenCV** — Computer vision
* **NumPy / Pandas** — Data processing
* **SQLite** — Local logging
* **Matplotlib** — Analytics charts
* **Playsound** — Cross‑platform alerts

---

## 🧠 Responsible AI & IBM Track Alignment

* Privacy‑by‑design (local processing)
* No facial data stored
* Explainable fatigue metrics (EAR, PERCLOS)
* Transparent limitations documented
* Governance & audit logs

---

## 👥 Team Roles

* **Person A — Vision Engineer**
  Computer vision, fatigue metrics, detection logic

* **Person B — Safety Architect**
  Alert system, logging, analytics

* **Person C — Governance Guardian**
  UI/UX, privacy, IBM alignment

---

## 🚀 Demo Tips

* Start with eyes open → normal state
* Close eyes for 2–3 seconds → trigger HIGH alert
* Show analytics dashboard after demo
* Highlight privacy features for IBM judges

---

## 📌 Future Improvements

* Mobile deployment
* Fleet management dashboard
* ML‑based fatigue classifier
* Voice alerts & haptic feedback

---

## 📜 License

This project is for educational and hackathon use.

---

**VigilDrive AI — Building safer roads with responsible AI.** 🚦
