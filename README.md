# 🛡️ PhishGuard

### AI-Powered Phishing Detection & Threat Intelligence Platform

PhishGuard is an intelligent phishing detection platform that combines browser automation, computer vision, machine learning, local Large Language Models, and threat intelligence to perform deep website security analysis.

Unlike traditional URL scanners that rely only on blacklist matching, PhishGuard performs a multi-stage investigation by simulating real browser interaction, extracting visual and technical indicators, analyzing website content using AI, and combining those results with machine learning models to produce an explainable phishing risk assessment.

---

# Features

## Browser Automation

- Playwright-powered website analysis
- Full webpage rendering
- Dynamic content loading
- JavaScript execution
- Screenshot capture

---

## Computer Vision

- OCR using Moondream
- Website logo detection
- Brand identification
- Security badge recognition
- Visual phishing indicator analysis

---

## Artificial Intelligence

Local AI processing powered by Ollama.

Models used:

- Phi-3
- Moondream

Capabilities:

- Website understanding
- Suspicious content analysis
- Security reasoning
- Threat explanation
- JSON generation
- Investigation summaries

---

## Machine Learning

PhishGuard combines multiple ML technologies including:

- AutoGluon
- Scikit-Learn
- CatBoost
- LightGBM
- XGBoost

Used for:

- Phishing classification
- Feature analysis
- Threat prediction
- Risk scoring

---

## Threat Intelligence

- DuckDuckGo Search
- WHOIS lookup
- Security vendor verification
- Domain investigation
- Website metadata analysis

---

## Interactive Dashboard

Modules include:

- Scanner Pipeline
- Threat Score
- Investigation
- Reports
- Dashboard
- Suspicious Indicators
- Command Center

---

## Live Scan Pipeline

Real-time pipeline visualization using Flask-SocketIO.

Stages include:

✔ URL Submission

↓

✔ Browser Automation

↓

✔ Website Screenshot

↓

✔ OCR Processing

↓

✔ AI Analysis

↓

✔ Feature Extraction

↓

✔ Threat Intelligence

↓

✔ Machine Learning

↓

✔ Threat Score Generation

↓

✔ Investigation Report

---

# Technology Stack

## Backend

- Python
- Flask
- Flask-SocketIO

---

## Artificial Intelligence

- Ollama
- Phi-3
- Moondream
- HuggingFace Transformers
- PyTorch

---

## Machine Learning

- AutoGluon
- Scikit-Learn
- CatBoost
- XGBoost
- LightGBM

---

## Browser Automation

- Playwright

---

## Computer Vision

- EasyOCR
- OpenCV
- Pillow

---

## Data Processing

- Pandas
- NumPy
- PyArrow

---

## Threat Intelligence

- DDGS
- WHOIS
- BeautifulSoup
- Requests

---

## Visualization

- Plotly
- Matplotlib
- Seaborn

---

# Project Architecture

```
                   User URL
                       │
                       ▼
            Browser Automation
                (Playwright)
                       │
                       ▼
              Website Screenshot
                       │
                       ▼
                OCR (Moondream)
                       │
                       ▼
             AI Website Analysis
                  (Phi-3)
                       │
                       ▼
             Feature Extraction
                       │
                       ▼
             Threat Intelligence
                       │
                       ▼
          Machine Learning Engine
        (AutoGluon / XGBoost etc.)
                       │
                       ▼
             Threat Score Engine
                       │
                       ▼
        Investigation & Dashboard
```

---

# Folder Structure

```
PhishGuard/
│
├── ai/
├── scanner/
├── static/
├── templates/
├── utils/
├── dataset/
├── app.py
├── shared.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/USERNAME/PhishGuard.git

cd PhishGuard
```

---

## Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Playwright Browsers

```bash
playwright install
```

---

# Install Ollama

Download Ollama:

https://ollama.com/download

Verify:

```bash
ollama --version
```

---

# Download Required AI Models

```bash
ollama pull phi3
```

```bash
ollama pull moondream
```

Verify:

```bash
ollama list
```

Expected:

```
phi3

moondream
```

---

# Start Ollama

```bash
ollama serve
```

---

# Run PhishGuard

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

# Required Software

| Software | Required |
|------------|----------|
| Python 3.11+ | ✅ |
| Ollama | ✅ |
| Playwright | ✅ |
| Git | ✅ |

---

# AI Models

| Model | Purpose |
|---------|----------|
| Phi-3 | Website reasoning |
| Moondream | OCR & vision analysis |

---

# Major Components

- Browser Automation
- OCR
- Computer Vision
- Threat Intelligence
- Local AI
- Machine Learning
- Dashboard
- Live Terminal Streaming
- SocketIO Real-Time Updates
- JSON Report Generation

---

# Future Improvements

- VirusTotal API
- AbuseIPDB Integration
- Multi-user Authentication
- Docker Deployment
- REST API
- PDF Report Export
- Email Scanner
- Mobile Responsive UI
- Cloud Deployment
- Multi-language Support

---

# Disclaimer

PhishGuard is intended for educational, research, and defensive cybersecurity purposes only.

The project should not be used for unauthorized testing or activities that violate applicable laws or terms of service.

---

# License

AGPL V3

---

# Author 

Developed by **<Swastik Saha>**

Cybersecurity • Artificial Intelligence • Threat Intelligence • Machine Learning
