import os
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command

import database as db
import keyboards as kb
from keyboards import INTERESTS
from docx_generator import generate_docx, make_familya_initial
from config import ADMIN_IDS

router = Router()
logger = logging.getLogger(__name__)


# ─── States ──────────────────────────────────────────────────────────────────

class Form(StatesGroup):
    full_name  = State()
    fakultet   = State()
    yonalish   = State()
    guruh      = State()
    phone      = State()
    interest   = State()
    motivation = State()
    confirm    = State()


class EditForm(StatesGroup):
    waiting = State()


# ─── Helpers ─────────────────────────────────────────────────────────────────

STATUS_UZ = {
    "pending":   "⏳ Ko'rib chiqilmoqda",
    "invited":   "📅 Suhbatga taklif etilgansiz",
    "accepted":  "✅ Qabul qilindingiz!",
    "rejected":  "❌ Rad etildi",
    "probation": "⏳ Sinov muddatida (1 oy)",
}


def preview_text(d: dict) -> str:
    fish = d["full_name"]
    familya_initial = make_familya_initial(fish)
    return (
        f"<i>Termiz iqtisodiyot va servis universiteti\n"
        f"rektori A.E.Absamatovga\n"
        f"{d['fakultet']}\n"
        f"{d['yonalish']} {d['guruh']}-guruh talabasi\n"
        f"{fish} tomonidan</i>\n\n"
        f"<b>ARIZA</b>\n\n"
        f"Men <b>{fish}</b> Termiz iqtisodiyot va servis "
        f"universitetida tashkil etilgan \"Intellectual Leaders Club\"ga "
        f"a'zolikka qabul qilish bo'yicha o'tkaziladigan tanlovda ishtirok "
        f"etishimga ruxsat berishingizni so'rayman.\n\n"
        f"<i>{d['guruh']}-guruh talabasi          {familya_initial}</i>"
    )


# ─── /start ──────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)

    if user:
        status = STATUS_UZ.get(user["status"], "Noma'lum")
        await message.answer(
            f"Salom, <b>{message.from_user.first_name}</b>! 👋\n\n"
            f"Sizning ariza holatingiz: {status}\n\n"
            f"Batafsil ma'lumot uchun /mystatus",
            parse_mode="HTML",
            reply_markup=kb.main_menu_kb()
        )
        return

    await message.answer(
        "🎓 <b>Intellectual Leaders Club</b>ga xush kelibsiz!\n\n"
        "Bu klub Termiz iqtisodiyot va servis universiteti talabalariga:\n\n"
        "🔬 Ilmiy tadqiqot imkoniyatlari\n"
        "💡 Innovatsion g'oyalar va startaplar\n"
        "🎯 Liderlik ko'nikmalarini rivojlantirish\n"
        "🤝 Hamkorlik va networking\n\n"
        "A'zo bo'lish uchun ariza topshiring! 👇",
        parse_mode="HTML",
        reply_markup=kb.main_menu_kb()
    )


# ─── /mystatus ───────────────────────────────────────────────────────────────

@router.message(Command("mystatus"))
async def cmd_mystatus(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("Siz hali ariza topshirgansiz. Ariza topshirish uchun /start")
        return

    status = STATUS_UZ.get(user["status"], "Noma'lum")
    await message.answer(
        f"📋 <b>Ariza holati</b>\n\n"
        f"👤 Ism: {user['full_name']}\n"
        f"🏫 Fakultet: {user['fakultet']}\n"
        f"📚 Yo'nalish: {user['yonalish']}\n"
        f"👥 Guruh: {user['guruh']}\n"
        f"🎯 Qiziqish: {user['interest']}\n\n"
        f"📌 Holat: {status}",
        parse_mode="HTML"
    )


# ─── Ariza boshlash ───────────────────────────────────────────────────────────

@router.message(F.text == "📝 Ariza topshirish")
async def start_form(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if user:
        status = STATUS_UZ.get(user["status"], "Noma'lum")
        await message.answer(
            f"Siz allaqachon ariza topshirgansiz.\n"
            f"Holat: {status}\n\n/mystatus"
        )
        return

    await state.set_state(Form.full_name)
    await message.answer(
        "📝 <b>Ariza to'ldirish boshlandi.</b>\n\n"
        "<b>1/7</b> — To'liq ismingizni kiriting (Familya Ism Otasining ismi):\n"
        "<i>Misol: Toshtemirov Dilmurod Xasanovich</i>",
        parse_mode="HTML",
        reply_markup=kb.cancel_kb()
    )


# ─── Anketa savollari ─────────────────────────────────────────────────────────

@router.message(Form.full_name)
async def get_full_name(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=kb.main_menu_kb())
        return
    await state.update_data(full_name=message.text.strip())
    await state.set_state(Form.fakultet)
    await message.answer(
        "<b>2/7</b> — Fakultetingizni kiriting:\n"
        "<i>Misol: Iqtisodiyot va axborot texnologiyalari fakulteti</i>",
        parse_mode="HTML"
    )


@router.message(Form.fakultet)
async def get_fakultet(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=kb.main_menu_kb())
        return
    await state.update_data(fakultet=message.text.strip())
    await state.set_state(Form.yonalish)
    await message.answer(
        "<b>3/7</b> — Ta'lim yo'nalishingizni kiriting:\n"
        "<i>Misol: Iqtisodiyot</i>",
        parse_mode="HTML"
    )


@router.message(Form.yonalish)
async def get_yonalish(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=kb.main_menu_kb())
        return
    await state.update_data(yonalish=message.text.strip())
    await state.set_state(Form.guruh)
    await message.answer(
        "<b>4/7</b> — Guruhingizni kiriting:\n"
        "<i>Misol: IQT-4-23</i>",
        parse_mode="HTML"
    )


@router.message(Form.guruh)
async def get_guruh(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=kb.main_menu_kb())
        return
    await state.update_data(guruh=message.text.strip())
    await state.set_state(Form.phone)
    await message.answer(
        "<b>5/7</b> — Telefon raqamingizni kiriting:\n"
        "<i>Misol: +998901234567</i>",
        parse_mode="HTML"
    )


@router.message(Form.phone)
async def get_phone(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=kb.main_menu_kb())
        return
    await state.update_data(phone=message.text.strip())
    await state.set_state(Form.interest)
    await message.answer(
        "<b>6/7</b> — Qaysi yo'nalishga eng ko'p qiziqasiz?",
        parse_mode="HTML",
        reply_markup=kb.interests_kb()
    )


@router.message(Form.interest)
async def get_interest(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=kb.main_menu_kb())
        return
    if message.text not in INTERESTS:
        await message.answer("Iltimos, quyidagi tugmalardan birini tanlang! 👇")
        return
    await state.update_data(interest=message.text)
    await state.set_state(Form.motivation)
    await message.answer(
        "<b>7/7</b> — Motivatsiya xatingizni yozing:\n\n"
        "<i>Nima uchun bu klubga qo'shilmoqchisiz?\n"
        "Klub orqali nimaga erishmoqchisiz?</i>",
        parse_mode="HTML",
        reply_markup=kb.cancel_kb()
    )


@router.message(Form.motivation)
async def get_motivation(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=kb.main_menu_kb())
        return
    await state.update_data(motivation=message.text.strip())
    data = await state.get_data()
    await state.set_state(Form.confirm)
    await message.answer(
        f"📄 <b>Ariza ko'rinishi:</b>\n\n{preview_text(data)}\n\n"
        "Arizani tasdiqlaysizmi?",
        parse_mode="HTML",
        reply_markup=kb.confirm_app_kb()
    )


# ─── Tasdiqlash / Tahrirlash / Rad etish ─────────────────────────────────────

@router.callback_query(F.data == "confirm_app")
async def confirm_app(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    fish = data["full_name"]
    familya_initial = make_familya_initial(fish)

    # DB ga saqlash
    await db.add_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username or "",
        full_name=fish,
        fakultet=data["fakultet"],
        yonalish=data["yonalish"],
        guruh=data["guruh"],
        phone=data["phone"],
        interest=data["interest"],
        motivation=data["motivation"],
    )

    # .docx generatsiya
    docx_path = generate_docx(data, familya_initial)

    await callback.message.answer(
        "✅ <b>Arizangiz muvaffaqiyatli yuborildi!</b>\n\n"
        "Natija haqida xabar beramiz.\n"
        "Ariza holatingizni kuzatish: /mystatus",
        parse_mode="HTML",
        reply_markup=kb.main_menu_kb()
    )

    # Foydalanuvchiga .docx yuborish
    await callback.message.answer_document(
        FSInputFile(docx_path),
        caption="📄 Sizning rasmiy arizangiz — imzolab saqlang."
    )

    # Adminga xabar + .docx
    admin_text = (
        f"🆕 <b>Yangi ariza!</b>\n\n"
        f"👤 Ism: {fish}\n"
        f"🏫 Fakultet: {data['fakultet']}\n"
        f"📚 Yo'nalish: {data['yonalish']}\n"
        f"👥 Guruh: {data['guruh']}\n"
        f"📞 Tel: {data['phone']}\n"
        f"🎯 Qiziqish: {data['interest']}\n"
        f"💬 Motivatsiya: {data['motivation']}\n\n"
        f"🆔 <code>{callback.from_user.id}</code>"
    )

    for admin_id in ADMIN_IDS:
        try:
            await callback.bot.send_message(
                admin_id, admin_text,
                parse_mode="HTML",
                reply_markup=kb.admin_app_kb(callback.from_user.id)
            )
            await callback.bot.send_document(
                admin_id,
                FSInputFile(docx_path),
                caption=f"📄 {fish} — ariza fayli"
            )
        except Exception as e:
            logger.warning(f"Admin {admin_id} ga yuborishda xato: {e}")

    os.remove(docx_path)
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "edit_app")
async def edit_app(callback: CallbackQuery):
    await callback.message.answer(
        "Qaysi ma'lumotni o'zgartirmoqchisiz?",
        reply_markup=kb.edit_fields_kb()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("edit_"))
async def edit_field(callback: CallbackQuery, state: FSMContext):
    field_map = {
        "edit_full_name":  ("full_name",  "To'liq ism (F.I.Sh.)"),
        "edit_fakultet":   ("fakultet",   "Fakultet"),
        "edit_yonalish":   ("yonalish",   "Ta'lim yo'nalishi"),
        "edit_guruh":      ("guruh",       "Guruh"),
        "edit_phone":      ("phone",       "Telefon raqam"),
        "edit_motivation": ("motivation",  "Motivatsiya xati"),
    }
    if callback.data not in field_map:
        return
    field, label = field_map[callback.data]
    await state.update_data(editing_field=field)
    await state.set_state(EditForm.waiting)
    await callback.message.answer(
        f"✏️ Yangi <b>{label}</b>ni kiriting:",
        parse_mode="HTML",
        reply_markup=kb.cancel_kb()
    )
    await callback.answer()


@router.message(EditForm.waiting)
async def save_edit(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.set_state(Form.confirm)
        data = await state.get_data()
        await message.answer(
            f"📄 <b>Ariza ko'rinishi:</b>\n\n{preview_text(data)}\n\n"
            "Arizani tasdiqlaysizmi?",
            parse_mode="HTML",
            reply_markup=kb.confirm_app_kb()
        )
        return

    data = await state.get_data()
    field = data.get("editing_field")
    await state.update_data(**{field: message.text.strip()})
    await state.set_state(Form.confirm)
    data = await state.get_data()
    await message.answer(
        f"✅ O'zgartirildi!\n\n📄 <b>Ariza ko'rinishi:</b>\n\n{preview_text(data)}\n\n"
        "Arizani tasdiqlaysizmi?",
        parse_mode="HTML",
        reply_markup=kb.confirm_app_kb()
    )


@router.callback_query(F.data == "back_preview")
async def back_preview(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(
        f"📄 <b>Ariza ko'rinishi:</b>\n\n{preview_text(data)}\n\n"
        "Arizani tasdiqlaysizmi?",
        parse_mode="HTML",
        reply_markup=kb.confirm_app_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "cancel_app")
async def cancel_app(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Ariza bekor qilindi.", reply_markup=kb.main_menu_kb())
    await callback.answer()


# ─── Suhbat javobi ───────────────────────────────────────────────────────────

@router.callback_query(F.data == "interview_yes")
async def interview_yes(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    name = user["full_name"] if user else callback.from_user.first_name
    for admin_id in ADMIN_IDS:
        try:
            await callback.bot.send_message(
                admin_id,
                f"✅ <b>{name}</b> suhbatga kelishini tasdiqladi!",
                parse_mode="HTML"
            )
        except Exception:
            pass
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("✅ Javobingiz qabul qilindi!", show_alert=True)


@router.callback_query(F.data == "interview_no")
async def interview_no(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    name = user["full_name"] if user else callback.from_user.first_name
    phone = user["phone"] if user else "—"
    for admin_id in ADMIN_IDS:
        try:
            await callback.bot.send_message(
                admin_id,
                f"❌ <b>{name}</b> suhbatga kela olmasligini bildirdi.\n"
                f"📞 Tel: {phone}",
                parse_mode="HTML"
            )
        except Exception:
            pass
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Javobingiz qabul qilindi.", show_alert=True)
