# DevSecOps Week 9

## DevSecOps Monitoring & Security Simulation

[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://www.docker.com/)
[![Elastic](https://img.shields.io/badge/ELK-8.11.0-yellow)](https://www.elastic.co/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-Dashboard-red)](https://grafana.com/)
[![DevSecOps](https://img.shields.io/badge/DevSecOps-Monitoring--Security-success)](#)

---

## Deskripsi Proyek

Repository ini berisi implementasi **centralized logging dan system monitoring** menggunakan **ELK Stack** serta **Prometheus & Grafana**.  
Selain deployment monitoring, proyek ini juga mencakup **simulasi skenario keamanan** untuk menganalisis indikasi ancaman dan dampaknya terhadap sistem.

---

## Arsitektur Monitoring

```mermaid
flowchart LR
    User -->|HTTP Request| FlaskApp
    FlaskApp -->|Application Logs| LogFile
    LogFile --> Filebeat
    Filebeat --> Elasticsearch
    Elasticsearch --> Kibana

    NodeExporter --> Prometheus
    Prometheus --> Grafana
````

---

## Teknologi yang Digunakan

* Docker & Docker Compose
* Elasticsearch 8.11
* Kibana 8.11
* Flask (Python)
* Prometheus
* Node Exporter
* Grafana

---

## Struktur Direktori

```text
devsecops-monitoring/
├── docker-compose.yml
├── Dockerfile
├── prometheus.yml
├── app/
│   └── app.log
│   └── app.py
└── README.md
```

---

## Deploy Infrastruktur Monitoring

### 1. Jalankan Seluruh Service

```bash
docker compose up -d
```

### 2. Akses Service

* Elasticsearch: [http://localhost:9200](http://localhost:9200)
* Kibana: [http://localhost:5601](http://localhost:5601)
* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)

Login Grafana:

```
username: admin
password: admin
```

---

## Aplikasi Simulasi Log

File `app.py` digunakan untuk menghasilkan log aplikasi.

```python
import logging
import os
from flask import Flask

app = Flask(__name__)

LOG_DIR = "/app"
LOG_FILE = "/app/app.log"

# pastikan folder log ada
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

@app.route("/")
def home():
    app.logger.info("User accessed home page")
    return "Hello DevSecOps"

@app.route("/login")
def login():
    app.logger.warning("Failed login attempt")
    return "Login failed"

@app.route("/error")
def error():
    app.logger.error("Application error occurred")
    return 1 / 0

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

```

---

## Praktik 1 – Centralized Logging (ELK)

### Kirim Log Aplikasi ke ELK

Log aplikasi Flask disimpan ke file `app.log` dan dikirim ke Elasticsearch menggunakan Filebeat (standalone).

### Analisis di Kibana

Gunakan **Kibana Discover** untuk mencari log:

```
message : "Failed login attempt"
log.level : "error"
```

---

## Praktik 2 – Metrics Monitoring (Prometheus & Grafana)

### Tambahkan Data Source Prometheus di Grafana

URL:

```
http://prometheus:9090
```

### Import Dashboard

Dashboard ID:

```
1860
```

Dashboard ini digunakan untuk memantau:

* CPU Usage
* Memory Usage
* Load Average

---

## Simulasi Skenario Keamanan

### 1. Error Aplikasi

Trigger error:

```powershell
Invoke-WebRequest http://localhost:5000/error
```

Hasil:

* Log level ERROR tercatat
* Error terdeteksi di Kibana

---

### 2. Login Gagal Berulang (Brute Force)

Simulasi:

```powershell
for ($i=1; $i -le 30; $i++) {
  Invoke-WebRequest http://localhost:5000/login -UseBasicParsing
}
```

Indikasi:

* Banyak log login gagal dalam waktu singkat
* Pola brute force attack

---

### 3. Beban Sistem Tinggi (CPU)

Simulasi CPU tinggi:

```powershell
1..8 | ForEach-Object {
  Start-Job { while ($true) { } }
}
```

Hentikan simulasi:

```powershell
Get-Job | Remove-Job -Force
```

Hasil:

* Lonjakan CPU terlihat di Grafana
* Sistem mengalami resource pressure

---

## Analisis Keamanan

### Indikasi Ancaman

* Error aplikasi menunjukkan potensi bug atau eksploitasi
* Login gagal berulang mengindikasikan brute force attack
* Lonjakan CPU menunjukkan potensi denial of service

### Dampak ke Sistem

* Penurunan performa aplikasi
* Risiko account takeover
* Potensi downtime akibat resource exhaustion

---

## Kesimpulan

Implementasi monitoring dengan ELK Stack serta Prometheus dan Grafana memungkinkan deteksi dini terhadap ancaman keamanan. Dengan melakukan simulasi error aplikasi, brute force login, dan beban sistem tinggi, sistem monitoring mampu memberikan visibilitas terhadap indikasi serangan dan dampaknya. Monitoring yang baik menjadi fondasi penting dalam penerapan DevSecOps untuk menjaga keamanan dan ketersediaan sistem.
