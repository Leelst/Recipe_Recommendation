import pymysql
import pandas as pd
from sqlalchemy import create_engine


location = '/Users/ijeong-an/Desktop/codestates/cp1/team_data/menu.csv'
df = pd.read_csv(location)


conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='cp1', charset='utf8')

cur = conn.cursor()


engine = create_engine('mysql+mysqlconnector://root:Lja15410!@localhost/', encoding = 'utf-8')

df.to_sql('menu', schema='cp1', con = engine, if_exists='replace', index=False)