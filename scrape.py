import requests
from bs4 import BeautifulSoup
import json

headers = {
  'authority': 'bg.annapurnapost.com',
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.5',
  'origin': 'https://annapurnapost.com',
  'referer': 'https://annapurnapost.com/',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

articles = []


def scrape_article(page_no, keyword):
    url = f"https://bg.annapurnapost.com/api/search?page={page_no}&title={keyword}"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data


def clear_data(data):
    base_url = "https://bg.annapurnapost.com"
    for item in data['data']['items']:
        title = item['title']
        img_ul = item['featuredImage']
        published_on = item['publishOn']

        # taking text only as content
        content_html = item['content']
        soup = BeautifulSoup(content_html, 'html5lib')
        content = soup.text.replace('\n', '')

        # taking catagory's name list
        catagories_dict = item['categories']
        catagories = []
        for catagory in catagories_dict:
            catagories.append(catagory['name'])
        
        article = {
            'title': title,
            'content': content,
            'img_url': base_url + img_ul,
            'published_on': published_on,
            'catagories': catagories
        }
        articles.append(article)


if __name__ == "__main__":
    page_no = 1
    while len(articles) < 30:
        try:
            data = scrape_article(page_no, "नेपाल")
            if data:
                clear_data(data)
                page_no += 1
            else:
                print("Page limit exceed!")
        except:
            print("Network error!")
            break
    
    if len(articles) >= 30:
        with open('articles.json', 'w') as f:
            # creates readable Nepali text in json file
            json.dump(articles, f, indent=4, ensure_ascii=False) 