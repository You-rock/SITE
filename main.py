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
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    fio TEXT DEFAULT "",
    login TEXT DEFAULT "",
    password TEXT DEFAULT "");
"""
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

@app.route("/exit")
def exit():
    user.set_user(name="",login="",status="")
    return redirect(request.referrer)


@app.route("/<chapter>")
def index(chapter):
    if  chapter in types:
        name = [m['name'] for m in menu if m['type'] == chapter][0] 
        return render_template('info.html', menu = menu, chapter = chapter, name = name, user = user.userdata)
    else:
        return render_template('404.html')
if __name__ == "__main__":
    app.run(debug = True)
