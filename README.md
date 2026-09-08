# 🏎️ F1 Companion

**F1 Companion** is a desktop application built in Python designed for Formula 1 enthusiasts, strategy fans, and telemetry analysts. It bridges the gap between complex raw timing/telemetry data and a clean, responsive graphical user interface.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)
![PRs](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)
---

## ✨ Features

* **Telemetry Comparison Engine:** Compare speed, braking points, and throttle profiles between any two drivers in real-time.
* **Non-blocking UI:** Multithreaded background data ingestion via `fastf1` to ensure smooth GUI responsiveness during large data downloads.
* **Modern Dark UI:** CustomTkinter interface designed with Formula 1 aesthetics.
* **Automatic Lap Normalization:** Normalizes spatial distance telemetry to display accurate head-to-head comparisons starting at the start/finish line.

---

## 🛠️ Built With

* **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter):** Modern UI framework for Python.
* **[FastF1](https://github.com/theOehrly/Fast-F1):** Access to F1 live timing, telemetry, and session data.
* **[Matplotlib](https://matplotlib.org/):** Embedded data visualization plots.
* **[Pandas](https://pandas.pydata.org/):** High-performance data manipulation and filtering.

---

## 🚀 Quick Start

### Prerequisites
Make sure you have **Python 3.9+** installed.

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/joaomariapires2011-gif/F1-Companion-.git](https://github.com/joaomariapires2011-gif/F1-Companion-.git)
   cd F1-Companion-
---

## 📌 Roadmap

- [x] Basic telemetry visualization (Speed vs. Distance)
- [x] Multithreaded data loader
- [x] Track Map visualization (rendering circuit X/Y telemetry coordinates)
- [x] Implement full Lap Times comparison table
- [ ] Weather telemetry and track conditions integration
