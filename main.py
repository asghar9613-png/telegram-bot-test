import os
import requests
import jdatetime
import random
from datetime import datetime

# ۱. دریافت توکن‌ها از سکرت‌های گیت‌هاب
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ۲. محاسبه تاریخ شمسی و روز هفته
days_of_week = {
    0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 
    3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"
}
current_gregorian_day = datetime.now().weekday()
day_name = days_of_week[current_gregorian_day]

# دریافت تاریخ شمسی امروز
shamsi_date = jdatetime.datetime.now().strftime("%Y/%m/%d")

# ۳. دریافت آنلاین وضعیت آب و هوای تهران
weather_text = "آب‌وهوا: در دسترس نیست"
try:
    weather_res = requests.get("https://wttr.in/Tehran?format=%C+++%t")
    if weather_res.status_code == 200:
        weather_text = f"🌤️ وضعیت هوای تهران: {weather_res.text.strip()}"
except Exception:
    pass

# ۴. بانک جملات مدیریتی و انگیزشی (ربات هر بار یکی را تصادفی انتخاب می‌کند)
quotes = [
    "«مدیریت یعنی هنر انجام کارها به وسیله دیگران و هدایت انرژی‌ها به سمت هدف.»",
    "«موفقیت نهایی نیست، شکست هم کشنده نیست؛ این شجاعتِ ادامه دادن است که حساب می‌شود.»",
    "«بهترین راه برای پیش‌بینی آینده، ساختن آن است.»",
    "«نظم و تداوم، تفاوت اصلی بین رویا و واقعیت است.»"
]
selected_quote = random.choice(quotes)

# ۵. ساختن بدنه نهایی گزارش مدیریتی آغاز روز
message = (
    f"📋 **گزارش مدیریتی آغاز روز**\n"
    f"━━━━━━━━━━━━━━━━━━\n"
    f"📅 **روز:** {day_name}\n"
    f"📆 **تاریخ:** {shamsi_date}\n"
    f"{weather_text}\n"
    f"━━━━━━━━━━━━━━━━━━\n"
    f"💡 **جمله مدیریتی روز:**\n"
    f"{selected_quote}\n\n"
    f"🚀 روز موفقی داشته باشی اصغر جان! سیستم آماده کار است."
)

# ۶. ارسال به تلگرام
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
response = requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
})

if response.status_code == 200:
    print("Advanced report sent successfully!")
else:
    print(f"Failed to send. Error: {response.text}")
