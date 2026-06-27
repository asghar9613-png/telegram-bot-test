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
    weather_res = requests.get("https://wttr.in/Tehran?format=%C+++%t")
    if weather_res.status_code == 200:
        weather_text = f"🌤️ هوای تهران: {weather_res.text.strip()}"
except Exception:
    pass

# ۴. دریافت آنلاین قیمت طلا و ارز از API عمومی و زنده
financial_text = "💰 **وضعیت بازار مالی:**\n❌ دریافت اطلاعات بازار با خطا مواجه شد."
try:
    # متصل شدن به یک اپن‌دیتا برای قیمت ارز و طلا در ایران
    gold_res = requests.get("https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency.json")
    if gold_res.status_code == 200:
        data = gold_res.json()
        
        # استخراج قیمت‌ها از ساختار دیتای خروجی
        currency_list = data.get("currency", [])
        gold_list = data.get("gold", [])
        
        dollar_price = next((item["price"] for item in currency_list if item["name"] == "دلار"), "نامشخص")
        euro_price = next((item["price"] for item in currency_list if item["name"] == "یورو"), "نامشخص")
        gold_18k = next((item["price"] for item in gold_list if "18" in item["name"]), "نامشخص")
        
        # سه رقم سه رقم جدا کردن قیمت‌ها برای خوانایی بهتر
        f_dollar = f"{dollar_price:,} ریال" if isinstance(dollar_price, int) else dollar_price
        f_euro = f"{euro_price:,} ریال" if isinstance(euro_price, int) else euro_price
        f_gold = f"{gold_18k:,} ریال" if isinstance(gold_18k, int) else gold_18k
        
        financial_text = (
            f"💰 **پایش بازار مالی (ریال):**\n"
            f"💵 دلار بازار آزاد: {f_dollar}\n"
            f"💶 یورو: {f_euro}\n"
            f"🪙 طلای ۱۸ عیار (گرم): {f_gold}"
        )
except Exception as e:
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
response = requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
})

if response.status_code == 200:
    print("Advanced financial report sent successfully!")
else:
    print(f"Failed to send. Error: {response.text}")
