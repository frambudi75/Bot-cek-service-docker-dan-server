# Telegram Server & Docker Monitor Bot

Bot Telegram sederhana untuk:
- Cek status server (CPU, RAM, disk, uptime)
- Cek & kontrol service (nginx, mysql, dll)
- Monitoring container Docker (status, log, restart)

## Cara Pakai

1. Salin `.env.example` jadi `.env` dan isi token + user ID kamu
2. Install dependency:
   ```
   pip install -r requirements.txt
   ```
3. Jalankan bot:
   ```
   python bot.py
   ```

Bot akan membalas perintah dari Telegram seperti:
- /status
- /docker
- /dockerlogs nama_container
- /restart nginx

> Pastikan Docker dan Python 3.9+ sudah terinstall di server kamu.
