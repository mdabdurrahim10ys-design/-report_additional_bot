
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CopyTextButton
)

TZ = ZoneInfo("Asia/Dhaka")

# প্রকৃত নিয়মভঙ্গের ক্ষেত্রে ব্যবহারযোগ্য নিরপেক্ষ টেমপ্লেট
ADDITIONAL_DATA = {
    "facebook": {
        "all": [
            "Hello, I believe this content may violate Facebook's Community Standards. Please review the specific content and take appropriate action if a violation is confirmed.",
            "Please review this Facebook account or content. I have a genuine concern that it may violate the platform's rules. Thank you.",
            "I am reporting this content because of a possible policy violation. Please independently review the evidence before taking action."
        ],
        "mail": [
            "Facebook support: https://www.facebook.com/help/",
            "Facebook reporting help: https://www.facebook.com/help/report"
        ]
    },

    "tiktok": {
        "all": [
            "Hello, please review this TikTok content for a possible violation of Community Guidelines. Thank you.",
            "I believe this account or content may violate TikTok's rules. Please review the specific evidence.",
            "Please independently review this report and take appropriate action only if a violation is confirmed."
        ],
        "mail": [
            "TikTok Help Center: https://support.tiktok.com/"
        ]
    },

    "instagram": {
        "all": [
            "Hello, I believe this Instagram content may violate Community Guidelines. Please review it.",
            "Please review this account for a possible policy violation. The report is based on a genuine concern.",
            "I request an independent review of this content and any appropriate action if a violation is confirmed."
        ],
        "mail": [
            "Instagram Help Center: https://help.instagram.com/"
        ]
    },

    "youtube": {
        "all": [
            "Hello, please review this YouTube video or channel for a possible violation of the Community Guidelines.",
            "I believe this content may violate YouTube policies. Please review the relevant content and evidence.",
            "Please investigate this specific content and take action only if a policy violation is confirmed."
        ],
        "mail": [
            "YouTube Help Center: https://support.google.com/youtube/"
        ]
    },

    "ai": {
        "all": [
            "Create an original, clean social media banner with modern typography and a professional layout.",
            "Write a clear Bengali social media caption with a friendly tone and suitable emojis.",
            "Create an original minimalist logo concept using the provided brand name."
        ],
        "mail": [
            "AI product support: ব্যবহার করা AI সেবার অফিসিয়াল Help Center দেখুন।"
        ]
    }
}


def get_daily_additional(category, kind):
    """বাংলাদেশ সময় অনুযায়ী প্রতিদিন একটি করে লেখা নির্বাচন করে।"""

    if category not in ADDITIONAL_DATA:
        return "এই ক্যাটাগরি পাওয়া যায়নি।"

    if kind not in ADDITIONAL_DATA[category]:
        return "এই অপশন পাওয়া যায়নি।"

    items = ADDITIONAL_DATA[category][kind]

    if not items:
        return "এই ক্যাটাগরিতে এখনো কোনো তথ্য যোগ করা হয়নি।"

    today = datetime.now(TZ).date()
    day_number = today.toordinal()

    index = day_number % len(items)

    return items[index]


def additional_keyboard(category, kind, content):
    """Copy এবং Back বাটন তৈরি করে।"""

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Copy",
                    copy_text=CopyTextButton(
                        text=content[:256]
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Back",
                    callback_data=f"category:{category}"
                )
            ]
        ]
    )
