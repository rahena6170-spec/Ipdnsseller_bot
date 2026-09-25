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

# Payment Details
NAGAD_NUMBER = "01641208274"
BINANCE_PAY_ID = "1228672891"
BYBIT_UID = "214653317"
BEP20_ADDRESS = "0x3afa44c7ac99faa566d5bc00f5dfe7d9f64273d6"

ADMIN_HANDLE = "Gmailbuysell18"
CHANNEL_USERNAME = "@Global_gmail_tricks"

user_states = {}

# --- Helper Function: Check Channel Membership ---
def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        return True

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Check if user is subscribed to the channel
    if not is_user_subscribed(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        clean_channel_handle = CHANNEL_USERNAME.replace('@', '')
        btn_channel = types.InlineKeyboardButton("📢 Join Official Channel", url=f"https://t.me/{clean_channel_handle}")
        btn_check = types.InlineKeyboardButton("✅ Joined / Check Status", callback_data='check_join')
        markup.add(btn_channel, btn_check)
        
        join_msg = (
            f"🚫 **ACCESS RESTRICTED**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ You must join our official channel to use this bot:\n"
            f"👉 {CHANNEL_USERNAME}\n\n"
            f"🔹 *Join the channel and click 'Joined / Check Status' below.*"
        )
        bot.send_message(message.chat.id, join_msg, parse_mode='Markdown', reply_markup=markup)
        return

    user_states.pop(user_id, None)
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_ip_dns = types.InlineKeyboardButton("🌐 Buy IP & DNS", callback_data='cat_ip_dns')
    btn_bypass = types.InlineKeyboardButton("🛠️ Gmail Bypass Tools", callback_data='gmail_bypass')
    btn_support = types.InlineKeyboardButton("💬 Support / Admin", url=f"https://t.me/{ADMIN_HANDLE}")
    
    markup.add(btn_ip_dns, btn_bypass, btn_support)
    welcome_text = (
        "🤖 **WELCOME TO SERVICES HUB**\n\n"
        f"Welcome {message.from_user.first_name}!\n\n"
        "👇 *Please select an option from the menu below:*"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    # Handle Force Join verification check
    if call.data == 'check_join':
        if is_user_subscribed(user_id):
            bot.answer_callback_query(call.id, "✅ Verification Successful! Welcome to the bot.")
            send_welcome(call.message)
        else:
            bot.answer_callback_query(call.id, "❌ You haven't joined the channel yet! Please join first.", show_alert=True)
        return

    if call.data == 'main_menu':
        send_welcome(call.message)

    elif call.data == 'cat_ip_dns':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Oxylabs Corporate 1 GB - $3", callback_data='pkg_Oxylabs Corporate 1GB_$3_390 BDT'),
            types.InlineKeyboardButton("Oxylabs Corporate 2 GB - $4", callback_data='pkg_Oxylabs Corporate 2GB_$4_520 BDT'),
            types.InlineKeyboardButton("Oxylabs Corporate 3 GB - $6", callback_data='pkg_Oxylabs Corporate 3GB_$6_780 BDT'),
            types.InlineKeyboardButton("Private DNS 1 Month - $1", callback_data='pkg_Private DNS 1 Month_$1_130 BDT'),
            types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')
        )
        bot.edit_message_text(
            "🌐 **IP & DNS Packages:**\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Select your required package:",
            chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup
        )

    elif call.data == 'gmail_bypass':
        if chat_id not in user_states:
            user_states[chat_id] = {}
        user_states[chat_id]['service_type'] = 'bypass_tool'
        user_states[chat_id]['usd_price'] = '5 USD'
        user_states[chat_id]['bdt_price'] = '640 BDT'
        user_states[chat_id]['step'] = 'waiting_for_android_screenshot'
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu'))
        
        bot.edit_message_text(
            "🛠️ **GMAIL BYPASS TOOLS**\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📱 **Step 1:** Please send a screenshot of your device's Android version.",
            chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup
        )

    elif call.data.startswith('pkg_'):
        parts = call.data.replace('pkg_', '').split('_')
        pkg_name = parts[0]
        usd_val = parts[1]
        bdt_val = parts[2]

        if chat_id not in user_states:
            user_states[chat_id] = {}
        user_states[chat_id]['selected_package'] = pkg_name
        user_states[chat_id]['usd_price'] = usd_val
        user_states[chat_id]['bdt_price'] = bdt_val
        user_states[chat_id]['service_type'] = 'ip_dns'

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(f"NAGAD ({bdt_val})", callback_data='pay_nagad'),
            types.InlineKeyboardButton(f"BINANCE ({usd_val})", callback_data='pay_binance'),
            types.InlineKeyboardButton(f"BYBIT ({usd_val})", callback_data='pay_bybit'),
            types.InlineKeyboardButton(f"USDT BEP20 ({usd_val})", callback_data='pay_bep20'),
            types.InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu')
        )
        bot.edit_message_text(
            f"📦 **Selected:** {pkg_name}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 **Select Payment Method:**",
            chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup
        )

    elif call.data == 'select_payment':
        usd_val = user_states.get(chat_id, {}).get('usd_price', '5 USD')
        bdt_val = user_states.get(chat_id, {}).get('bdt_price', '640 BDT')
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(f"NAGAD ({bdt_val})", callback_data='pay_nagad'),
            types.InlineKeyboardButton(f"BINANCE ({usd_val})", callback_data='pay_binance'),
            types.InlineKeyboardButton(f"BYBIT ({usd_val})", callback_data='pay_bybit'),
            types.InlineKeyboardButton(f"USDT BEP20 ({usd_val})", callback_data='pay_bep20'),
            types.InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu')
        )
        bot.edit_message_text(
            "💳 **SELECT PAYMENT METHOD**\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your preferred payment method:",
            chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup
        )

    elif call.data in ['pay_nagad', 'pay_binance', 'pay_bybit', 'pay_bep20']:
        usd_val = user_states.get(chat_id, {}).get('usd_price', '5 USD')
        bdt_val = user_states.get(chat_id, {}).get('bdt_price', '640 BDT')

        method_map = {
            'pay_nagad': ("Nagad", f"Send Money Amount: `{bdt_val}`\nPayment Number: `{NAGAD_NUMBER}`"),
            'pay_binance': ("Binance", f"Pay Amount: `{usd_val}`\nBinance UID: `{BINANCE_PAY_ID}`"),
            'pay_bybit': ("Bybit", f"Pay Amount: `{usd_val}`\nBybit UID: `{BYBIT_UID}`"),
            'pay_bep20': ("USDT BEP20", f"Pay Amount: `{usd_val}`\nWallet Address: `{BEP20_ADDRESS}`")
        }
        method_name, details = method_map[call.data]
        
        if chat_id not in user_states:
            user_states[chat_id] = {}
        user_states[chat_id]['payment_method'] = method_name
        user_states[chat_id]['step'] = 'waiting_for_txid'

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔄 Change Method", callback_data='select_payment'),
            types.InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu')
        )
        
        bot.edit_message_text(
            f"💳 **{method_name.upper()} PAYMENT DETAILS**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{details}\n\n"
            f"⚠️ **Important:** Complete the payment and send your Transaction ID / Hash ID below in the chat:",
            chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=markup
        )

@bot.message_handler(content_types=['photo', 'text'])
def handle_user_input(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if chat_id not in user_states:
        return

    step = user_states[chat_id].get('step')

    # Step 1: Receiving Android Version Screenshot for Bypass Tools
    if step == 'waiting_for_android_screenshot':
        if message.photo:
            user_states[chat_id]['step'] = 'select_payment'
            usd_val = user_states[chat_id].get('usd_price', '5 USD')
            bdt_val = user_states[chat_id].get('bdt_price', '640 BDT')

            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(f"NAGAD ({bdt_val})", callback_data='pay_nagad'),
                types.InlineKeyboardButton(f"BINANCE ({usd_val})", callback_data='pay_binance'),
                types.InlineKeyboardButton(f"BYBIT ({usd_val})", callback_data='pay_bybit'),
                types.InlineKeyboardButton(f"USDT BEP20 ({usd_val})", callback_data='pay_bep20'),
                types.InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu')
            )
            bot.send_message(
                chat_id,
                "✅ **Screenshot Received!**\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "💳 **Step 2:** Please select your payment method:",
                parse_mode='Markdown',
                reply_markup=markup
            )
        else:
            bot.send_message(chat_id, "⚠️ Please send a valid screenshot of your Android version.")
        return

    # Step 2: Receiving Transaction ID / Hash ID
    if step == 'waiting_for_txid' and message.text:
        txid = message.text.strip()
        payment_method = user_states[chat_id].get('payment_method', 'Unknown')
        service_type = user_states[chat_id].get('service_type', 'General')
        selected_pkg = user_states[chat_id].get('selected_package', 'Gmail Bypass Tool')

        admin_notification = (
            f"🚨 **NEW PAYMENT SUBMISSION!**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **User ID:** `{user_id}`\n"
            f"📦 **Service/Package:** {selected_pkg if service_type == 'ip_dns' else 'Gmail Bypass Tool'}\n"
            f"🏷️ **Method:** {payment_method}\n"
            f"🔑 **TxID / Hash:** `{txid}`"
        )

        try:
            bot.send_message(ADMIN_HANDLE if ADMIN_HANDLE.startswith('@') else f"@{ADMIN_HANDLE}", admin_notification, parse_mode='Markdown')
        except Exception:
            pass

        markup = types.InlineKeyboardMarkup()
        btn_admin = types.InlineKeyboardButton(f"📩 Contact Admin (@{ADMIN_HANDLE})", url=f"https://t.me/{ADMIN_HANDLE}")
        markup.add(btn_admin)

        bot.send_message(
            chat_id,
            f"❌ **TRANSACTION ID SUBMITTED**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Submitted TxID: `{txid}`\n\n"
            f"⚠️ If your transaction ID is incorrect or for instant access, please contact our admin @{ADMIN_HANDLE}.\n"
            f"Once you message the admin, you will receive your menu/access!",
            parse_mode='Markdown',
            reply_markup=markup
        )
        user_states.pop(chat_id, None)
        return

if __name__ == '__main__':
    # Start Web Server in background thread
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("Bot starting...")
    bot.infinity_polling()
    
