from bs4 import BeautifulSoup 
import pandas as pd
import requests
from tqdm import tqdm
import time
path = 'TB_RECIPE_SEARCH-220701.csv'
df = pd.read_csv(path, encoding='cp949')
#널 값 제거하고 레시피 일련번호만 추출
df = df.dropna()
rcp_ids = df['RCP_SNO'].values

def crawling(id_num):
  url = f'https://www.10000recipe.com/recipe/{id_num}'
  response = requests.get(url)
  if response.status_code == 200:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    try:
      res = soup.find('div', class_='ready_ingre3')
    except:
      return None
    try:
      ingredient_list = []
      for n in res.find_all('ul'):
        for tmp in n.find_all('li'):
          lst = []
          temp = tmp.get_text().split('\n')
          for word in temp:
            word = word.strip()
            if   word == '구매' or word =='':
              pass
            else:
              lst.append(word)
          ingredient_list.append(lst)
      return ingredient_list
    except:
      return None
  else:
    print(response.status_code)


ingredient_list = []
for i in tqdm(range(len(rcp_ids))):
  lst = crawling(rcp_ids[i])
  if lst == None:
    ingredient_list.append([])
  else:
    ingredient_list.append(lst)
data_dic = {'id' : rcp_ids,
"ingredient" : ingredient_list}
data = pd.DataFrame(data_dic)
#data.to_parquet('ingredient.parquet', index=False)
print(data)
