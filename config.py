from sqlalchemy import URL
from telebot import TeleBot, StateMemoryStorage

TG_TOKEN = ''
state_storage = StateMemoryStorage()
bot = TeleBot(TG_TOKEN, state_storage=state_storage)

# Параметры БД

db_connection = "dbname=english_bot_db user=postgres password=12345"
DSN = URL.create(
     "postgresql",
     username="postgres",
     password="12345",
     host="localhost",
     port=5432,
     database="english_bot_db",
 )
DSN = "postgresql://postgres:12345@localhost:5432/english_bot_db"