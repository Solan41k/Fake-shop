import telebot
import dotenv
import os

#from aiocpa import CryptoPay
from database import *
from telebot import types
#from headers import *
from markups import *

dotenv.load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN")) #str(os.getenv("BOT_TOKEN"))
#cp = CryptoPay(os.getenv("PAY_TOKEN")) #


@bot.message_handler(commands=["start"])
def start(message):
    setup_users()
    #print(message)
    if not check_us_register(message) and not message.from_user.is_bot:
        bot.send_message(message.chat.id,"🌿",reply_markup=types.ReplyKeyboardMarkup())
        bot.send_message(message.chat.id,"Вас приветствует Cloud9, Выберете ваш город:",reply_markup=city_markup())
        bot.register_next_step_handler(message,setup_user)
        print(check_us_register(message))
    else:
        print(check_us_register(message))
        bot.send_message(message.chat.id,"🌿",reply_markup=types.ReplyKeyboardMarkup())
        bot.send_message(message.chat.id,"Вас приветствует Cloud9. Выберете пункт из меню: ",reply_markup=main_markup())
        #main(message)

def setup_user(message):
    if message.text in get_cytes():
        bot.delete_messages(message.chat.id,message_ids=[message.message_id,message.message_id-1,message.message_id-2])
        if not message.from_user.is_bot:
            bot.send_message(message.chat.id,"Выберете ваш район: ",reply_markup=rayon_murkup(message.text))
            bot.register_next_step_handler(message,setup_user1,message.text)
            #city = message.text
            
            #reg_user(message,city)
        #start(message)
    elif message.text == "/start":
        bot.delete_messages(message.chat.id,message_ids=[message.message_id,message.message_id-1,message.message_id-2])
        start(message)
    else:
        bot.delete_message(message.chat.id,message.message_id)
        bot.register_next_step_handler(message,setup_user)
    
def setup_user1(message,city):
    if not message.text in main_button:
        if message.text in get_rayons(city):
            try:
                reg_user(message,city,message.text)
                try:
                    bot.delete_messages(message.chat.id,[message.message_id,message.message_id-1])
                except:pass
            except Exception as e:
                print(e)
            start(message)
        else:
            bot.delete_message(message.chat.id,message.message_id)
            bot.register_next_step_handler(message,setup_user1)
    else:
        main_han(message)
def main(message):
    bot.send_message(message.chat.id,"Выберете пункт из меню: ",reply_markup=main_markup()) 

def update_us_city(message):
    if message.text in get_cytes():
        try:
            bot.send_message(message.chat.id,"Выберете ваш район: ",reply_markup=rayon_murkup(message.text))
            bot.register_next_step_handler(message,update_us_city1,message.text)
            
            #update_city(message,message.text)

            # bot.delete_messages(message.chat.id,message_ids=[message.message_id,message.message_id-1])
            # bot.send_message(message.chat.id,"Успешно",reply_markup=main_markup())
        except:
            bot.send_message(message.chat.id,"Что-то пошло не так",reply_markup=main_markup())
        
    elif message.text == "/start":
        start(message)
    elif message.text == "Назад ◀":
        bot.delete_message(message.chat.id,message.message_id)
        bot.delete_message(message.chat.id,message.message_id-1)
        main(message)
    else:
        bot.delete_message(message.chat.id,message.message_id)
        bot.register_next_step_handler(message,update_us_city) 

def update_us_city1(message,city):
    if message.text in get_rayons(city):
        try:
            update_city(message,city,message.text)
            bot.send_message(message.chat.id,"Успешно")
            try:
                bot.delete_messages(message.chat.id,[message.message_id,message.message_id-1,message.message_id-2,message.message_id-3])
            except Exception as e:print(e)
            main(message)
        except Exception as e:
            print(e)
            main(message)
    elif message.text == "/start":
        start(message)
    elif message.text == "Назад ◀":
        bot.delete_message(message.chat.id,message.message_id)
        bot.delete_message(message.chat.id,message.message_id-1)
        main(message)
    else:
        bot.delete_message(message.chat.id,message.message_id)
        bot.register_next_step_handler(message,update_us_city) 

@bot.message_handler(func=lambda message: not message.text in main_button)

@bot.message_handler(func=lambda message: any(word in message.text for word in main_button))
def main_han(message):
    try:
        if check_us_register(message):
            match message.text:
                case "Каталог🗃":
                    bot.send_message(message.chat.id,"🗂",reply_markup=types.ReplyKeyboardMarkup())
                    bot.send_message(message.chat.id,"Каталог товаров:",reply_markup=produts_markup())
                case "Город🏙":
                    bot.reply_to(message,"Выберете ваш город: ",reply_markup = city_markup())
                    bot.register_next_step_handler(message,update_us_city)
                case "Работа🥷":
                    bot.send_message(message.chat.id,"Мы предлагаем лучшие условия, и в любои случае не грозим расправой❤️\nПисать сюда: @")
                case"Поддержка👨‍💻":
                    bot.send_message(message.chat.id,"Аккаунт тех поддержки: @")
                case "/start":
                    start(message)
                case _:
                    bot.delete_message(message.chat.id,message.message_id)
        else:
            try:
                start(message)
            except Exception as e:
                print(e)
    except:pass

@bot.callback_query_handler(func=lambda call:call.data.startswith("products"))
def product_handler(callback):
    id = callback.data.split("|")[1]
    id,name,price,unit_type,description,_ = get_products(id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Инструкция как купить крипто-валюту",url="https://t.me/manualpokypkuwalytu"))
    markup.add(types.InlineKeyboardButton("Купить",callback_data=f"take_order|{id}"))
    markup.add(types.InlineKeyboardButton("<- Назад",callback_data=f"take_order|back"))
    bot.edit_message_text(f"<b>{name}: </b>\n <i>{description}</i>\n\n Цена: {price}₽/{unit_type}",callback.message.chat.id,callback.message.message_id,parse_mode="HTML",reply_markup=markup)

@bot.callback_query_handler(func=lambda call:call.data.startswith("take_order"))
def take_us_order(callback):
    product_id = callback.data.split("|")[1]
    if product_id == "back":
        bot.edit_message_text("Каталог товаров:",callback.message.chat.id,callback.message.message_id,reply_markup=produts_markup())
        return
    #id,name,price,unit_type,_,min_order = get_products(product_id)
    bot.edit_message_text("Выберете способ оплаты",callback.message.chat.id,callback.message.message_id,reply_markup=method_pay_markup(product_id))


@bot.callback_query_handler(func=lambda callback:callback.data.startswith("paymethod"))
def choice_paymethod(callback):
    met,product_id = callback.data.split("|")[1],callback.data.split("|")[2]
    # print(met,product_id)
    
    id,_,_,unit_type,_,min_order = get_products(product_id)
    try:
        bot.edit_message_text(f"Введите количество для покупки(в {unit_type})\n<b>Минимальное количество для покупки</b>: {min_order}{unit_type}",callback.message.chat.id,callback.message.message_id,parse_mode="HTML")
    except:
        bot.send_message(callback.message.chat.id,f"Введите количество для покупки(в {unit_type})\n<b>Минимальное количество для покупки</b>: {min_order}{unit_type}",parse_mode="HTML")
    bot.register_next_step_handler(callback.message,enter_quantity,id,min_order,met)
 
def enter_quantity(message,id,min_order,paymethod):
    #print(float(message.text))
    try:
        if not message.text in main_button:
            input_ =float(message.text)

            if not input_<min_order:
                _,_,price,_,_,min_order = get_products(id)
                match paymethod:
                    #case "CB":
                     #   try:
                      #      create_order(message,id,input_)
                       # except Exception as e:
                        #    if 'AMOUNT_TOO_BIG' in str(e):
                         #       bot.delete_message(message.chat.id,message.message_id)
                          #      bot.send_message(message.chat.id,"Слишком огромная сума, введите суму поменьше:")
                           #     bot.register_next_step_handler(message,enter_quantity,id,min_order,paymethod)
                    case "BK":
                        # print(get_cards())
                        text ="<b>📎Список всех карт: </b>\n\n"
                        for c_id,c,a in get_cards():
                            text += f"💳 {c_id} - <code>{c}</code>\n└🇷🇺{a}\n\n"
                        text +=f"\n\nСкиньте на одну из этих карт {input_ *price}₽ и пришлите в тех.поддержку👨‍💻 чек оплаты📃 \nПосле проверки оплаты товар будут направлятся к вам"
                        bot.send_message(message.chat.id,text,parse_mode="HTML")
            else:
                bot.send_message(message.chat.id,f"Минимально количество для покупки {min_order}! Введите ещё раз")
                bot.register_next_step_handler(message,enter_quantity,id,min_order,paymethod)
        else:
            main_han(message)
    
    except Exception as e:
        print(e)
        if not message.text in main_button:
            bot.delete_message(message.chat.id,message.message_id)
            bot.register_next_step_handler(message,enter_quantity,id,min_order,paymethod)

def create_order(message,product_id,quantity):
    try:
        _,name,price,unit_type,_,min_order = get_products(product_id)
        #invoice = cp.create_invoice(amount=price*quantity,currency_type="fiat",fiat="RUB",expires_in=180)#,fiat=True,description="Оплата товара",)
        #markup = types.InlineKeyboardMarkup()
        #markup.add(types.InlineKeyboardButton("Оплатить",url=invoice.pay_url))
        #markup.add(types.InlineKeyboardButton("Проверить",callback_data=f"invoice|check|{invoice.invoice_id}"))
        #markup.add(types.InlineKeyboardButton("Отменить",callback_data=f"invoice|delete|{invoice.invoice_id}"))
        #bot.send_message(message.chat.id,"Оплатите счет и в ближайшем времени свами свяжутся раскажут все подробности",reply_markup=markup)
    except Exception as e:
        print("loh")
        print(e)
            

#@bot.callback_query_handler(func=lambda call:call.data.startswith("invoice"))
#def invoice_(callback):
#   data = callback.data.split("|")
#    _,met,invoice_id = data
#    if invoice_id:
#        match met:
#            case "check":
#                invoice = cp.get_invoices(invoice_ids=[invoice_id])[0]
#                match invoice.status:
#                    case "active":
#                        bot.send_message(callback.message.chat.id,"Вы ещё не оплатили!")
#                    case "paid":
#                        bot.edit_message_text("Вы успешно оплатили в ближайшем времени с вами свяжутся",callback.message.chat.id,callback.message.message_id)
#                    case _:
#                        bot.edit_message_text("Счет не найден или удален",callback.message.chat.id,callback.message.message_id)
#            case "delete":
#                try:
#                    cp.delete_invoice(invoice_id)
#                    bot.edit_message_text("Отменено",callback.message.chat.id,callback.message.message_id)
#                except:
#                    bot.send_message(callback.message.chat.id,"Произошла ошибка")
#                    bot.delete_message(callback.message.chat.id,callback.message.message_id)
 #   else:
 #       bot.edit_message_text("Счет не найден или удален",callback.message.chat.id,callback.message.message_id)
        

bot.infinity_polling()
