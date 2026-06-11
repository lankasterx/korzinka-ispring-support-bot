from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
import os

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = -5294785696

LANGUAGE, FIO, EMPLOYEE_ID, DEPARTMENT, PROBLEM, SCREENSHOT = range(6)

TEXTS = {
    "ru": {
        "welcome": "Здравствуйте! Выберите язык.",
        "fio": "Введите ваши ФИО:",
        "emp": "Введите табельный номер:",
        "dep": "Введите подразделение или магазин:",
        "problem": "Опишите проблему со входом в iSpring:",
        "screenshot": "Прикрепите скриншот ошибки или напишите 'Нет'.",
        "done": "Спасибо! Ваша заявка зарегистрирована.",
    },
    "uz": {
        "welcome": "Assalomu alaykum! Tilni tanlang.",
        "fio": "F.I.Sh. ni kiriting:",
        "emp": "Tabel raqamingizni kiriting:",
        "dep": "Bo‘lim yoki do‘konni kiriting:",
        "problem": "iSpring bilan bog‘liq muammoni tasvirlang:",
        "screenshot": "Xatolik skrinshotini yuboring yoki 'Yo‘q' deb yozing.",
        "done": "Rahmat! Murojaatingiz qabul qilindi.",
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🇷🇺 Русский", "🇺🇿 O'zbekcha"]]
    await update.message.reply_text(
        "Выберите язык / Tilni tanlang",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return LANGUAGE


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = "ru" if "Русский" in update.message.text else "uz"
    context.user_data["lang"] = lang

    await update.message.reply_text(TEXTS[lang]["fio"])
    return FIO


async def fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fio"] = update.message.text
    lang = context.user_data["lang"]

    await update.message.reply_text(TEXTS[lang]["emp"])
    return EMPLOYEE_ID


async def employee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["employee_id"] = update.message.text
    lang = context.user_data["lang"]

    await update.message.reply_text(TEXTS[lang]["dep"])
    return DEPARTMENT


async def department(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["department"] = update.message.text
    lang = context.user_data["lang"]

    await update.message.reply_text(TEXTS[lang]["problem"])
    return PROBLEM


async def problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["problem"] = update.message.text
    lang = context.user_data["lang"]

    await update.message.reply_text(TEXTS[lang]["screenshot"])
    return SCREENSHOT


async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]

    text = f"""
📩 Новая заявка iSpring

Язык: {lang}
ФИО: {context.user_data['fio']}
Табельный номер: {context.user_data['employee_id']}
Подразделение: {context.user_data['department']}

Проблема:
{context.user_data['problem']}
"""

    await context.bot.send_message(chat_id=GROUP_ID, text=text)

    if update.message.photo:
        photo = update.message.photo[-1].file_id
        await context.bot.send_photo(chat_id=GROUP_ID, photo=photo)

    await update.message.reply_text(TEXTS[lang]["done"])
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT, language)],
            FIO: [MessageHandler(filters.TEXT, fio)],
            EMPLOYEE_ID: [MessageHandler(filters.TEXT, employee)],
            DEPARTMENT: [MessageHandler(filters.TEXT, department)],
            PROBLEM: [MessageHandler(filters.TEXT, problem)],
            SCREENSHOT: [MessageHandler(filters.ALL, screenshot)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)

    app.run_polling()


if __name__ == "__main__":
    main()
