from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator
import pytesseract
from PIL import Image
import io

# نام کاربری کانال
CHANNEL_USERNAME = '@downloadpaviz'

# بررسی عضویت در کانال
def check_membership(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    try:
        member = context.bot.get_chat_member(CHANNEL_USERNAME, chat_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except:
        pass
    return False

# پردازش پیام خوشامدگویی
def start(update: Update, context: CallbackContext):
    if check_membership(update, context):
        update.message.reply_text("سلام! شما عضو کانال هستید و می‌توانید از ربات استفاده کنید.")
        update.message.reply_text("لطفاً یکی از گزینه‌ها رو انتخاب کنید:\n"
                                  "1. تبدیل عکس به متن\n"
                                  "2. ترجمه از فارسی به انگلیسی\n"
                                  "3. ترجمه از انگلیسی به فارسی")
    else:
        update.message.reply_text("برای استفاده از ربات، لطفاً ابتدا به کانال ما عضو شوید.")
        update.message.reply_text(f"برای عضویت، به این لینک بروید: {CHANNEL_USERNAME}")

# تبدیل عکس به متن
def image_to_text(image):
    text = pytesseract.image_to_string(image, lang='fas+eng')
    return text

# ترجمه متنی
def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

# پردازش پیام‌ها
def process_message(update: Update, context: CallbackContext):
    if check_membership(update, context):
        # بررسی اینکه آیا پیام شامل عکس است یا متن
        if update.message.photo:
            # گرفتن عکس ارسال شده
            photo = update.message.photo[-1].get_file()
            photo.download('photo.jpg')
            img = Image.open('photo.jpg')
            text = image_to_text(img)
            update.message.reply_text(f"متن استخراج شده از عکس: \n{text}")
        elif update.message.text:
            user_text = update.message.text.lower()
            if "تبدیل عکس به متن" in user_text:
                update.message.reply_text("لطفاً عکسی ارسال کنید.")
            elif "ترجمه از فارسی به انگلیسی" in user_text:
                update.message.reply_text("لطفاً متن فارسی خود را ارسال کنید.")
            elif "ترجمه از انگلیسی به فارسی" in user_text:
                update.message.reply_text("لطفاً متن انگلیسی خود را ارسال کنید.")
            else:
                update.message.reply_text("لطفاً یکی از گزینه‌ها رو انتخاب کنید:\n"
                                          "1. تبدیل عکس به متن\n"
                                          "2. ترجمه از فارسی به انگلیسی\n"
                                          "3. ترجمه از انگلیسی به فارسی")
    else:
        update.message.reply_text("برای استفاده از ربات، لطفاً ابتدا به کانال ما عضو شوید.")
        update.message.reply_text(f"برای عضویت، به این لینک بروید: {CHANNEL_USERNAME}")

# پردازش ترجمه
def process_translation(update: Update, context: CallbackContext):
    user_text = update.message.text
    if "فارسی به انگلیسی" in user_text:
        translated = translate_text(user_text, 'fa', 'en')
        update.message.reply_text(f"ترجمه به انگلیسی: {translated}")
    elif "انگلیسی به فارسی" in user_text:
        translated = translate_text(user_text, 'en', 'fa')
        update.message.reply_text(f"ترجمه به فارسی: {translated}")

# دستور شروع
def main():
    updater = Updater('8031137676:AAFk5lTgXWPyzAADl0AaxdEaDIO9TD06cIs', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))
    dp.add_handler(MessageHandler(Filters.photo, process_message))
    dp.add_handler(MessageHandler(Filters.text, process_translation))
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()