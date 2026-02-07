"""Telegram bot entry point using aiogram 3."""

import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, WebAppInfo

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://example.com")


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    """Send entry point button for the mini app."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Open VPN App", web_app=WebAppInfo(url=WEB_APP_URL))]],
        resize_keyboard=True,
    )
    await message.answer("Welcome!", reply_markup=keyboard)


async def main() -> None:
    """Run the bot."""
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is required")

    bot = Bot(BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
