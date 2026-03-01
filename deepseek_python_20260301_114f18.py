import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time
import os

# Токен бота (замени на свой)
TOKEN = '7888076856:AAH76s_YqoRv0TQyI9z_Sn7E0vQcEM1bIhA'
# Твой личный Telegram ID (узнай у @userinfobot)
ADMIN_ID = 1825184352

bot = telebot.TeleBot(TOKEN)
user_themes = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    
    # Создаем клавиатуру с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        KeyboardButton("🎂 День рождения"),
        KeyboardButton("❤️ Признание"),
        KeyboardButton("💪 Поддержка"),
        KeyboardButton("🎁 Розыгрыш"),
        KeyboardButton("🎉 Праздник"),
        KeyboardButton("💍 Свадьба"),
        KeyboardButton("👶 Для детей"),
        KeyboardButton("🎵 Без повода"),
        KeyboardButton("✏️ Свой вариант")
    ]
    markup.add(*buttons)
    
    welcome_text = f"Привет, {first_name}!\nТвойХит на связи!\n\nКакую песню ты хотел бы создать?\n\nНу что, поехали?! 😊"
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [
    "🎂 День рождения", "❤️ Признание", "💪 Поддержка", 
    "🎁 Розыгрыш", "🎉 Праздник", "💍 Свадьба", 
    "👶 Для детей", "🎵 Без повода", "✏️ Свой вариант"
])
def handle_theme(message):
    chat_id = message.chat.id
    theme = message.text
    user_themes[chat_id] = theme
    
    bot.send_message(
        chat_id, 
        f"Отлично! Ты выбрал {theme}\n\n"
        "Теперь напиши пару фактов о человеке или событии:\n"
        "- Кому посвящается?\n"
        "- Какой повод?\n"
        "- Какие детали добавить? (характер, увлечения, смешные моменты)\n\n"
        "Чем подробнее, тем круче получится трек ✍️"
    )

@bot.message_handler(func=lambda message: True)
def handle_facts(message):
    chat_id = message.chat.id
    facts = message.text
    theme = user_themes.get(chat_id, "Не выбрана")
    
    user = message.from_user
    username = f"@{user.username}" if user.username else "нет username"
    
    # Отправляем уведомление админу
    admin_msg = (
        f"📩 НОВЫЙ ЗАКАЗ!\n\n"
        f"Тема: {theme}\n"
        f"Факты: {facts}\n\n"
        f"От: {user.first_name}\n"
        f"Username: {username}\n"
        f"ID: {chat_id}"
    )
    bot.send_message(ADMIN_ID, admin_msg)
    
    # Подтверждаем пользователю
    bot.send_message(
        chat_id,
        "✅ Спасибо! Твоя заявка принята.\n\n"
        "Я скоро создам трек и пришлю его сюда. Обычно это занимает 5-10 минут.\n\n"
        "Хочешь сделать еще одну песню? Нажми /start"
    )
    
    if chat_id in user_themes:
        del user_themes[chat_id]

print("Бот запущен...")
bot.infinity_polling()