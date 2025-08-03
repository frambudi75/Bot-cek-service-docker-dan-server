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

# Utility function to execute shell commands safely
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

# Authorization check
def authorized_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not is_authorized(update):
            return
        return await func(update, context)
    return wrapper

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.reply_text("✅ Bot aktif. Ketik /help untuk daftar perintah.")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    msg = (
        "📌 Perintah Bot:\n"
        "/start - Mulai bot\n"
        "/help - Bantuan\n"
        "/status - Cek status server\n"
        "/service <nama> - Cek status service\n"
        "/restart <service> - Restart service\n"
        "/docker - Daftar container Docker\n"
        "/dockerstart <container> - Start container\n"
        "/dockerstop <container> - Stop container\n"
        "/dockerremove <container> - Hapus container\n"
        "/dockerinspect <container> - Inspect container\n"
        "/dockerlogs <container> - Lihat log\n"
        "/dockerrestart <container> - Restart container\n"
        "/dockerimages - Daftar image\n"
        "/dockerremoveimage <image> - Hapus image\n"
        "/dockerpull <image> - Tarik image\n"
        "/dockervolumes - Daftar volume\n"
        "/dockernetworks - Daftar network\n"
        "/ip - IP address\n"
        "/uptime - Uptime server\n"
        "/topcpu - Proses CPU terberat\n"
    )
    await update.message.reply_text(msg)

# Server status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    uptime = subprocess.getoutput("uptime -p")
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    ip_pub = requests.get("https://api.ipify.org").text

    msg = f"📊 STATUS SERVER:\nUptime: {uptime}\nCPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%\nIP Publik: {ip_pub}"
    await update.message.reply_text(msg)

# Service status
async def service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /service <nama_service>")
        return
    svc = context.args[0]
    status = subprocess.getoutput(f"systemctl is-active {svc}")
    await update.message.reply_text(f"Status {svc}: {status}")

# Restart service
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /restart <nama_service>")
        return
    svc = context.args[0]
    os.system(f"sudo systemctl restart {svc}")
    await update.message.reply_text(f"Service {svc} direstart.")

# Docker containers list
async def docker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    result = subprocess.getoutput("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
    await update.message.reply_text("📦 Docker Container:\n" + result)

# Start container
async def docker_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerstart <nama_container>")
        return
    name = context.args[0]
    result = run_command(f"docker start {name}")
    await update.message.reply_text(f"✅ Container `{name}` started.\n```\n{result}\n```", parse_mode='Markdown')

# Stop container
async def docker_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerstop <nama_container>")
        return
    name = context.args[0]
    result = run_command(f"docker stop {name}")
    await update.message.reply_text(f"⏹ Container `{name}` stopped.\n```\n{result}\n```", parse_mode='Markdown')

# Remove container
async def docker_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerremove <nama_container>")
        return
    name = context.args[0]
    result = run_command(f"docker rm {name}")
    await update.message.reply_text(f"🗑 Container `{name}` removed.\n```\n{result}\n```", parse_mode='Markdown')

# Inspect container
async def docker_inspect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerinspect <nama_container>")
        return
    name = context.args[0]
    result = run_command(f"docker inspect {name}")
    # Limit output to prevent message size issues
    if len(result) > 3000:
        result = result[:3000] + "\n... (output truncated)"
    await update.message.reply_text(f"🔍 Container `{name}` details:\n```\n{result}\n```", parse_mode='Markdown')

# Docker logs
async def docker_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerlogs <nama_container>")
        return
    name = context.args[0]
    result = subprocess.getoutput(f"docker logs --tail 20 {name}")
    await update.message.reply_text(f"📝 Log dari `{name}`:\n```\n{result}\n```", parse_mode='Markdown')

# Restart container
async def docker_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerrestart <nama_container>")
        return
    name = context.args[0]
    subprocess.run(f"docker restart {name}", shell=True)
    await update.message.reply_text(f"✅ Container `{name}` direstart.", parse_mode='Markdown')

# Docker images list
async def docker_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    result = subprocess.getoutput("docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}'")
    await update.message.reply_text("🖼 Docker Images:\n```\n" + result + "\n```", parse_mode='Markdown')

# Remove Docker image
async def docker_remove_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerremoveimage <image_name>")
        return
    name = context.args[0]
    result = run_command(f"docker rmi {name}")
    await update.message.reply_text(f"🗑 Image `{name}` removed.\n```\n{result}\n```", parse_mode='Markdown')

# Pull Docker image
async def docker_pull(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if len(context.args) == 0:
        await update.message.reply_text("Gunakan: /dockerpull <image_name>")
        return
    name = context.args[0]
    result = run_command(f"docker pull {name}")
    await update.message.reply_text(f"📥 Image `{name}` pull result:\n```\n{result}\n```", parse_mode='Markdown')

# Docker volumes list
async def docker_volumes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    result = subprocess.getoutput("docker volume ls --format 'table {{.Name}}\t{{.Driver}}\t{{.Scope}}'")
    await update.message.reply_text("💾 Docker Volumes:\n```\n" + result + "\n```", parse_mode='Markdown')

# Docker networks list
async def docker_networks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    result = subprocess.getoutput("docker network ls --format 'table {{.Name}}\t{{.Driver}}\t{{.Scope}}'")
    await update.message.reply_text("🌐 Docker Networks:\n```\n" + result + "\n```", parse_mode='Markdown')

# IP command
async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    ip_pub = requests.get("https://api.ipify.org").text
    ip_local = subprocess.getoutput("hostname -I").strip()
    await update.message.reply_text(f"🌐 IP Publik: {ip_pub}\n🏠 IP Lokal: {ip_local}")

# Uptime command
async def uptime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    uptime = subprocess.getoutput("uptime -p")
    await update.message.reply_text(f"⏱️ Uptime: {uptime}")

# Top CPU processes
async def topcpu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    result = subprocess.getoutput("ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6")
    await update.message.reply_text(f"🔥 Top Proses CPU:\n```\n{result}\n```", parse_mode='Markdown')

# Main application
app = ApplicationBuilder().token(TOKEN).build()

# Command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("service", service))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(CommandHandler("docker", docker))
app.add_handler(CommandHandler("dockerstart", docker_start))
app.add_handler(CommandHandler("dockerstop", docker_stop))
app.add_handler(CommandHandler("dockerremove", docker_remove))
app.add_handler(CommandHandler("dockerinspect", docker_inspect))
app.add_handler(CommandHandler("dockerlogs", docker_logs))
app.add_handler(CommandHandler("dockerrestart", docker_restart))
app.add_handler(CommandHandler("dockerimages", docker_images))
app.add_handler(CommandHandler("dockerremoveimage", docker_remove_image))
app.add_handler(CommandHandler("dockerpull", docker_pull))
app.add_handler(CommandHandler("dockervolumes", docker_volumes))
app.add_handler(CommandHandler("dockernetworks", docker_networks))
app.add_handler(CommandHandler("ip", ip_command))
app.add_handler(CommandHandler("uptime", uptime_command))
app.add_handler(CommandHandler("topcpu", topcpu_command))

# Run the bot
app.run_polling()
