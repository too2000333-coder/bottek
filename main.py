import telebot
import requests

BOT_TOKEN = "8673932260:AAHfiFc_DPN82LzyxZd3obdzkmh-08LV99Q"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو تيك توك لتحميله بدون علامة مائية ✨")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text.strip()
    
    if "tiktok.com" not in url:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط فيديو تيك توك صحيح.")
        return

    msg = bot.reply_to(message, "⏳ جاري جلب وتحميل الفيديو...")

    try:
        api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
        response = requests.get(api_url).json()

        video_url = None
        if "video" in response and "noWatermark" in response["video"]:
            video_url = response["video"]["noWatermark"]
        elif "url" in response:
            video_url = response["url"]

        if video_url:
            bot.send_video(
                chat_id=message.chat.id,
                video=video_url,
                caption="🎬 تم التحميل بنجاح ✨"
            )
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        else:
            bot.edit_message_text("❌ تعذر جلب الفيديو، حاول مرة أخرى برابط آخر.", message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء التحميل: {str(e)}", message.chat.id, msg.message_id)

print("البوت يعمل...")
bot.infinity_polling()
