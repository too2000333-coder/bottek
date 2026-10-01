import telebot
import requests

TOKEN = '8673932260:AAHfiFc_DPN82LzyxZd3obdzkmh-08LV99Q'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو تيك توك وسأقوم بتحميله لك بدون علامة مائية.")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text.strip()
    
    if "tiktok.com" not in url:
        bot.reply_to(message, "يرجى إرسال رابط تيك توك صحيح.")
        return

    bot.reply_to(message, "جاري تحميل الفيديو، انتظر لحظة...")

    try:
        api_url = "https://www.tikwm.com/api/"
        response = requests.get(api_url, params={'url': url}).json()

        if response.get('code') == 0:
            video_url = response['data']['play']
            bot.send_video(message.chat.id, video_url)
        else:
            bot.reply_to(message, "عذراً، تعذر جلب الفيديو. تأكد من صحة الرابط.")
    except Exception as e:
        bot.reply_to(message, "حدث خطأ أثناء التحميل، يرجى المحاولة لاحقاً.")

bot.polling(none_stop=True)

