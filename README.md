# 🔧 Telegram Server & Docker Monitor Bot

Bot Telegram sederhana untuk monitoring server Linux (Ubuntu/Debian), termasuk:
- 🔍 Cek status server: CPU, RAM, Disk, IP publik, uptime
- 🧰 Cek & kontrol service: nginx, mysql, dll
- 🐳 Monitoring container Docker (status, log, restart)
- 🔔 Notifikasi otomatis saat login SSH

---

## 📦 Fitur Utama

| Command Telegram       | Fungsi                                   |
|------------------------|-------------------------------------------|
| `/status`              | Info CPU, RAM, disk, IP publik, uptime    |
| `/service nginx`       | Cek status service tertentu               |
| `/restart nginx`       | Restart service tertentu                  |
| `/docker`              | Tampilkan semua container Docker          |
| `/dockerlogs nginx`    | Lihat 20 baris terakhir log container     |
| `/dockerrestart nginx` | Restart container Docker tertentu         |

---

## 🚀 Instalasi Bot

### 1. Install Python & pip

Untuk Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

> Cek versi Python:
```bash
python3 --version
```

Minimal Python **3.9** disarankan.

---

### 2. Clone Repo dan Install Dependensi

```bash
git clone https://github.com/kamu/telegram-docker-bot.git
cd telegram-docker-bot
pip3 install -r requirements.txt
```

---

### 3. Konfigurasi `.env`

Salin `.env.example` ke `.env` lalu edit:

```bash
cp .env.example .env
nano .env
```

Isi:

```env
BOT_TOKEN=123456789:ABCDEF_token_dari_BotFather
ALLOWED_USER_ID=123456789
```

- `BOT_TOKEN`: didapat dari @BotFather
- `ALLOWED_USER_ID`: user ID kamu, bisa dapat dari bot dengan `/start`

---

### 4. Jalankan Bot

```bash
python3 bot.py
```

---

## 🔐 SSH Login Notification (Opsional)

Agar setiap login SSH ke server kamu memicu notifikasi ke Telegram:

1. Buka file `.bashrc` atau `/etc/profile`:
```bash
sudo nano /etc/profile
```

2. Tambahkan di akhir:
```bash
bash /path/ke/ssh_login_notify.sh
```

3. Edit `ssh_login_notify.sh`, isi token & chat_id:
```bash
TOKEN="BOT_TOKEN"
CHAT_ID="USER_CHAT_ID"
```

4. Simpan & tes login SSH

---

## 🛠 Autostart dengan systemd (Opsional)

1. Buat file `/etc/systemd/system/telegrambot.service`:

```ini
[Unit]
Description=Telegram Docker Bot
After=network.target

[Service]
User=yourusername
WorkingDirectory=/home/yourusername/telegram-docker-bot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Enable service:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable telegrambot
sudo systemctl start telegrambot
```

---

## ✅ Lisensi

Proyek ini open-source. Bebas digunakan, dimodifikasi dan disebarkan. Kredit ke pembuat sangat dihargai 🙏

---

## 📮 Kontak

Untuk dukungan, ide fitur, atau kerja sama:
- Email: [frambudihabib@gmail.com](mailto:frambudihabib@gmail.com)
