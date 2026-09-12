import os
import threading
from flask import Flask
import telebot
from telebot import types

# --- Flask Server setup to keep Render awake ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Telegram Bot setup ---
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

BINANCE_PAY_ID = "1228672891"
BYBIT_UID = "214653317"
BEP20_ADDRESS = "0x3afa44c7ac99faa566d5bc00f5dfe7d9f64273d6"
ADMIN_HANDLE = "Ipdnssellersupport"

user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📧 IP for Gmail Create (Oxylabs)", callback_data='cat_gmail')
    btn2 = types.InlineKeyboardButton("📱 IP for WhatsApp & Instagram", callback_data='cat_social')
    btn3 = types.InlineKeyboardButton("🌐 Premium DNS", callback_data='cat_dns')
    # 🆕 New Category: Gmail Tools & Setup Video
    btn_tools = types.InlineKeyboardButton("📹 Gmail Tools & Setup Video ($3)", callback_data='pkg_Gmail Tools & Setup Video ($3)')
    btn4 = types.InlineKeyboardButton("💬 Support / Admin", url=f"https://t.me/{ADMIN_HANDLE}")
    
    markup.add(btn1, btn2, btn3, btn_tools, btn4)
    welcome_text = f"Welcome {message.from_user.first_name}!\n\nPlease select your required service from the options below:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id

    if call.data == 'cat_gmail':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Oxylabs Corporate 1 GB - $4", callback_data='pkg_Oxylabs Corporate 1GB ($4)'),
            types.InlineKeyboardButton("Oxylabs Corporate 2 GB - $8", callback_data='pkg_Oxylabs Corporate 2GB ($8)'),
            types.InlineKeyboardButton("Oxylabs Corporate 3 GB - $12", callback_data='pkg_Oxylabs Corporate 3GB ($12)'),
            types.InlineKeyboardButton("Oxylabs Corporate 4 GB - $15", callback_data='pkg_Oxylabs Corporate 4GB ($15)'),
            types.InlineKeyboardButton("Oxylabs Corporate 5 GB - $18", callback_data='pkg_Oxylabs Corporate 5GB ($18)'),
            types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')
        )
        bot.edit_message_text("📧 **IP for Gmail Create (Oxylabs Corporate):**", chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'cat_social':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔹 9Proxy (1 GB - $1)", callback_data='pkg_9Proxy 1GB ($1)'),
            types.InlineKeyboardButton("🔹 Proxy-Seller (1 GB - $1.02)", callback_data='pkg_Proxy-Seller 1GB ($1.02)'),
            types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')
        )
        bot.edit_message_text("📱 **WhatsApp & Instagram Proxy Options:**", chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'cat_dns':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Private DNS 1 Month - $1", callback_data='pkg_DNS 1 Month ($1)'),
            types.InlineKeyboardButton("Private DNS 2 Months - $2", callback_data='pkg_DNS 2 Months ($2)'),
            types.InlineKeyboardButton("Private DNS 6 Months - $6", callback_data='pkg_DNS 6 Months ($6)'),
            types.InlineKeyboardButton("Private DNS 1 Year (8 DNS) - $10", callback_data='pkg_DNS 1 Year ($10)'),
            types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')
        )
        bot.edit_message_text("🌐 **Premium DNS Packages:**", chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'main_menu':
        send_welcome(call.message)

    elif call.data.startswith('pkg_'):
        selected_pkg = call.data.replace('pkg_', '')
        user_states[chat_id] = {'selected_package': selected_pkg}
        payment_text = (
            f"📦 **Selected Package:** {selected_pkg}\n\n"
            "💳 **Payment Methods:**\n"
            f"🔸 **Binance Pay ID:** `{BINANCE_PAY_ID}`\n"
            f"🔸 **Bybit UID:** `{BYBIT_UID}`\n"
            f"🔸 **BEP20 Address (USDT):**\n`{BEP20_ADDRESS}`\n\n"
            "⚠️ **After completing payment, click below to submit your Transaction Hash (TxID) or Screenshot.**"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📤 Submit Payment Proof", callback_data='submit_proof'))
        bot.send_message(chat_id, payment_text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'submit_proof':
        if chat_id not in user_states:
            user_states[chat_id] = {}
        user_states[chat_id]['awaiting_proof'] = True
        bot.send_message(chat_id, "Please type your Transaction Hash (TxID) or send the payment Screenshot:")

@bot.message_handler(content_types=['text', 'photo'])
def handle_proof(message):
    chat_id = message.chat.id
    if chat_id in user_states and user_states[chat_id].get('awaiting_proof'):
        
        markup = types.InlineKeyboardMarkup()
        btn_admin = types.InlineKeyboardButton("💬 Contact Admin Now", url=f"https://t.me/{ADMIN_HANDLE}")
        markup.add(btn_admin)
        
        error_text = (
            "❌ **Verification Failed!**\n\n"
            "System could not verify this Transaction Hash/Screenshot automatically.\n\n"
            "Please click the button below to send your payment proof directly to the **Admin** for instant manual verification and proxy delivery."
        )
        
        bot.send_message(chat_id, error_text, parse_mode='Markdown', reply_markup=markup)
        user_states[chat_id]['awaiting_proof'] = False

if __name__ == '__main__':
    # Start Web Server in background thread
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("Bot starting...")
    bot.infinity_polling()
    
