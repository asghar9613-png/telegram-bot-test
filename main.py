import os
import requests
from datetime import datetime

# ۱. دریافت توکن‌ها از سکرت‌های گیت‌هاب
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ۲. دریافت آنلاین وضعیت آب و هوای تهران
weather_text = "آب‌وهوا: در دسترس نیست"
try:
    # استفاده از یک API رایگان و بدون توکن برای وضعیت فعلی هوای تهران
    weather_res = requests.get("https://wttr.in/Tehran?format=%C+++%t")
    if weather_res.status_code == 200:
        weather_text = f"🌤️ وضعیت هوای تهران: {weather_res.text.strip()}"
except Exception:
    pass

# ۳. ثبت زمان دقیق ارسال گزارش
now = datetime.now()
time_str = now.strftime("%H:%M")

# ۴. ساختن متن شیک و مدیریتی گزارش
message = (
    f"📊 **گزارش آغاز روز هوشمند**\n\n"
    f"⏰ زمان ارسال: {time_str}\n"
    f"{weather_text}\n\n"
    f"✨ **جمله روز:**\n"
    f"«موفقیت مجموعه‌ای از تلاش‌های کوچک است که هر روز تکرار می‌شوند.»\n\n"
    f"🚀 روز خوبی داشته باشی اصغر جان! سیستم آماده خدمت است."
)

# ۵. ارسال به تلگرام
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
response = requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown" # برای بولد شدن و شیک شدن متن
})

if response.status_code == 200:
    print("Report sent successfully!")
else:
    print(f"Failed to send. Error: {response.text}")
