import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

app = ApplicationBuilder().token(TOKEN).build()


def is_valid(url):
    return "tiktok.com" in url or "instagram.com" in url


# 🔥 RUN HEAVY DOWNLOAD OUTSIDE EVENT LOOP
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not is_valid(url):
        await update.message.reply_text("Send TikTok or Instagram link")
        return

    msg = await update.message.reply_text("Downloading...")

    try:
        # 🔥 move blocking task to thread
        filename = await asyncio.to_thread(download_video, url)

        with open(filename, 'rb') as f:
            await update.message.reply_video(video=f)

        os.remove(filename)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"Error: {e}")


app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))


if __name__ == "__main__":
    print("🔥 BOT STARTED")
    app.run_polling(drop_pending_updates=True)
