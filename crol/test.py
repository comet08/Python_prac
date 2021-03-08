import urllib.request
from bs4 import BeautifulSoup
import json


def toJSON(dict):
    with open('result.json','w', encoding='utf-8') as file:
        json.dump(dict, file, ensure_ascii=False, indent='\t')

url = ""
soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
tags = soup.find_all('td', class_='ta_l')

#tags = tags.replace('\t','').replace('\n','')
result=[]
for i in tags:
    #print(i.find('a').get('href'))
    title = i.get_text().replace('\t','').replace('\n','')
    link = "https://www.scnu.ac.kr/" + i.find('a').get('href')
    result.append({'title' : title, 'link' : link})



