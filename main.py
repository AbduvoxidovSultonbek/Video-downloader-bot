

import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder,MessageHandler,filters,ContextTypes

TOKEN = "7469155829:AAEBuYTOgocOszms_KMe8Zh2p-46j4TBCA4"

def is_valid(url):
    return "tiktok.com" in url or "instagram.com" in url

async def handle(update:Update,context:ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not is_valid(url):
        await update.message.reply_text("Send TikTok or Instagram link")
        return

    msg = await update.message.reply_text("Downloading...")

    ydl_opts = {
        'format': 'best',
        'merge_output_format': 'mp4',
        'outtmpl': 'video.%(ext)s',
        'noplaylist':True,
        'quiet': True,
        'geo_bypass':True

    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        size = os.path.getsize(filename)

        if size>49*1024*1024:
            os.remove(filename)
            await msg.edit_text("Video size too large")
            return

        await update.message.reply_video(video=open(filename, 'rb'))
        os.remove(filename)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT&~filters.COMMAND, handle))

app.run_polling()


