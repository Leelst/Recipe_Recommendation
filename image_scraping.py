import requests
from bs4 import BeautifulSoup


url = 'https://www.10000recipe.com/recipe/6905889'

resp = requests.get(url)

soup = BeautifulSoup(resp.content, 'html.parser')

name = soup.find(id = "main_thumbs")

image_url = str(name).split("src=")[1].split("/>")[0]
print(image_url)