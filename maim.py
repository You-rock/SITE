from flask import Flask, render_template

app=Flask(__name__)

status = "admin"
menu = [{"name":"Видеокарты", "type":"videocard"}, {"name":"Материнские платы", "type":"motherboard"},{"name":"Компьютеры в сборе", "type":"computers"}]

types = [m['type'] for m in menu]

@app.route("/")
def base():
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
