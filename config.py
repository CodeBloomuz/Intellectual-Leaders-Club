import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))
DB_PATH = "ilc_bot.db"
TEMPLATE_PATH = "Ariza_Namuna.docx"
