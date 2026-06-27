import os
import requests
import jdatetime
import pytz
import random
from datetime import datetime
from bs4 import BeautifulSoup

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

# ۴. استخراج آنلاین و معتبر قیمت‌ها از سایت TGJU
financial_text = "💰 **وضعیت بازار مالی:**\n❌ دریافت اطلاعات بازار با خطا مواجه شد."
try:
    # درخواست به سایت شبکه اطلاع‌رسانی طلا و ارز با هدر مرورگر برای جلوگیری از بلاک شدن
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    tgju_res = requests.get("https://www.tgju.org/", headers=headers, timeout=10)
    
    if tgju_res.status_code == 200:
        soup = BeautifulSoup(tgju_res.text, 'html.parser')
        
        # پیدا کردن قیمت‌ها از روی کلاس‌های مشخص در سایت TGJU
        dollar_span = soup.find("li", {"id": "price_dollar_id"})
        gold_span = soup.find("li", {"id": "price_geram18"})
        coin_span = soup.find("li", {"id": "price_sekee"})
        
        dollar_price = dollar_span.find("span", {"class": "value"}).text.strip() if dollar_span else "نامشخص"
        gold_price = gold_span.find("span", {"class": "value"}).text.strip() if gold_span else "نامشخص"
        coin_price = coin_span.find("span", {"class": "value"}).text.strip() if coin_span else "نامشخص"
        
        financial_text = (
            f"💰 **پایش بازار مالی (تومان - TGJU):**\n"
            f"💵 دلار بازار آزاد: {dollar_price}\n"
            f"🪙 طلای ۱۸ عیار (گرم): {gold_price}\n"
            f"🪙 سکه امامی: {coin_price}"
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
    print("TGJU financial report sent successfully!")
else:
    print(f"Failed to send. Error: {response.text}")
