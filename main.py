import os
import requests
import jdatetime
import pytz
import random
from datetime import datetime

# ---------------------------------------------------------
# بخش اول: تنظیم زمان و تاریخ (حساب و کتاب تقویم)
# ---------------------------------------------------------
# ساعت سرور گیت‌هاب را به وقت آسیا/تهران تغییر می‌دهیم
tehran_tz = pytz.timezone('Asia/Tehran')
now_tehran = datetime.now(tehran_tz)
time_str = now_tehran.strftime("%H:%M") # استخراج ساعت و دقیقه

# نام روزهای هفته را به فارسی جفت می‌کنیم
days_of_week = {0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه", 5: "شنبه", 6: "یکشنبه"}
day_name = days_of_week[now_tehran.weekday()]

# تاریخ میلادی سرور را به شمسی تبدیل می‌کنیم
shamsi_date = jdatetime.datetime.now(tehran_tz).strftime("%Y/%m/%d")

# ---------------------------------------------------------
# بخش دوم: گرفتن اطلاعات آنلاین آب‌و‌هوا
# ---------------------------------------------------------
weather_text = "🌤️ هوای تهران: در دسترس نیست"
try:
    # به سایت wttr وصل می‌شویم و ۵ ثانیه بیشتر منتظر نمی‌مانیم (timeout=5)
    weather_res = requests.get("https://wttr.in/Tehran?format=%C+++%t", timeout=5)
    if weather_res.status_code == 200:
        weather_text = f"🌤️ هوای تهران: {weather_res.text.strip()}"
except Exception:
    pass # اگر اینترنت قطع بود، برنامه بدون ارور دادن عبور می‌کند

# ---------------------------------------------------------
# بخش سوم: انتخاب جمله روز و ساخت بدنه پیام
# ---------------------------------------------------------
quotes = [
    "«مدیریت یعنی هنر انجام کارها به وسیله دیگران.»",
    "«بهترین راه برای پیش‌بینی آینده، ساختن آن است.»",
    "«نظم و تداوم، تفاوت اصلی بین رویا و واقعیت است.»"
]
selected_quote = random.choice(quotes) # انتخاب تصادفی یک جمله

# قالب‌بندی نهایی متن گزارش برای ارسال
message = (
    f"👑 **دستیار جامع مدیریتی**\n"
    f"━━━━━━━━━━━━━━━━━━\n"
    f"📅 **روز:** {day_name} | ⏰ **ساعت:** {time_str}\n"
    f"📆 **تاریخ شمسی:** {shamsi_date}\n"
    f"{weather_text}\n"
    f"━━━━━━━━━━━━━━━━━━\n"
    f"💡 **جمله مدیریتی روز:**\n"
    f"{selected_quote}\n\n"
    f"🚀 روز پربرکت و موفقی داشته باشی اصغر جان!"
)

# ---------------------------------------------------------
# بخش چهارم: شلیک اطلاعات به تلگرام و بله
# ---------------------------------------------------------
# ۱. ارسال به تلگرام (با استفاده از سکرت‌هایی که قبلاً ساختی)
TELEGRAM_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID")

if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
    tele_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(tele_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})

# ۲. ارسال به بله (به آدرس سرور بله دقت کن؛ دقیقاً مثل تلگرام است!)
# برای تست سریع، می‌توانی توکن و چت‌آیدی بله را مستقیم درون کوتیشن بگذاری
BALE_TOKEN = "200848722:ci15Oxn3JuizYjY75fLcQrhXBT1KFm-2akU"
BALE_CHAT_ID = "1779961872"

if BALE_TOKEN and BALE_CHAT_ID !="200848722:ci15Oxn3JuizYjY75fLcQrhXBT1KFm-2akU":
    bale_url = f"https://api.bale.ai/bot{BALE_TOKEN}/sendMessage"
    requests.post(bale_url, data={"chat_id": BALE_CHAT_ID, "text": message})
