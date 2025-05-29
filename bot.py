import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram import F
from dotenv import load_dotenv
from tox import is_toxic
from aiogram.client.default import DefaultBotProperties

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')



bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


dp = Dispatcher()

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


async def main():
    await dp.start_polling(bot)

if __name__ =='__main__':
    import asyncio
    asyncio.run(main()) 