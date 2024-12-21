import sqlite3

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect("DataBase.db")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    return conn

# def do_sql(sql_comand,*params):
#     with get_conn() as conn:
#         cur = conn.cursor()

#         cur.execute(sql_comand,params)
    
def setup_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE if not EXISTS users(
                chat_id INTEGER ,
                tg_username TEXT ,
                city TEXT,
                UNIQUE(chat_id,tg_username)
    ) """)
    conn.commit()
    cur.execute("SELECT * FROM users")
    #print(cur.fetchall())
    conn.close()

def reg_user(message,city,rayon):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("INSERT or IGNORE INTO users VALUES(?,?,?,?)",(message.chat.id,message.from_user.username,city,rayon,))

    conn.commit()
    conn.close()

def check_us_register(message)->bool:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE chat_id = ?",(message.chat.id,))
    try:
        rez = cur.fetchone()
        if (rez):
            return True
    except:
        return False

    conn.commit()
    conn.close()

def update_city(message,city,rayon):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("UPDATE OR IGNORE users SET city = ? WHERE chat_id = ?",(city,message.chat.id,))
    cur.execute("UPDATE OR IGNORE users SET rayon = ? WHERE chat_id = ?",(rayon,message.chat.id))

    conn.commit()
    conn.close()

def get_catalog() -> list[any]:
    conn = get_conn()
    cur = conn.cursor()

    rez = cur.execute("SELECT * FROM products").fetchall()

    conn.close()
    return rez
    

def get_products(id):
    conn = get_conn()
    cur = conn.cursor()

    rez = cur.execute("SELECT * FROM products WHERE id = ?",(id,)).fetchone()

    conn.close()
    return rez

def get_cytes():
    conn = get_conn()
    cur = conn.cursor()

    _rez = cur.execute("SELECT city FROM citys").fetchall()
    rez = []
    for el in _rez:
        el = el[0]
        rez.append(el)
    conn.close()

    return rez

def get_rayons(city):
    conn = get_conn()
    cur = conn.cursor()
    rez = []
    for ra in cur.execute("SELECT rayons FROM citys WHERE city = ?",(city,)).fetchone()[0].split(","):
        rez.append(ra)
    conn.close()
    return rez

def get_cards():
    conn = get_conn()
    cur = conn.cursor()
    rez = cur.execute("SELECT * FROM cards").fetchall()
    conn.close()
    return rez

def get_users():
    conn = get_conn()
    cur = conn.cursor()

    rez = cur.execute("SELECT * FROM users").fetchall()

    conn.close()

    return rez

def write_card(card,author):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("INSERT INTO cards (card,author)VALUES(?,?)",(card,author,))
    conn.commit()

    conn.close()
    
def delete_card(id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM cards WHERE id = ?",(id,))
    conn.commit()

    conn.close()

def get_user_wid(id):
    conn = get_conn()
    cur = conn.cursor()

    rez = cur.execute("SELECT * FROM users WHERE chat_id = ?",(id,)).fetchone()

    conn.close()
    return rez
def delete_user_wid(id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE chat_id = ?",(id,))
    conn.commit()

    conn.close()