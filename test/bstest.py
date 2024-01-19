import requests
from bs4 import BeautifulSoup
import datetime

url = "https://www.dell.com/community/ja/conversations/%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8-%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3/powerstore-%E3%81%AE%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E3%83%9D%E3%83%BC%E3%83%88%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/65a8b3e2c833c24319f8a218"

response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to fetch {url}")

soup = BeautifulSoup(response.text, 'html.parser')

meta_tag = soup.find('meta', attrs={'data-react-helmet': 'true', 'name': 'description'})
content = meta_tag['content']

print(content)

p_text = soup.find('p', class_='text-overflow text text--large css-1ry1tx8 css-okc7pe').get_text(strip=True)
h1_text = soup.find('h1', class_='conversation-balloon__content__title word-wrap heading heading--h1 css-1ry1tx8 css-1pj99nl').get_text(strip=True)

print(p_text)
print(h1_text)

date_text = soup.find('p', class_='m-r-1 dell-conversation-ballon__header-date text text--normal css-1ry1tx8 css-jp8xm2').get_text(strip=True)

original_time = datetime.datetime.strptime(date_text, "%Y年%m月%d日 %H:%M")
new_time = original_time + datetime.timedelta(hours=9)
new_time = new_time.strftime('%Y-%m-%d %H:%M')

print(new_time)