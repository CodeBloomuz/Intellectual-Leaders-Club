# 🎓 Intellectual Leaders Club Bot

Termiz iqtisodiyot va servis universiteti "Intellectual Leaders Club" uchun Telegram bot.

## O'rnatish

```bash
pip install -r requirements.txt
```

## Sozlash

`.env.example` faylni `.env` ga nusxalab, to'ldiring:

```
BOT_TOKEN=BotFather dan olingan token
ADMIN_IDS=Telegram ID (vergul bilan, masalan: 123456,789012)
```

Telegram ID ni bilish uchun: @userinfobot ga `/start` yozing.

## Ishga tushirish (local)

```bash
python bot.py
```

## Railway deploy

1. GitHub'ga yuklang
2. Railway → New Project → GitHub repo tanlang
3. Environment Variables ga `BOT_TOKEN` va `ADMIN_IDS` kiriting
4. Deploy! 🚀

## Fayl tuzilmasi

```
ilc-bot/
├── bot.py               # Asosiy fayl
├── config.py            # Sozlamalar
├── database.py          # SQLite baza
├── keyboards.py         # Tugmalar
├── docx_generator.py    # Ariza .docx generatsiya
├── handlers/
│   ├── user.py          # Foydalanuvchi funksiyalari
│   └── admin.py         # Admin panel
├── Ariza_Namuna.docx    # Ariza shabloni
├── requirements.txt
└── Procfile
```

## Admin buyruqlari

- `/admin` — Admin panelni ochish

## Foydalanuvchi buyruqlari

- `/start` — Botni boshlash
- `/mystatus` — Ariza holati

## Bosqichlar

```
Ariza topshirish → Kutilmoqda → Suhbatga taklif → Qabul/Rad/Sinov muddati
```
