# search_route.py
from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask import Blueprint
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='cp1', charset='utf8')
cur = conn.cursor()

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/',methods = ['GET','POST'])
def search():
    # home 에서 입력받은 값을 받아온다.
    ingredients = str(request.form['ingredients'])
    price = request.form['price']
    how = str(request.form['how'])
    category = str(request.form['category'])
    difficulty = str(request.form['difficulty'])
    time = str(request.form['time'])
    dislike = str(request.form['dislike'])

    print(f"'{ingredients}', {price}, '{how}', '{category}', '{difficulty}', '{time}', '{dislike}'")
    if ingredients != " ":
        ingredients = ingredients.strip()
    
    if dislike != " ":
        dislike = dislike.strip()

    if price == " ":
        price = 99999999

    cur.execute(f"INSERT INTO user_search VALUES ('{ingredients}', {price}, '{how}', '{category}', '{difficulty}', '{time}', '{dislike}');")
    
    conn.commit()

    # sql 쿼리문을 작성하여 fetch
    # conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='football', charset='utf8')
    # cur = conn.cursor()

    # cur.execute(f"""
    # INSERT INTO search_data VALUES ()
    # """)

    return render_template('search_ing.html', 
        ingredients=ingredients,
        price=price,
        how=how,
        category=category,
        difficulty=difficulty,
        time=time,
        dislike= dislike,
        enumerate=enumerate)


