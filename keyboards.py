from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

INTERESTS = [
    "🔬 Ilmiy-tadqiqot",
    "💡 Innovatsion va startap",
    "🧠 Intellektual va madaniy-ma'rifiy",
    "📢 Axborot va targ'ibot",
]


def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📝 Ariza topshirish")]],
        resize_keyboard=True
    )


def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )


def interests_kb():
    buttons = [[KeyboardButton(text=i)] for i in INTERESTS]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def confirm_app_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_app")],
        [InlineKeyboardButton(text="✏️ Tahrirlash", callback_data="edit_app")],
        [InlineKeyboardButton(text="❌ Rad etish", callback_data="cancel_app")],
    ])


def edit_fields_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 To'liq ism", callback_data="edit_full_name")],
        [InlineKeyboardButton(text="🏫 Fakultet", callback_data="edit_fakultet")],
        [InlineKeyboardButton(text="📚 Yo'nalish", callback_data="edit_yonalish")],
        [InlineKeyboardButton(text="👥 Guruh", callback_data="edit_guruh")],
        [InlineKeyboardButton(text="📞 Telefon", callback_data="edit_phone")],
        [InlineKeyboardButton(text="💬 Motivatsiya", callback_data="edit_motivation")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_preview")],
    ])


def admin_app_kb(telegram_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Qabul", callback_data=f"accept_{telegram_id}"),
         InlineKeyboardButton(text="⏳ Sinov", callback_data=f"probation_{telegram_id}"),
         InlineKeyboardButton(text="❌ Rad", callback_data=f"reject_{telegram_id}")],
    ])


def interview_response_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Kelaman", callback_data="interview_yes")],
        [InlineKeyboardButton(text="❌ Kela olmayman", callback_data="interview_no")],
    ])


def interview_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha, yuborish", callback_data="send_interview")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_interview")],
    ])


def broadcast_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha, yuborish", callback_data="send_broadcast")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_broadcast")],
    ])


def admin_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Arizalar ro'yxati"), KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="📅 Suhbat belgilash"), KeyboardButton(text="📤 Excel eksport")],
            [KeyboardButton(text="📢 Broadcast")],
        ],
        resize_keyboard=True
    )
