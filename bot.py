
import os
import asyncio
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@rahimpathanx"
CHANNEL_LINK = "https://t.me/rahimpathanx"
TZ = ZoneInfo("Asia/Dhaka")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
router = Router()
dp.include_router(router)

CATEGORIES = {
    "facebook": "📘 Facebook",
    "tiktok": "🎵 TikTok",
    "instagram": "📸 Instagram",
    "youtube": "▶️ YouTube",
    "ai": "🤖 AI Prompt"
}

def main_menu():
    buttons = []
    for key, name in CATEGORIES.items():
        buttons.append([
            InlineKeyboardButton(
                text=name,
                callback_data=f"category:{key}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def category_menu(category):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📚 All Report Additional",
            callback_data=f"all:{category}"
        )],
        [InlineKeyboardButton(
            text="📧 Mail Address",
            callback_data=f"mail:{category}"
        )],
        [InlineKeyboardButton(
            text="⬅️ Back",
            callback_data="home"
        )]
    ])

def join_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📢 Join Channel",
            url=CHANNEL_LINK
        )],
        [InlineKeyboardButton(
            text="✅ Joined",
            callback_data="check_join"
        )]
    ])

async def is_joined(user_id):
    try:
        member = await bot.get_chat_member(
            CHANNEL, user_id
        )
        return member.status in (
            "member", "administrator", "creator"
        )
    except Exception:
        return False

async def profile_card(user):
    now = datetime.now(TZ)
    hour = now.hour

    if 5 <= hour < 12:
        greeting = "☀️ শুভ সকাল"
    elif 12 <= hour < 17:
        greeting = "🌤️ শুভ দুপুর"
    elif 17 <= hour < 20:
        greeting = "🌇 শুভ সন্ধ্যা"
    else:
        greeting = "🌙 শুভ রাত্রি"

    username = (
        f"@{user.username}"
        if user.username else "Username নেই"
    )

    caption = (
        f"{greeting}\n\n"
        f"👤 <b>Username:</b> {username}\n"
        f"🆔 <b>Chat ID:</b> <code>{user.id}</code>\n\n"
        f"🕒 <b>সময়:</b> {now.strftime('%I:%M:%S %p')}\n"
        f"📅 <b>তারিখ:</b> {now.strftime('%d-%m-%Y')}\n\n"
        "✨ Welcome to REPORT ADDITIONAL"
    )

    photos = await bot.get_user_profile_photos(
        user.id, limit=1
    )

    if photos.total_count:
        photo_id = photos.photos[0][-1].file_id
        await bot.send_photo(
            user.id,
            photo_id,
            caption=caption,
            reply_markup=main_menu()
        )
    else:
        await bot.send_message(
            user.id,
            caption,
            reply_markup=main_menu()
        )

@router.message(CommandStart())
async def start(message: Message):
    if not await is_joined(message.from_user.id):
        await message.answer(
            "👋 REPORT ADDITIONAL-এ স্বাগতম!\n\n"
            "বট ব্যবহার করতে আগে আমাদের চ্যানেলে Join করুন।",
            reply_markup=join_menu()
        )
        return

    await profile_card(message.from_user)

@router.callback_query(F.data == "check_join")
async def check_join(callback: CallbackQuery):
    if not await is_joined(callback.from_user.id):
        await callback.answer(
            "❌ আগে চ্যানেলে Join করুন!",
            show_alert=True
        )
        return

    await callback.message.delete()
    await profile_card(callback.from_user)
    await callback.answer("Welcome!")

@router.callback_query(F.data == "home")
async def home(callback: CallbackQuery):
    if not await is_joined(callback.from_user.id):
        await callback.message.answer(
            "আগে চ্যানেলে Join করুন।",
            reply_markup=join_menu()
        )
        await callback.answer()
        return

    await callback.message.delete()
    await profile_card(callback.from_user)
    await callback.answer()

@router.callback_query(F.data.startswith("category:"))
async def category(callback: CallbackQuery):
    if not await is_joined(callback.from_user.id):
        await callback.answer(
            "আগে চ্যানেলে Join করুন।",
            show_alert=True
        )
        return

    key = callback.data.split(":")[1]
    name = CATEGORIES.get(key)

    if not name:
        await callback.answer()
        return

    await callback.message.edit_text(
        f"{name}\n\nনিচের অপশন নির্বাচন করুন:",
        reply_markup=category_menu(key)
    )
    await callback.answer()

# Additional library will be connected here.
@router.callback_query(
    F.data.startswith("all:") |
    F.data.startswith("mail:")
)
async def additional_menu(callback: CallbackQuery):
    if not await is_joined(callback.from_user.id):
        await callback.answer(
            "আগে চ্যানেলে Join করুন।",
            show_alert=True
        )
        return

    await callback.answer(
        "Additional Library পরবর্তী ধাপে যুক্ত হবে।",
        show_alert=True
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
