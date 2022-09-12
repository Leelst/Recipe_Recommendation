from flask import render_template, request
from flask import Blueprint
import pymysql
import datetime
from models.ml1 import get_level


bp = Blueprint('regist_recipe', __name__, url_prefix='/regist_recipe')


@bp.route('/', methods=['GET','POST'] )
def regis_recipe():
    return render_template("regist_recipe.html")


number = 1556056
@bp.route('/commit', methods=['GET','POST'])
def commit_recipe():
    name = request.form['menu_name'] #메뉴이름
    ingred_list = {}
    for i in range(1,11):
        #재료입력란이 공백인지 확인 후 {'달걀' : ('1','개')} 형태로 저장
        if request.form[f'ingred{i}']:
            ingred_list[request.form[f'ingred{i}']] = (request.form[f'ingred{i}_unit'], request.form[f'ingred{i}_unittype'])
        else:
            pass
        # 방법,상황,식품군,종류,인분,조리시간,해당 월
    #등록 당월
    month = str(datetime.datetime.now().month)
    if len(month) == 1:
        month = '0' + month + '월'
    else:
        month = month + '월'
    #모델링에 필요한 컬럼 리스트 생성
    # 방법,상황,식품군,종류,인분,조리시간,해당 월
    model = ['method','concept','class1','class','count','time']
    column = []
    for cat in model:
        column.append(request.form[cat])
    column.append(month)

    level = get_level(column)

    global number
    number += 1
    print("여기까지 나오나")
    print(ingred_list.values())

    ###
    conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='cp1', charset='utf8')
    cur = conn.cursor()

    cur.execute(f'''
    INSERT INTO new_info VALUES ('{number}','{column[0]}','{column[1]}','{column[2]}','{column[3]}','{column[4]}','{column[5]}');
    ''')

   

    for i in range(len(ingred_list)):
        cur.execute(f"""
        INESERT INTO new_recipe VALUES ('{number}', '{name}', '{ingred_list.keys()[i]}', '{ingred_list[ingred_list.keys()[i][0]]}', '{ingred_list[ingred_list.keys()[i][1]]}');
        """)

    conn.commit()

    return render_template("commit_recipe.html", name=name, ingred_list=ingred_list, col = column, level=level)