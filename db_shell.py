import sqlite3

# Створюємо підключення один раз
conn = sqlite3.connect("DataBase.db")
conn.execute("PRAGMA foreign_keys = ON")  # Увімкнення зовнішніх ключів для поточного з'єднання
cur = conn.cursor()

while True:
    input_ = input(": ")
    if input_ == "STOP":
        break
    else:
        try:
            cur.execute(input_)
            try:
                rez = cur.fetchall()
                if rez:  # Якщо є результат запиту
                    for el in rez:
                        print(el)
            except:
                pass
            conn.commit()  # Зберігаємо зміни
        except Exception as e:
            print(f"Error: {e}")

# Закриваємо підключення після завершення
conn.close()
