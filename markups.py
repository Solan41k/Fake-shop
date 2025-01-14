from telebot import types
from database import *

main_button = ["Каталог🗃","Город🏙","/start","Выберете пункт из меню⏬","Работа🥷","Поддержка👨‍💻"]
def city_markup() -> types.ReplyKeyboardMarkup:
    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    for i in get_cytes():
        markup.add(types.KeyboardButton(i))
    markup.add(types.KeyboardButton("Назад ◀"))
    return markup

def rayon_murkup(city):
    markup = types.ReplyKeyboardMarkup()
    for i in get_rayons(city):
        markup.add(types.KeyboardButton(i))
    markup.add(types.KeyboardButton("Назад ◀"))
    return markup

def main_markup():
    markupmain = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markupmain.add(types.KeyboardButton("Выберете пункт из меню⏬"))
    for i in ["Каталог🗃","Город🏙","Работа🥷","Поддержка👨‍💻"]:
        markupmain.add(types.KeyboardButton(i))
    #markupmain.add(types.KeyboardButton("Назад ◀"))
    return markupmain

def produts_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for id,name,price,unit_type,_,_ in get_catalog():
        markup.add(types.InlineKeyboardButton(f"{id}: {name} {price}₽/{unit_type}",callback_data=f"products|{id}"))
    return markup

def method_pay_markup(product_id):
    markup= types.InlineKeyboardMarkup()
    for el,met in [("Банковская карта💳","BK"),("Crypto Bot💵","CB")]: #,("Stars💫","S")
        markup.add(types.InlineKeyboardButton(el,callback_data=f"paymethod|{met}|{product_id}"))
    markup.add(types.InlineKeyboardButton("<- Назад",callback_data=f"products|{product_id}"))
    return markup


