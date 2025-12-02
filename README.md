# SensorsMonitoringSystem — High-Availability IoT Monitoring

![IoT](https://img.shields.io/badge/IoT-Project-blue?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-Compose-orange?style=flat-square) ![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

## 📖 Gambaran Umum

**SensorsMonitoringSystem** adalah simulasi arsitektur sistem pemantauan IoT yang dirancang untuk mendemonstrasikan konsep *High Availability* (HA) dan *Failover*. Proyek ini mensimulasikan lingkungan di mana sensor mengirimkan data secara terus-menerus ke sistem pusat melalui protokol MQTT, dengan mekanisme redundansi untuk memastikan data tetap terkirim meskipun broker utama mengalami gangguan.

Sistem ini terdiri dari komponen-komponen berikut:
- **MQTT Brokers (Failover Cluster):** Dua *instance* Mosquitto (Primary & Secondary) untuk menjamin ketersediaan layanan.
- **Sensor Nodes:** Beberapa *container* yang mensimulasikan perangkat IoT, mempublikasikan data telemetri ke topik MQTT.
- **Dashboard Monitoring:** Aplikasi berbasis web (Flask) yang berlangganan (*subscribe*) ke topik data sensor dan memvisualisasikan status secara *real-time*.

---

## 🛠️ Prasyarat Sistem

Sebelum menjalankan proyek ini, pastikan perangkat Anda telah memenuhi kebutuhan berikut:

1. **Docker Engine** & **Docker Compose** (versi terbaru direkomendasikan).
2. **Pengguna Windows:** Disarankan menggunakan **Docker Desktop** dengan backend **WSL2**.
3. Pastikan *port* host berikut tidak sedang digunakan oleh aplikasi lain: `1883`, `1884`, `5001`.

---

## 🚀 Panduan Memulai (Quick Start)

Ikuti langkah-langkah berikut untuk menjalankan seluruh stack aplikasi secara lokal.

### 1. Persiapan Lingkungan
Buka terminal dan arahkan direktori ke folder proyek:
```bash
cd IOTMonitoring
```

### 2. Build dan Jalankan Layanan
Jalankan perintah berikut untuk membangun *image* dan menjalankan *container*:
```bash
docker-compose up --build
```

### 3. Akses Dashboard
Setelah semua layanan berjalan, buka peramban (*browser*) Anda dan akses alamat berikut untuk melihat visualisasi data:
```text
http://localhost:5001
```

### 4. Menghentikan Layanan
Untuk menghentikan dan menghapus container yang berjalan:
```bash
docker-compose down
```

---

## ⚙️ Arsitektur & Konfigurasi Port

Berikut adalah rincian layanan dan pemetaan *port* yang digunakan dalam proyek ini:

| Service Name | Tipe Layanan | Port Internal | Port Host (Akses Luar) | Keterangan |
| :--- | :--- | :--- | :--- | :--- |
| `broker-primary` | MQTT Broker | 1883 | **1883** | Broker utama. |
| `broker-secondary` | MQTT Broker | 1883 | **1884** | Broker cadangan (*failover*). |
| `dashboard` | Web App (Flask) | 5000 | **5001** | Antarmuka pengguna. |
| `sensor-*` | Python Script | - | - | *Publisher* data (internal). |

### Struktur File Utama
* `docker-compose.yml`: Orkestrasi seluruh layanan dan jaringan.
* `mosquitto.conf`: Konfigurasi standar untuk kedua broker MQTT.
* `dashboard/`: Kode sumber aplikasi web (`app.py`), Dockerfile, dan dependensi.
* `sensor_node/`: Kode simulasi sensor (`main.py`) yang menangani logika pengiriman data.

---

## 📡 Format Data & Protokol

Agar data dapat ditampilkan dengan benar pada Dashboard, seluruh sensor harus mengikuti standar berikut:

* **Topik MQTT:** `sensor/<tipe_sensor>` (Contoh: `sensor/temperature`, `sensor/humidity`)
* **Format Payload (JSON):**

```json
{
  "sensor": "temperature",
  "value": 25.5,
  "broker_used": "broker-primary"
}
```

> **Catatan:** Field `broker_used` berguna untuk memantau broker mana yang sedang aktif melayani sensor tersebut.

---

## 🐛 Debugging & Monitoring Log

Berikut adalah perintah-perintah yang berguna untuk memantau status sistem:

**Melihat log seluruh layanan (Real-time):**
```bash
docker-compose logs -f
```

**Melihat log layanan spesifik:**
```bash
# Log Dashboard
docker-compose logs -f dashboard

# Log Sensor Tertentu
docker-compose logs -f sensor-temp
```

**Verifikasi pesan MQTT secara manual:**
Anda dapat berlangganan langsung ke topik untuk memastikan data terkirim:
```bash
# Melalui Host (jika mosquitto-clients terinstall)
mosquitto_sub -h localhost -p 1883 -t 'sensor/#' -v

# Melalui dalam Container
docker exec -it broker-primary mosquitto_sub -t 'sensor/#' -v
```

---

## ❓ Pemecahan Masalah (Troubleshooting)

Berikut adalah solusi untuk beberapa kendala yang umum terjadi:

### 1. Error `ModuleNotFoundError: No module named 'flask'`
Terjadi jika dependensi belum terinstall dalam *image*.
* **Solusi:** Pastikan `flask` dan `gunicorn` ada di `dashboard/requirements.txt`, lalu bangun ulang container:
    ```bash
    docker-compose build dashboard
    docker-compose up --build dashboard
    ```

### 2. Dashboard Kosong (Tidak Ada Data)
* **Penyebab:** Format data salah atau sensor gagal *publish*.
* **Solusi:**
    * Pastikan sensor mengirim ke topik `sensor/#`.
    * Pastikan payload berbentuk JSON valid yang mengandung *key* `sensor` dan `value`.

### 3. Sensor Terus Reconnect / Gagal Publish
* **Penyebab:** Konfigurasi host broker tidak sesuai atau masalah jaringan Docker.
* **Solusi:** Periksa variabel `BROKER_LIST` pada `sensor_node/main.py`. Pastikan nama host sesuai dengan nama service di docker-compose (`broker-primary`, `broker-secondary`).

---

## 🤝 Kontribusi

Kontribusi sangat terbuka untuk pengembangan proyek ini. Jika Anda ingin menambahkan fitur atau memperbaiki *bug*:

1. **Fork** repositori ini.
2. Buat **Branch** baru untuk fitur Anda.
3. Lakukan pengujian lokal dengan `docker-compose up`.
4. Ajukan **Pull Request** dengan deskripsi perubahan yang jelas.

---
*Dibuat untuk keperluan simulasi dan pembelajaran arsitektur IoT Terdistribusi.*