from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
import random
from dotenv import load_dotenv

# Загружаем токен
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ----- Команды -----
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("Привет! Я твой расширенный бот 🤖\nНапиши /help чтобы узнать команды.")

@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    help_text = (
        "/start — Приветствие\n"
        "/help — Помощь\n"
        "/game — Угадай число\n"
        "Отправь стикер или фото — я отвечу!\n"
        "Напиши 'привет' или 'пока' — я отвечу"
    )
    await message.reply(help_text)

# ----- Простая игра: угадай число -----
game_numbers = {}  # Словарь {user_id: число}

@dp.message_handler(commands=["game"])
async def game_cmd(message: types.Message):
    number = random.randint(1, 10)
    game_numbers[message.from_user.id] = number
    await message.reply("Я загадал число от 1 до 10. Попробуй угадать!")

# ----- Обработка текстовых сообщений -----
@dp.message_handler()
async def text_handler(message: types.Message):
    text = message.text.lower()

    # Ответ на ключевые слова
    if "привет" in text:
        await message.reply("Привет! Как дела?")
        return
    elif "пока" in text:
        await message.reply("Пока! Увидимся!")
        return

    # Проверка игры
    if message.from_user.id in game_numbers:
        try:
            guess = int(text)
            answer = game_numbers[message.from_user.id]
            if guess == answer:
                await message.reply(f"🎉 Верно! Я загадал {answer}")
                del game_numbers[message.from_user.id]
            elif guess < answer:
                await message.reply("Больше!")
            else:
                await message.reply("Меньше!")
        except ValueError:
            await message.reply("Напиши число от 1 до 10")
        return

    # Эхо
    await message.reply(f"Ты написал: {message.text}")

# ----- Обработка стикеров -----
@dp.message_handler(content_types=["sticker"])
async def sticker_handler(message: types.Message):
    await message.reply("👍 Крутой стикер!")

# ----- Обработка фото -----
@dp.message_handler(content_types=["photo"])
async def photo_handler(message: types.Message):
    await message.reply("📸 Отличное фото!")

# ----- Запуск бота -----
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
