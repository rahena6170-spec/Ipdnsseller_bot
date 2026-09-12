import os
import telebot
from telebot import types

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# ==========================================
# আপনার পেমেন্ট তথ্য ও এডমিন আইডি
# ==========================================
BINANCE_PAY_ID = "1228672891"
BYBIT_UID = "214653317"
BEP20_ADDRESS = "0x3afa44c7ac99faa566d5bc00f5dfe7d9f64273d6"
ADMIN_USERNAME = "@your_telegram_username"  # এখানে আপনার টেলিগ্রাম ইউজারনেম দিন (যেমন: @AdminName)
# ==========================================

user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton("📧 IP for Gmail Create (Oxylabs)", callback_data='cat_gmail')
    btn2 = types.InlineKeyboardButton("📱 IP for WhatsApp & Instagram", callback_data='cat_social')
    btn3 = types.InlineKeyboardButton("🌐 Premium DNS", callback_data='cat_dns')
    btn4 = types.InlineKeyboardButton("💬 সাপোর্ট / এডমিন", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")
    
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = f"স্বাগতম {message.from_user.first_name}!\n\nআপনার প্রয়োজনীয় সেবাটি নিচের অপশন থেকে নির্বাচন করুন:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id

    # ১. Gmail Create IP (Oxylabs Corporate)
    if call.data == 'cat_gmail':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Oxylabs Corporate 1 GB - $4", callback_data='pkg_Oxylabs Corporate 1GB ($4)'),
            types.InlineKeyboardButton("Oxylabs Corporate 2 GB - $8", callback_data='pkg_Oxylabs Corporate 2GB ($8)'),
            types.InlineKeyboardButton("Oxylabs Corporate 3 GB - $12", callback_data='pkg_Oxylabs Corporate 3GB ($12)'),
            types.InlineKeyboardButton("Oxylabs Corporate 4 GB - $15", callback_data='pkg_Oxylabs Corporate 4GB ($15)'),
            types.InlineKeyboardButton("Oxylabs Corporate 5 GB - $18", callback_data='pkg_Oxylabs Corporate 5GB ($18)'),
            types.InlineKeyboardButton("🔙 মূল মেনুতে ফিরুন", callback_data='main_menu')
        )
        bot.edit_message_text("📧 **IP for Gmail Create (Oxylabs Corporate):**", chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    # ২. Social Create IP Category (WhatsApp & Instagram)
    elif call.data == 'cat_social':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔹 9Proxy (5 GB - $1)", callback_data='pkg_9Proxy 5GB ($1)'),
            types.InlineKeyboardButton("🔹 Proxy-Seller (1 GB - $1.02)", callback_data='pkg_Proxy-Seller 1GB ($1.02)'),
            types.InlineKeyboardButton("🔙 মূল মেনুতে ফিরুন", callback_data='main_menu')
        )
        bot.edit_message_text("📱 **WhatsApp & Instagram Proxy Options:**", chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    # ৩. Premium DNS
    elif call.data == 'cat_dns':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Private DNS 1 Month - $1", callback_data='pkg_DNS 1 Month ($1)'),
            types.InlineKeyboardButton("Private DNS 2 Months - $2", callback_data='pkg_DNS 2 Months ($2)'),
            types.InlineKeyboardButton("Private DNS 6 Months - $6", callback_data='pkg_DNS 6 Months ($6)'),
            types.InlineKeyboardButton("Private DNS 1 Year (8 DNS) - $10", callback_data='pkg_DNS 1 Year ($10)'),
            types.InlineKeyboardButton("🔙 মূল মেনুতে ফিরুন", callback_data='main_menu')
        )
        bot.edit_message_text("🌐 **Premium DNS Packages:**", chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

    # ব্যাক টু মেইন মেনু
    elif call.data == 'main_menu':
        send_welcome(call.message)

    # প্যাকেজ সিলেক্ট করার পর পেমেন্ট মেথড শো করবে
    elif call.data.startswith('pkg_'):
        selected_pkg = call.data.replace('pkg_', '')
        user_states[chat_id] = {'selected_package': selected_pkg}
        
        payment_text = (
            f"📦 **নির্বাচিত প্যাকেজ:** {selected_pkg}\n\n"
            "💳 **আমাদের পেমেন্ট মেথডসমূহ:**\n"
            f"🔸 **Binance Pay ID:** `{BINANCE_PAY_ID}`\n"
            f"🔸 **Bybit UID:** `{BYBIT_UID}`\n"
            f"🔸 **BEP20 Address (USDT):**\n`{BEP20_ADDRESS}`\n\n"
            "⚠️ **পেমেন্ট সম্পন্ন করার পর নিচে চাপ দিয়ে আপনার Transaction Hash (TxID) অথবা স্ক্রিনশট সাবমিট করুন।**"
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📤 পেমেন্ট প্রুফ (Hash / Screenshot) পাঠান", callback_data='submit_proof'))
        bot.send_message(chat_id, payment_text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'submit_proof':
        user_states[chat_id]['awaiting_proof'] = True
        bot.send_message(chat_id, "অনুগ্রহ করে আপনার Transaction Hash (TxID) টাইপ করে পাঠান অথবা পেমেন্টের Screenshot আপলোড করুন:")

# স্ক্রিনশট বা টেক্সট/হ্যাশ হ্যান্ডলার
@bot.message_handler(content_types=['text', 'photo'])
def handle_proof(message):
    chat_id = message.chat.id
    
    if chat_id in user_states and user_states[chat_id].get('awaiting_proof'):
        pkg = user_states[chat_id].get('selected_package', 'N/A')
        username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
        user_info = f"👤 User: {username} (ID: `{chat_id}`)\n📦 Package: {pkg}"
        
        if message.content_type == 'text':
            proof_text = message.text
            bot.send_message(ADMIN_USERNAME, f"📥 **নতুন পেমেন্ট প্রুফ (Hash):**\n\n{user_info}\n\n🔑 **Hash/TxID:** `{proof_text}`", parse_mode='Markdown')
        
        elif message.content_type == 'photo':
            photo_id = message.photo[-1].file_id
            bot.send_photo(ADMIN_USERNAME, photo_id, caption=f"📥 **নতুন পেমেন্ট প্রুফ (Screenshot):**\n\n{user_info}", parse_mode='Markdown')

        bot.send_message(chat_id, "✅ আপনার পেমেন্ট প্রুফ সফলভাবে এডমিনের কাছে পাঠানো হয়েছে! ভেরিফাই করার পর খুব দ্রুত সার্ভিস দেওয়া হবে। ধন্যবাদ!")
        
        user_states[chat_id]['awaiting_proof'] = False

print("Bot is running...")
bot.infinity_polling()
