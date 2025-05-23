# 💧 Automatic Watering System with ESP32, FastAPI, and Vue

This project is an **automatic irrigation system** controlled via Wi-Fi, ideal for watering plants based on soil moisture. It uses an **ESP32**, sensors, and a web-based frontend and backend to visualize and manage the data.

## 🔧 Components Used

- ✅ ESP32 (Wi-Fi enabled)
- ✅ Capacitive soil moisture sensor
- ✅ 10kΩ resistor
- ✅ Transistor (to switch the pump)
- ✅ 5V relay module
- ✅ 5V water pump
- ✅ **MT3608** step-up module – used to boost battery voltage to 5V
- ✅ Power supply (batteries or power bank)
- ✅ Backend built with **FastAPI**
- ✅ Frontend built with **Vue + Vite**

## 🧠 Project Overview

- The **ESP32** reads soil moisture data and sends it to the API over Wi-Fi.
- The **FastAPI backend** stores the data in a PostgreSQL database.
- The **Vue frontend** displays the latest humidity reading in real-time and refreshes automatically.

---

## ⚙️ How to Run the Project

Requirements:

- Docker and Docker Compose installed
- Git

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
docker-compose up --build
```

- Access the **frontend locally**:  
  👉 http://localhost:5173

---

## 🌐 Access from Another Device on the Network

To access the frontend from another phone or computer **on the same Wi-Fi network**:

1. Find out the local IP address of the machine running the project (e.g., `192.168.0.10`).
2. On the other device, open a browser and go to:  
   👉 `http://192.168.0.10:5173`

> The frontend automatically detects this IP and correctly connects to the FastAPI backend.

⚠️ **Note:** Only devices on your local network will have access — the server is not exposed to the public internet by default.
