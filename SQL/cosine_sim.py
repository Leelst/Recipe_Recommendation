import pymysql
import pandas as pd
from sqlalchemy import create_engine



location = '/Users/ijeong-an/Desktop/codestates/cp1/team_data/cosine_similarity.parquet'
df = pd.read_parquet(location, engine='fastparquet')
df = df.reset_index(drop=False) # id가 인덱스로 되어있어서 컬럼으로 만들어준다.

conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='cp1', charset='utf8')

cur = conn.cursor()


engine = create_engine('mysql+mysqlconnector://root:Lja15410!@localhost/', encoding = 'utf-8')

df.to_sql('cosine', schema='cp1', con = engine, if_exists='replace', index=False)
