from flask import Flask, render_template, request
import sqlite3

class User:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        

 
 
u = User()
print(u)

exit()         

connection = sqlite3.connect('magaz.db')
cursor = connection.cursor()
con = sqlite3.connect("magaz.db")
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
        con = sqlite3.connect("magaz.db")
        cursor = con.cursor()
        #Значение на кнопке
        reg_status = request.form.get('reg_status')
        #Данные
        login = request.form.get('login')
        password = request.form.get('password')
        fio = request.form.get('fio')

        if reg_status == "userregister":
            cursor.execute("INSERT INTO users (fio, login, password) VALUES (?,?,?)", (fio, login, password))
        elif reg_status == "userenter":
            pass
        con.commit()
        con.close()
    return render_template('index.html', menu = menu, chapter = "")


@app.route("/<chapter>")
def index(chapter):
    if  chapter in types:
        name = [m['name'] for m in menu if m['type'] == chapter][0] 
        return render_template('info.html', menu = menu, chapter = chapter, name = name)
    else:
        return render_template('404.html')
if __name__ == "__main__":
    app.run(debug = True)
con.close()
