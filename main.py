from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
class User:
    __instance = None
    __userdata = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @property
    def userdata(cls):
        return cls.__userdata
    
    @classmethod
    def set_user(cls, **qwargs):
        cls.__userdata = qwargs

user = User()
user.set_user(name="",login="",status="")

bd_path = os.path.split(__file__)[0]+'/magaz.db'

con = sqlite3.connect(bd_path)
cursor = con.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    users_id INTEGER PRIMARY KEY,
    fio TEXT DEFAULT "",
    login TEXT DEFAULT "",
    password TEXT DEFAULT "");
'''
)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tovar(
    tovar_id INTEGER PRIMARY KEY,
    name TEXT DEFAULT "",
    category TEXT DEFAULT "",
    category_name TEXT DEFAULT "",
    price INT DEFAULT 0);
'''
)
con.commit()
con.close

app=Flask(__name__)

menu = [{"name":"Видеокарты", "type":"videocard"}, {"name":"Материнские платы", "type":"motherboard"},{"name":"Компьютеры в сборе", "type":"computers"}]

types = [m['type'] for m in menu]

@app.route("/",methods=['post', 'get'])
def base():
    if request.method == 'POST':
        con = sqlite3.connect(bd_path)
        cursor = con.cursor()
        #Значение на кнопке
        reg_status = request.form.get('reg_status')
        #Данные
        login = request.form.get('login')
        password = request.form.get('password')
        fio = request.form.get('fio')

        if reg_status == "userregister":
            cursor.execute('''SELECT COUNT(*) FROM users WHERE login = ?''', (login,))
            n = cursor.fetchone()[0]
            if n > 0: 
                user.set_user(name="",login=login, status="Такой логин уже есть!")
            else:
                cursor.execute("INSERT INTO users (fio, login, password) VALUES (?,?,?)", (fio, login, password))
                user.set_user(name=fio,login=login, status="")
        elif reg_status == "userenter":
            cursor.execute('''SELECT * FROM users WHERE login = ?''', (login,))
            users = cursor.fetchall()
            n = len(users)
            if n>0: u_password = users[0][3] 
            if n == 0: 
                user.set_user(name="",login=login, status="Не верный логин")
            elif u_password != password:
                user.set_user(name="",login="", status="Не верный пароль!")
            else:
                user.set_user(name=users[0][1],login=login, status="")
        con.commit()
        con.close()
    return render_template('index.html', menu = menu, chapter = "", user = user.userdata)

@app.route("/admin", methods=['post', 'get'])
def admin():
    ####БД####
    con = sqlite3.connect(bd_path)
    cursor = con.cursor()
    ##########
    cursor.execute("SELECT * FROM tovar")
    tovars = cursor.fetchall()

    if request.method == 'POST':
        # Получаем данные
        cursor.execute("SELECT * FROM tovar ORDER BY category")
        tovars = cursor.fetchall()

        # Смотрим, какая нажата кнопка
        btn_id = request.form.get('add_tovar_buton')
        if btn_id == "addbuton":
                name=request.form.get("name")
                price = request.form.get("price")
                category = request.form.get("category")
                category_n = [m['name'] for m in menu if m['type'] == category][0] 
                cursor.execute("INSERT INTO tovar (name, price, category,category_name) VALUES (?,?,?,?)", (name, price, category, category_n))
                # Заново читаем базу
                cursor.execute("SELECT * FROM tovar ORDER BY category")
                tovars = cursor.fetchall()
        
        
        btn_id = request.form.get('del_tovar_buton')
        if btn_id == "delbutton":
            tovar_id=request.form.get("tovar_id")
            cursor.execute("DELETE FROM tovar WHERE tovar_id=?",(tovar_id,))
            # Заново читаем базу
            cursor.execute("SELECT * FROM tovar ORDER BY category")
            tovars = cursor.fetchall()        
        con.commit()
        con.close()
    return render_template('add_tovar.html', user = user.userdata, menu = menu, tovars=tovars)

@app.route("/exit")
def exit():
    user.set_user(name="",login="",status="")
    return redirect(request.referrer)


@app.route("/<chapter>", methods=['post', 'get'])
def index(chapter):
        ####БД####
    con = sqlite3.connect(bd_path)
    cursor = con.cursor()

    # Получаем данные
    cursor.execute("SELECT * FROM tovar WHERE category = ? ORDER BY category",(chapter,))
    tovars = cursor.fetchall()
    
    con.commit()
    con.close()

    if request.method == 'POST':
                            pass
    if  chapter in types:
        name = [m['name'] for m in menu if m['type'] == chapter][0] 
        return render_template('info.html', menu = menu, chapter = chapter, name = name, user = user.userdata, tovars = tovars)
    else:
        return render_template('404.html')



if __name__ == "__main__":
    app.run(debug = True)
