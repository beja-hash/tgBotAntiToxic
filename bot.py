import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.client.default import DefaultBotProperties

from aiohttp import web
from dotenv import load_dotenv
from tox import is_toxic

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my_secret_token")
BASE_WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")  # Автоматическая переменная Render

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer('Привет! Я проверяю сообщение на токсичность на нескольких языках')


@dp.message(F.text)
async def handle_message(message: Message):
    if is_toxic(message.text):
        await message.reply("Это сообщение считается токсичным")
        try:
            await message.delete()
        except:
            await message.reply("❗ Не могу удалить сообщение — проверь права администратора.")
    else:
        print(f'✅ Сообщение безопасное: {message.text}')


# Aiohttp Webhook Setup
async def on_startup(app):
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)


async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()


app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=int(os.getenv("PORT", 10000)))


import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    server = HTTPServer(('0.0.0.0', 10000), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()
