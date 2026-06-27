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

# ۴. دریافت آنلاین قیمت طلا و ارز از API فوق‌العاده پایدار و معتبر Navasan
financial_text = "💰 **وضعیت بازار مالی:**\n❌ دریافت اطلاعات بازار با خطا مواجه شد."
try:
    # یک وب‌سرویس ایرانی بسیار پایدار و بدون نیاز به دور زدن تحریم
    response_market = requests.get("https://api.navasan.tech/latest", timeout=7)
    
    if response_market.status_code == 200:
        data = response_market.json()
        
        # استخراج قیمت‌ها (قیمت‌ها در این API به تومان هستند)
        usd_data = data.get("usd", {})
        gold_data = data.get("geram18", {})
        coin_data = data.get("sekee", {})
        
        # گرفتن قیمت فروش (value)
        dollar_val = usd_data.get("value", "نامشخص")
        gold_val = gold_data.get("value", "نامشخص")
        coin_val = coin_data.get("value", "نامشخص")
        
        # فرمت‌دهی و سه رقم سه رقم جدا کردن اعداد
        f_dollar = f"{int(dollar_val):,} تومان" if str(dollar_val).isdigit() else dollar_val
        f_gold = f"{int(gold_val):,} تومان" if str(gold_val).isdigit() else gold_val
        f_coin = f"{int(coin_val):,} تومان" if str(coin_val).isdigit() else coin_val
        
        financial_text = (
            f"💰 **پایش بازار مالی (تومان):**\n"
            f"💵 دلار بازار آزاد: {f_dollar}\n"
            f"🪙 طلای ۱۸ عیار (گرم): {f_gold}\n"
            f"🪙 سکه امامی: {f_coin}"
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
requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
})
