from bs4 import BeautifulSoup
import requests, os, json
from os.path import exists


url = "https://www.lululemon.fr/fr-fr/c/hommes/collections/on-en-a-trop-pour-hommes?sz=150"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'html.parser')
items = soup.find_all('div', class_="col-6 col-md-4")
print(f"found {len(items)} items")
current_items = set([' '.join(item.find("img")["alt"].replace('"', 'inch').split()) for item in items])


# current_items = set(["item3"])

if (not exists("items.json")):
    os.system('echo {"item1": "value"} > items.json')

f = open('items.json', 'r',  encoding='utf-8')
dic = json.loads(f.read())
f.close()

old_items = set(dic.keys())
# print(f"old items are: {old_items}")

new_items = current_items.difference(old_items)
if (len(new_items) > 0):
    print(f"new items are: {new_items}")


current_state = {}
for i in current_items:
    current_state[i] = "value"

with open('items.json', 'w', encoding='utf-8') as f:
    json.dump(current_state, f, ensure_ascii=False, indent=4)
