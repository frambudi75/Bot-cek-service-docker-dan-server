
# 🛠️ Telegram Docker & Service Bot

Bot ini digunakan untuk mengontrol dan memantau server Linux (termasuk service systemd dan Docker container) langsung dari Telegram.

---

## 📦 Fitur Utama

- Cek status server: uptime, CPU, RAM, disk
- Kontrol Docker container (start, stop, restart, logs, inspect, remove, pull)
- Restart systemd service
- Perintah praktis via Telegram

---

## 🚀 Instalasi di Server

### 1. Clone Repositori

```bash
git clone https://github.com/frambudi75/Bot-cek-service-docker-dan-server.git
cd Bot-cek-service-docker-dan-server
```

### 2. Buat Virtual Environment (opsional)

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependency

```bash
pip install -r requirements.txt
```

### 4. Buat File `.env`

```bash
cp .env.example .env
```

Edit `.env`:

```
BOT_TOKEN=isi_token_bot_anda
ALLOWED_USER_ID=123456789
```

---

## ▶️ Menjalankan Bot Manual

```bash
python3 bot.py
```

---

## 🔁 Menjalankan Otomatis dengan systemd

### 1. Buat File Service

```bash
sudo nano /etc/systemd/system/telegrambot.service
```

Isi:

```
[Unit]
Description=Telegram Docker Bot
After=network.target

[Service]
User=habib
WorkingDirectory=/home/habib/Bot-cek-service-docker-dan-server
ExecStart=/usr/bin/python3 /home/habib/Bot-cek-service-docker-dan-server/bot.py
Restart=always
Environment=BOT_TOKEN=isi_token
Environment=ALLOWED_USER_ID=123456789

[Install]
WantedBy=multi-user.target
```

### 2. Reload dan Enable Service

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable telegrambot
sudo systemctl start telegrambot
```

---

## 🔐 Izin sudo (untuk restart service)

Edit sudoers:

```bash
sudo visudo
```

Tambahkan:

```
habib ALL=(ALL) NOPASSWD: /bin/systemctl restart *
```

Untuk Docker:

```bash
sudo usermod -aG docker sudo_user
```

Lalu restart server.

---

## ✅ Perintah di Telegram

Ketik `/help` di bot untuk melihat semua perintah:

Contoh:
- `/status`
- `/restart nginx`
- `/dockerstart portainer`
- `/dockerpull nginx`
- `/topcpu`

---

## 👤 Dibuat oleh

**Habib Frambudi** – [github.com/frambudi75](https://github.com/frambudi75)
