import discord
import requests
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=vi"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description'].capitalize()
        wind = data['wind']['speed']
        humidity = data['main']['humidity']
        return f"🌤️ Thời tiết ở **{city}**:\n- Nhiệt độ: {temp}°C\n- Trạng thái: {desc}\n- Gió: {wind} km/h\n- Độ ẩm: {humidity}%"
    else:
        return "❌ Không tìm thấy thành phố hoặc lỗi API."

@client.event
async def on_ready():
    print(f"Đã đăng nhập thành: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!weather"):
        city = message.content[len("!weather"):].strip()
        if not city:
            await message.channel.send("❗ Vui lòng nhập tên thành phố. VD: `!weather Hà Nội`")
            return
        weather = get_weather(city)
        await message.channel.send(weather)

client.run(TOKEN)
