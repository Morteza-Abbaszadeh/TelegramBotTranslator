

import telebot
from telebot import types
from googletrans import Translator, LANGUAGES


token = 'token'



bot = telebot.TeleBot(token)
translator = Translator()

# Language options
language_codes = {
    'English': 'en',
    'Persian': 'fa',
    'German': 'de',
    'Spanish': 'es',
    'Arabic': 'ar',
    'Chinese': 'zh-cn',
    'Japanese': 'ja',
    'Korean': 'ko'
}

# Temporary dictionary to store the user's input text and selected language
user_data = {}

# Start command handler
@bot.message_handler(commands=['start'])
def start_translation(message):
    bot.reply_to(message, "Please enter the text you want to translate:")
    bot.register_next_step_handler(message, get_text_to_translate)

# Get the text from the user
def get_text_to_translate(message):
    user_id = message.chat.id
    user_data[user_id] = {'text': message.text}  # Store the input text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for language in language_codes.keys():
        markup.add(language)
    bot.send_message(user_id, "Please select the target language:", reply_markup=markup)
    bot.register_next_step_handler(message, get_language)

# Get the selected language
def get_language(message):
    user_id = message.chat.id
    selected_language = message.text

    if selected_language in language_codes:
        user_data[user_id]['language'] = language_codes[selected_language]
        translate_text(message)
    else:
        bot.send_message(user_id, "Invalid language. Please try again.")
        bot.register_next_step_handler(message, get_language)

# Translate and send the result
def translate_text(message):
    user_id = message.chat.id
    input_text = user_data[user_id]['text']
    target_language = user_data[user_id]['language']

    try:
        translated = translator.translate(input_text, dest=target_language)
        bot.send_message(user_id, f"Translated text: {translated.text}")
    except Exception as e:
        bot.send_message(user_id, "Error during translation. Please try again.")

bot.polling()

