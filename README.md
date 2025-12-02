
**SensorsMonitoringSystem — High-Availability IoT Monitoring (README)**

Ringkasan singkat
- Project ini men-simulasikan sistem monitoring IoT yang terdiri dari:
  - Dua instance Mosquitto (broker-primary, broker-secondary) untuk demo failover/HA.
  - Beberapa container sensor yang mem-publish data ke topik MQTT.
  - Sebuah dashboard berbasis Flask yang berlangganan topik `sensor/#` dan menampilkan nilai sensor.

Tujuan README ini
- Panduan cepat agar pengguna (pengembang/pengetes) dapat membangun, menjalankan, dan menguji proyek ini secara lokal.

Prasyarat
- Docker (Engine) dan Docker Compose tersedia dan berjalan.
- Jika di Windows: gunakan Docker Desktop (WSL2 direkomendasikan) dan pastikan resource/port tidak diblokir.

Quick start (jalankan seluruh stack)
1. Buka terminal di folder proyek (`IOTMonitoring`).
2. Build dan jalankan semua service:

```bash
docker-compose up --build
```

3. Akses dashboard di browser:

```text
http://localhost:5001
```

4. Hentikan semua service:

```bash
docker-compose down
```

Penjelasan port dan layanan
- `broker-primary` — Mosquitto, host port `1883` -> container `1883`.
- `broker-secondary` — Mosquitto cadangan, host port `1884` -> container `1883`.
- `dashboard` — Flask app, container mendengarkan `5000`, dipetakan ke host `5001`.

Struktur file penting
- `docker-compose.yml` — konfigurasi layanan dan jaringan.
- `mosquitto.conf` — konfigurasi Mosquitto yang dipakai kedua broker.
- `dashboard/` — aplikasi Flask (`app.py`), `Dockerfile`, `requirements.txt`.
- `sensor_node/` — simulator sensor (`main.py`), `Dockerfile`, `requirements.txt`.

Format data yang direkomendasikan
- Topik MQTT: `sensor/<type>` (contoh: `sensor/temperature`).
- Contoh payload JSON:

```json
{"sensor": "temperature", "value": 25.5, "broker_used": "broker-primary"}
```

Debugging & perintah berguna
- Tampilkan semua log (real time):

```bash
docker-compose logs -f
```

- Log dashboard saja:

```bash
docker-compose logs -f dashboard
```

- Log sensor (mis. temperature):

```bash
docker-compose logs -f sensor-temp
```

- Cek container berjalan / port mapping:

```bash
docker ps
```

- Subscribing langsung ke broker untuk melihat pesan:

```bash
# dari host (jika mosquitto_sub tersedia)
mosquitto_sub -h localhost -p 1883 -t 'sensor/#' -v

# atau dari dalam container broker-primary
docker exec -it broker-primary mosquitto_sub -t 'sensor/#' -v
```

Masalah umum & solusi singkat
- `ModuleNotFoundError: No module named 'flask'` saat memulai dashboard:
  - Pastikan `dashboard/requirements.txt` mencantumkan `Flask` dan `gunicorn`, lalu rebuild service:

```bash
docker-compose build dashboard
docker-compose up --build dashboard
```

- Dashboard tampil tetapi kosong (tidak ada sensor):
  - Pastikan sensor mem-publish ke topik `sensor/#` dan payload berformat JSON dengan `sensor` dan `value`.
  - Periksa log sensor dan dashboard untuk melihat apakah koneksi/publish terjadi.

- Sensor terus reconnect / tidak bisa publish:
  - Pastikan `BROKER_LIST` dalam `sensor_node/main.py` berisi nama service yang sesuai (`broker-primary`, `broker-secondary`).
  - Periksa jaringan Docker dan firewall.

Rebuild service tertentu

```bash
docker-compose build sensor-temp
docker-compose up -d sensor-temp
```

Kontribusi & pengembangan
- Jika ingin menambahkan fitur atau memperbaiki bug:
 1. Fork repo dan buat branch baru.
 2. Uji perubahan secara lokal dengan `docker-compose up --build`.
 3. Ajukan pull request dengan deskripsi perubahan.

Lisensi
- (Tambahkan lisensi proyek jika ingin dipublikasikan; contoh: MIT)

Butuh bantuan?
- Kalau perlu saya bantu standardisasi topik/payload atau buat script setup, beri tahu apa yang ingin disederhanakan.

