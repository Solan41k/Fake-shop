import telebot
import sqlite3
import dotenv
import os

from telebot import types
from database import *

dotenv.load_dotenv()
ratbot = telebot.TeleBot(os.getenv("RAT_TOKEN"))
button = ["Все пользователи","Карты","Удалить карту","Добавить карту","Искать пользователя по id","Удалить пользователя"]
passw = os.getenv("RAT_PASS")

@ratbot.message_handler(commands=["start"])
def start(message):
    print(os.getenv("RAT_PASS"))
    markup = types.ReplyKeyboardMarkup()
    for el in button:
        markup.add(types.KeyboardButton(el))
    ratbot.send_message(message.chat.id,'Выберете действие',reply_markup=markup)
    ratbot.register_next_step_handler(message,han1)

@ratbot.message_handler(func=lambda message: any(word in button for word in button))
def han1(message):
    try:
        if message.text in button:
            ratbot.send_message(message.chat.id,"Введите пароль: ")
            ratbot.register_next_step_handler(message,mainhan,message.text)
        else:
            try:ratbot.delete_message(message.chat.id,message.message_id)
            except:pass
    except Exception as e:
        ratbot.send_message(message.chat.id,str(e))

def mainhan(message,button:str):
    if message.text.strip() == passw:
        match button:
            case "Все пользователи":
                text = ''   
                try:   
                    for chat_id,tg_username,city,rayon in get_users():
                        text += f"id: {chat_id} username: @{tg_username} Город: {city} Район: {rayon}\n\n" 
                    ratbot.send_message(message.chat.id,text)
                except Exception as e:
                    if not get_users():
                        ratbot.send_message(message.chat.id,"No one users found")
                    else:
                        ratbot.send_message(message.chat.id,str(e))
            case "Карты":
                text ="<b>📎Список всех карт: </b>\n\n"
                for c_id,c,a in get_cards():
                    text += f"💳 {c_id} - <code>{c}</code>\n└🇷🇺{a}\n\n"
                ratbot.send_message(message.chat.id,text,parse_mode="HTML") 
            case "Добавить карту":
                ratbot.send_message(message.chat.id,"Введите номер карты: ")
                ratbot.register_next_step_handler(message,add_crd_input1)
            case "Удалить карту":
                ratbot.send_message(message.chat.id,"Введите номер карты: ")
                ratbot.register_next_step_handler(message,delete_card_)
            case "Искать пользователя по id":
                ratbot.send_message(message.chat.id,"Введите id пользователя: ")
                ratbot.register_next_step_handler(message,search_user)
                # chat_id,tg_username,city,rayon in searc_user()
            case "Удалить пользователя":
                ratbot.send_message(message.chat.id,"Введите id пользователя: ")
                ratbot.register_next_step_handler(message,delete_user)
    else:
        ratbot.send_message(message.chat.id,"Неправильный пароль введите ещё раз: ")
        ratbot.register_next_step_handler(message,mainhan,button)

def delete_user(message):
    try:
        int(message.text)
        delete_user_wid(message.text)
        ratbot.send_message(message.chat.id,"Успешно")
    except ValueError:
        ratbot.send_message(message.chat.id,"Вы неправильно ввели значение, введите ещё раз: ")
        ratbot.register_next_step_handler(message,search_user)
    except Exception as e:
        ratbot.send_message(message.chat.id,f"Произошла ошибка:\n\n{e}")
    

def search_user(message):
    try:
        int(message.text)
        chat_id,tg_username,city,rayon = get_user_wid(message.text)
        text = f"id: {chat_id} username: @{tg_username} Город: {city} Район: {rayon}"
        ratbot.send_message(message.chat.id,text)
    except ValueError:
        ratbot.send_message(message.chat.id,"Вы неправильно ввели значение, введите ещё раз: ")
        ratbot.register_next_step_handler(message,search_user)
    except Exception as e:
        ratbot.send_message(message.chat.id,f"Произошла ошибка:\n\n{e}")
    

def delete_card_(message):
    try:
        int(message.text)
        delete_card(message.text)
        ratbot.send_message(message.chat.id,"Успешно")
    except ValueError:
        ratbot.send_message(message.chat.id,"Вы неправильно ввели значение, введите ещё раз: ")
        ratbot.register_next_step_handler(message,delete_card_)
    except Exception as e:
        ratbot.send_message(message.chat.id,f"Произошла ошибка:\n\n{e}")
    

def add_crd_input1(message):
    try:
        n_c = int(message.text)
        ratbot.send_message(message.chat.id,"Введите владельца карты: ")
        ratbot.register_next_step_handler(message,add_crd_input2,n_c)
    except ValueError:
        ratbot.send_message(message.chat.id,"Вы неправильно ввели значение, введите ещё раз: ")
        ratbot.register_next_step_handler(message,add_crd_input1)
    except Exception as e:
        ratbot.send_message(message.chat.id,f"Произошла ошибка:\n\n{e}")
    

def add_crd_input2(message,number_card):
    try:
        write_card(number_card,message.text)
        ratbot.send_message(message.chat.id,"Успешно")
    except Exception as e:
        ratbot.send_message(message.chat.id,f"Произошла ошибка:\n\n{e}")
    

ratbot.infinity_polling()