import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

TOKEN = os.getenv("TOKEN")

# BOT
app = ApplicationBuilder().token(TOKEN).build()

def is_valid(url):
    return "tiktok.com" in url or "instagram.com" in url

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not is_valid(url):
        await update.message.reply_text("Send TikTok or Instagram link")
        return

    msg = await update.message.reply_text("Downloading...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(filename, 'rb'))
        os.remove(filename)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"Error: {e}")

# ✅ ADD HANDLER (THIS WAS MISSING)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

# FLASK
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running"

def run_web():
    flask_app.run(host="0.0.0.0", port=10000, use_reloader=False)

def run_bot():
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    print("🔥 BOT FILE IS RUNNING")
    threading.Thread(target=run_web, daemon=True).start()
    run_bot()
