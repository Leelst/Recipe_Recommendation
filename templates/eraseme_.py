from flask import render_template, request
from flask import Blueprint
from modules.preprocessing import preprocessing, load_db
bp = Blueprint('regist_recipe', __name__, url_prefix='/regist_recipe')


@bp.route('/', methods=['GET','POST'] )
def regis_recipe():
    return render_template("regist_recipe.html")

number = 1556056
@bp.route('/commit', methods=['GET','POST'])
def commit_recipe():
    name = request.form['menu_name']
    ingred_list = {}
    for i in range(1,11):
        if request.form[f'ingred{i}']:
            ingred_list[request.form[f'ingred{i}']] = request.form[f'ingred{i}_unit'], request.form[f'ingred{i}_unittype']
        else:
            pass
    print("checkpoint")
    global number
    number += 1

    print("여기까지 잘 나옵니다.1")
    ###
    conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='cp1', charset='utf8')
    cur = conn.cursor()
    # 1556056

    print(f"{number}, {name}, {ingred_list.keys[i]}, {ingred_list[ingred_list.keys[i][0]]}, {ingred_list[ingred_list.keys[i][1]]}")

    for i in range(len(ingred_list)):
        cur.execute(f"""
        INESERT INTO new_recipe VALUES ({number}, {name}, {ingred_list.keys[i]}, {ingred_list[ingred_list.keys[i][0]]}, {ingred_list[ingred_list.keys[i][1]]});
        """)
    print("여기까지 잘 나옵니다.2")
    # cur.execute(f"""
    # INSERT INTO new_info VALUES ({})
    # """)
    

    ###
    return render_template("commit_recipe.html", name=name, ingred_list=ingred_list)