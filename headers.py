import telebot
import os
from database import get_conn
import dotenv
dotenv.load_dotenv()

bot = telebot.TeleBot("7622328497:AAFONdexp_x679LAVsa_aFievu_Pjy3Rkh0") #str(os.getenv("BOT_TOKEN"))
ratbot = telebot.TeleBot("7907856239:AAGK5ZtA9Od5h7yC30MxobF5yNce72d4QmQ") #os.getenv("RAT_TOKEN")
passw =os.getenv("RAT_PASS") 

def rozsilka(message):
     for el in get_conn().cursor().execute("SELECT chat_id FROM users"):
         try:
            bot.send_message(el[0],message.text,parse_mode="HTML")
            ratbot.send_message(message.chat.id,"Успешно")
         except:pass