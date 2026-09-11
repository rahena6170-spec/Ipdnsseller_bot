import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# আপনার বিক্রি করার স্যাম্পল আইপি স্টক (প্রয়োজন অনুযায়ী পরিবর্তন করতে পারবেন)
ip_stock = [
    "192.168.1.1:8080:user1:pass1",
    "192.168.1.2:8080:user2:pass2"
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn_buy = InlineKeyboardButton("🛒 প্রাইস লিস্ট ও তথ্য", callback_data="price_list")
    btn_sample = InlineKeyboardButton("🎁 Free Sample IP", callback_data="get_sample")
    btn_admin = InlineKeyboardButton("💬 সাপোর্ট / এডমিন", url="https://t.me/GmailTricksGlobal") # আপনার চ্যানেলের ইউজারনেম দেওয়া হলো
    
    markup.add(btn_buy)
    markup.add(btn_sample)
    markup.add(btn_admin)
    
    bot.reply_to(message, f"স্বাগতম {message.from_user.first_name}!\nনিচের অপশন থেকে সিলেক্ট করুন:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "price_list":
        msg = (
            "📌 **আমাদের আইপি প্যাকেজ:**\n\n"
            "1️⃣ Residential IP - ৳১৫ / দিন\n"
            "2️⃣ Datacenter IP - ৳১০ / দিন\n\n"
            "💳 **পেমেন্ট:** বিকাশ / নগদ\n"
            "আইপি কিনতে সরাসরি এডমিনকে মেসেজ দিন।"
        )
        bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")
        
    elif call.data == "get_sample":
        if ip_stock:
            assigned_ip = ip_stock.pop(0)
            bot.send_message(call.message.chat.id, f"আপনার ফ্রি স্যাম্পল আইপি:\n`{assigned_ip}`", parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, "দুঃখিত, এই মুহূর্তে কোনো ফ্রি স্যাম্পল স্টক খালি নেই।")

if __name__ == "__main__":
    bot.infinity_polling()
    
