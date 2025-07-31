import os
import subprocess
import psutil
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER = int(os.getenv("ALLOWED_USER_ID"))

def is_authorized(update: Update):
    return update.effective_user.id == ALLOWED_USER

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    await update.message.reply_text("✅ Bot aktif. Ketik /help untuk daftar perintah.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    msg = (
        "📌 Perintah Bot:\n"
        "/status - Cek status server\n"
        "/service nginx - Status service\n"
        "/restart nginx - Restart service\n"
        "/docker - Daftar container Docker\n"
        "/dockerlogs nginx - Lihat log container\n"
        "/dockerrestart nginx - Restart container\n"
        "/ip - Lihat IP lokal & publik\n"
        "/uptime - Uptime server\n"
        "/topcpu - Proses paling tinggi CPU\n"
    )
    await update.message.reply_text(msg)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    uptime = subprocess.getoutput("uptime -p")
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    ip_pub = requests.get("https://api.ipify.org").text

    msg = f"""📊 STATUS SERVER:\nUptime: {uptime}\nCPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%\nIP Publik: {ip_pub}"""
    await update.message.reply_text(msg)

async def service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /service nginx")
        return
    svc = context.args[0]
    status = subprocess.getoutput(f"systemctl is-active {svc}")
    await update.message.reply_text(f"Status {svc}: {status}")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /restart nginx")
        return
    svc = context.args[0]
    os.system(f"sudo systemctl restart {svc}")
    await update.message.reply_text(f"Service {svc} direstart.")

async def docker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    result = subprocess.getoutput("docker ps -a --format '{{.Names}} | {{.Status}}'")
    await update.message.reply_text("📦 Docker Container:\n" + result)

async def docker_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerlogs nama_container")
        return
    name = context.args[0]
    result = subprocess.getoutput(f"docker logs --tail 20 {name}")
    await update.message.reply_text(f"📝 Log dari `{name}`:\n\n{result}", parse_mode='Markdown')

async def docker_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerrestart nama_container")
        return
    name = context.args[0]
    subprocess.run(f"docker restart {name}", shell=True)
    await update.message.reply_text(f"✅ Container `{name}` direstart.", parse_mode='Markdown')

async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    ip_pub = requests.get("https://api.ipify.org").text
    ip_local = subprocess.getoutput("hostname -I").strip()
    await update.message.reply_text(f"🌐 IP Publik: {ip_pub}\n🏠 IP Lokal: {ip_local}")

async def uptime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    uptime = subprocess.getoutput("uptime -p")
    await update.message.reply_text(f"⏱️ Uptime: {uptime}")

async def topcpu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update): return
    result = subprocess.getoutput("ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6")
    await update.message.reply_text(f"🔥 Top Proses CPU:\n\n{result}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("service", service))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(CommandHandler("docker", docker))
app.add_handler(CommandHandler("dockerlogs", docker_logs))
app.add_handler(CommandHandler("dockerrestart", docker_restart))
app.add_handler(CommandHandler("ip", ip_command))
app.add_handler(CommandHandler("uptime", uptime_command))
app.add_handler(CommandHandler("topcpu", topcpu_command))
app.run_polling()
