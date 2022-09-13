from flask import Flask, render_template, request, redirect, url_for,jsonify, session
from routes import search_route, login, regist_recipe
import pymysql
import pandas as pd
import requests
from bs4 import BeautifulSoup
# conda install -c conda-forge lightgbm

app = Flask(__name__)
app.secret_key = "aklsdfjij2@lidfjalk"
app.register_blueprint(search_route.bp)
app.register_blueprint(login.bp)
app.register_blueprint(regist_recipe.bp)


ID = "hello"
PW = "world"

conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='cp1', charset='utf8')
cur = conn.cursor()

@app.route('/', methods = ['get','post'])
def index():
    return render_template("home.html")
    
@app.route('/home', methods = ['get','post'])
def home():    
    global ID, PW

    loginId = request.args.get('loginId')
    loginPw = request.args.get('loginPw')
    
    if (loginId == ID) & (loginPw == PW):
        global session
        session["userID"] = loginId
        return render_template("home_login.html", username = session["userID"])
    else:
        return render_template("home_login.html", username = session["userID"])
    
    #return render_template("home_login.html", login = True, username = session.get("userID"))
    # else:
        # return render_template("home_login.html", username = session["userID"])

    # loginId = request.args.get('loginId')
    # loginPw = request.args.get('loginPw')

    # if ID == loginId and PW == loginPw:
    #     return render_template("home_login.html", username = loginId)
    # else:
    #     return redirect(url_for('index'))



@app.route('/logout', methods = ['get','post'])
def logout():
    session.pop("userID")
    return redirect(url_for('index'))
    

@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/signin_done', methods =["get"])
def signin_done():
    email = request.args.get("email")
    uid = request.args.get("id")
    pwd = request.args.get("pwd")
    name = request.args.get("name")
    # print(email, uid, pwd, name)  # 올바르게 되고 있는지 확인하기 위해서
    if DB.singin(email, uid, pwd, name):
        return redirect(url_for("index")) # index는 함수 이름인데..? 되네..? # url_for는 함수 이름을 적어줘야되나봄
    else:
        return redirect(url_for("signin"))

@app.route('/image_test')
def image_test():
    return render_template("image_test.html")

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html", username = session["userID"])

@app.route('/regis_recipe')
def regis_recipe():
    return render_template("regis_recipe.html", username = session["userID"])

@app.route('/table')
def sauce_table():
    return render_template("table.html", username = session["userID"])

@app.route('/market', methods=['get','post'])
def market():
    return render_template("market.html", username = session["userID"])



@app.route('/total_search', methods = ['get','post'])
def total_search():
    search_word = request.form['search_word']
    cur.execute(f"""
    SELECT name, id
    FROM menu
    WHERE menu.id IN (
        SELECT id 
        FROM ingred_inline
        WHERE ingred LIKE "%{search_word}%")
    ORDER BY view DESC
    LIMIT 10;
    """)

    res = cur.fetchall()

    image_urls = []
    for i in res:
        url = f'https://www.10000recipe.com/recipe/{i[1]}'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        name = soup.find(id = "main_thumbs")
        image_url = str(name).split("src=")[1].split("/>")[0].strip('"')
        image_urls.append(image_url)


    return render_template('total_search.html', search_word=search_word, res=res, image_urls = image_urls,
    enumerate = enumerate, username = session["userID"])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001) 

