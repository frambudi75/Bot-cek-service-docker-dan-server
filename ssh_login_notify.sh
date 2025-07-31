# ssh_login_notify.sh
# Tambahkan ini ke /etc/profile atau ~/.bashrc agar setiap login SSH akan mengirim notifikasi ke Telegram.

if [ -n "$SSH_CONNECTION" ]; then
  IP=$(echo $SSH_CONNECTION | awk '{print $1}')
  USER=$(whoami)
  HOST=$(hostname)
  TIME=$(date "+%Y-%m-%d %H:%M:%S")
  MESSAGE="🚨 SSH Login Detected\nUser: $USER\nIP: $IP\nHost: $HOST\nTime: $TIME"

  # Ganti dengan BOT_TOKEN dan CHAT_ID dari bot Telegram kamu
  TOKEN=\"ISI_BOT_TOKEN\"
  CHAT_ID=\"ISI_CHAT_ID\"

  curl -s -X POST \"https://api.telegram.org/bot$TOKEN/sendMessage\" \
    -d chat_id=\"$CHAT_ID\" -d text=\"$MESSAGE\"
fi
