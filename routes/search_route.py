# search_route.py
from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask import Blueprint
import requests
from bs4 import BeautifulSoup
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
    ingredients = ingredients.strip()
    
    if dislike != " ":
        dislike = dislike.strip()

    cur.execute(f"INSERT INTO user_search VALUES ('{ingredients}', {price}, '{how}', '{category}', '{difficulty}', '{time}', '{dislike}');")
    
    conn.commit()

    # sql 쿼리문을 작성하여 fetch
    # conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='football', charset='utf8')
    # cur = conn.cursor()

    # cur.execute(f"""
    # INSERT INTO search_data VALUES ()
    # """)

    ##################################################################################################
    if dislike != " ": # 싫어요 항목이 없을 경우
        cur.execute(f"""
        SELECT menu.name, menu.id
        FROM menu
        INNER JOIN (
        SELECT *
        FROM menu
        WHERE menu.id IN ( 
            SELECT ingred_inline.id
            FROM ingred_inline 
            WHERE ingred_inline.ingred LIKE '{ingredients}') AND
            menu.id NOT IN ( 
            SELECT ingred_inline.id
            FROM ingred_inline 
            WHERE ingred_inline.ingred LIKE '{dislike}'))AS CC
        ON menu.id = CC.id 
        WHERE menu.how = '{how}' AND menu.category = '{category}' AND menu.difficulty = '{difficulty}' AND menu.time = '{time}' AND menu.price <= '{price}'
        ORDER BY menu.view DESC
        LIMIT 10;
        """)

        

    else: # 싫어요 항목이 있을 경우
        cur.execute(f"""
        SELECT menu.name, menu.id
        FROM menu 
        INNER JOIN (
        SELECT *
        FROM menu
        WHERE menu.id IN ( 
            SELECT ingred_inline.id
            FROM ingred_inline 
            WHERE ingred_inline.ingred LIKE '{ingredients}'))AS CC
        ON menu.id = CC.id 
        WHERE menu.how = '{how}' AND menu.category = '{category}' AND menu.difficulty = '{difficulty}' AND menu.time = '{time}' AND menu.price <= '{price}'
        ORDER BY menu.view DESC
        LIMIT 10;
        """)

    
    query = cur.fetchall()
    res = ""
    if len(query) == 0:
        res = "검색 결과가 없습니다."   
    ##################################################################################################
    
    
    for_cos_id = []
    image_urls = []
    cosine_urls = []
   
    for i in query: # query : [menu.name, menu.id]
        id_ = i[1]
        for_cos_id.append(id_)

        cur.execute(f"""
        SELECT cosine.1, cosine.2, cosine.3, cosine.4, cosine.5
        FROM cosine
        WHERE id = {id_};
        """)

        cosine = cur.fetchall()

        # 검색된 요리 이미지 찾기
        url = f'https://www.10000recipe.com/recipe/{id_}'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        name = soup.find(id = "main_thumbs")
        image_url = str(name).split("src=")[1].split("/>")[0].strip('"')
        image_urls.append((image_url, id_, i[0], cosine))

        # 검색된 요리의 추천 레시피 이미지 찾기
        cos_url = f'https://www.10000recipe.com/recipe/{cosine[0][0]}'
        resp = requests.get(cos_url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        name = soup.find(id = "main_thumbs")
        cosine_image_url = str(name).split("src=")[1].split("/>")[0].strip('"')
        cosine_urls.append((cosine_image_url, cos_url))


    rc_name = []
    for i in for_cos_id: #홈에서 검색결과로 들어온 id 10개

        cur.execute(f"""
        SELECT menu.name, menu.id
        FROM menu
        WHERE menu.id = (
            SELECT cosine.1
            FROM cosine
            INNER JOIN menu
            ON menu.id = cosine.id
            WHERE cosine.id = {i});
        """)

        name_ = cur.fetchall()
        rc_name.append(name_[0])

        
        


    ### 추천시스템 쿼리문 작성 ###
    


    return render_template('search_ing.html', 
        ingredients=ingredients,
        price=price,
        how=how,
        category=category,
        difficulty=difficulty,
        time=time,
        dislike= dislike,
        result = query,
        res = res,
        image_urls = image_urls,
        cosine_urls = cosine_urls,
        rc_name = rc_name,
        enumerate = enumerate)


