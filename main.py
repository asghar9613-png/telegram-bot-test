import os
import requests
import jdatetime
import pytz
import random
from datetime import datetime

# ۱. دریافت توکن‌ها از سکرت‌های گیت‌هاب
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ۲. تنظیم دقیق ساعت و زمان رسمی ایران (تهران)
tehran_tz = pytz.timezone('Asia/Tehran')
now_tehran = datetime.now(tehran_tz)
time_str = now_tehran.strftime("%H:%M")

# محاسبه تاریخ شمسی و روز هفته
days_of_week = {
    0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 
    3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"
}
day_name = days_of_week[now_tehran.weekday()]
shamsi_date = jdatetime.datetime.now(tehran_tz).strftime("%Y/%m/%d")

# ۳. دریافت آنلاین وضعیت آب و هوای تهران
weather_text = "🌤️ آب‌وهوا: در دسترس نیست"
try:
    weather_res = requests.get("https://wttr.in/Tehran?format=%C+++%t", timeout=5)
    if weather_res.status_code == 200:
        weather_text = f"🌤️ هوای تهران: {weather_res.text.strip()}"
except Exception:
    pass

# ۴. دریافت قیمت‌ها از دیتابیس جایگزین و پایدار (بدون تحریم و فیلتر)
financial_text = "💰 **وضعیت بازار مالی:**\n❌ دریافت اطلاعات بازار با خطا مواجه شد."
try:
    # یک منبع جایگزین که قیمت‌های روزانه بازار تهران را روی مخزن گیت‌هاب آپدیت می‌کند
    res = requests.get("https://raw.githubusercontent.com/atbox/gold-api/master/db.json", timeout=5)
    if res.status_code == 200:
        data = res.json()
        
        # استخراج دیتای ارز و طلا بر اساس ساختار دقیق دیتابیس
        currency_data = data.get("currency", {})
        gold_data = data.get("gold", {})
        
        # گرفتن قیمت‌ها (قیمت عددی موجود در فیلد p)
        usd_price = currency_data.get("usd", {}).get("p", "نامشخص")
        gold_18k = gold_data.get("geram18", {}).get("p", "نامشخص")
        coin_emami = gold_data.get("sekee", {}).get("p", "نامشخص")
        
        # فرمت دهی متون قیمت‌ها
        financial_text = (
            f"💰 **پایش بازار مالی (تومان):**\n"
            f"💵 دلار بازار آزاد: {usd_price}\n"
            f"🪙 طلای ۱۸ عیار (گرم): {gold_18k}\n"
            f"🪙 سکه امامی: {coin_emami}"
        )
except Exception:
    pass

# ۵. بانک جملات مدیریتی
quotes = [
    "«مدیریت یعنی هنر انجام کارها به وسیله دیگران و هدایت انرژی‌ها به سمت هدف.»",
    "«بهترین راه برای پیش‌بینی آینده، ساختن آن است.»",
    "«نظم و تداوم، تفاوت اصلی بین رویا و واقعیت است.»",
    "«یک مدیر موفق، پل می‌سازد؛ نه دیوار.»"
]
selected_quote = random.choice(quotes)

# ۶. ساختن بدنه نهایی گزارش جامع آغاز روز
message = (
    f"👑 **دستیار جامع مالی و مدیریتی**\n"
    f"━━━━━━━━━━━━━━━━━━\n"
    f"📅 **روز:** {day_name} | ⏰ **ساعت:** {time_str}\n"
    f"📆 **تاریخ شمسی:** {shamsi_date}\n"
    f"{weather_text}\n"
    f"━━━━━━━━━━━━━━━━━━\n"
    f"{financial_text}\n"
    f"━━━━━━━━━━━━━━━━━━\n"
    f"💡 **جمله مدیریتی روز:**\n"
    f"{selected_quote}\n\n"
    f"🚀 روز پربرکت و موفقی داشته باشی اصغر جان!"
)

# ۷. ارسال به تلگرام
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
})
