import pymysql
import pandas as pd
from sqlalchemy import create_engine
## pymysql과 sqlalchemy 모두 불러와야하느냐?
## => yes / 이뉴는 아래 create)engine을 보면 mysql을 사용하는데 그때 connect과정이 필요하기 때문

conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='cp1', charset='utf8')

cur = conn.cursor()

# cur.execute("""create table if not exists cp1.ingred_inline(
#     id int,
#     menu varchar(30),
#     ingred varchar(10),
#     num float,
#     unit varchar(10)
# );""")

engine = create_engine('mysql+mysqlconnector://root:Lja15410!@localhost/', encoding = 'utf-8')

df = pd.read_csv('/Users/ijeong-an/Desktop/codestates/cp1/team_data/ingred_inline.csv')

df.to_sql('ingred_inline', schema ='cp1', con = engine, if_exists='replace', index=False)