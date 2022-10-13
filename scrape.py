from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import json


class ScrapeArticle():
    def __init__(self, url:str=None):
        print("Initializing object")
        if not url:
            self.url = 'https://annapurnapost.com'
        else:
            self.url = url

        # creating headless chrome browser for automatic interaction with web 
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_argument('--headless')
        driver_path = "/usr/bin/chromedriver" # give your driver path here
        self.driver = webdriver.Chrome(service=Service(driver_path), options=self.options)
        print("Initialization finished")

    def search(self,keyword: str):
        url = self.url + "/search/news?query=" + keyword
        driver = self.driver
        try:
            print("wating to load all content")
            driver.get(url)

            pagesource = driver.page_source

            soup = BeautifulSoup(pagesource, 'html5lib')

            art_figs = soup.select('a.slider-news-list-item-desktop')

            # today_price = []
            next_height = 1500
            
            while len(art_figs)<=30:
                print("waiting to get 30 articles, now is:", len(art_figs))
                
                #Scroll to Bottom of Webpage
                driver.execute_script(f"window.scrollTo(0,{next_height})")

                pagesource = driver.page_source
                soup = BeautifulSoup(pagesource, 'html5lib')
                art_figs = soup.select('a.slider-news-list-item-desktop')
                next_height += 300
                    
            print("success the number of articles is:", len(art_figs))

            articles = []
            for art in art_figs:
                art_url = art['href']
                art_img_url = art.img['src']
                title = art.img['alt']
                article = {
                    'title': title,
                    'article_url': self.url + art_url,
                    'image_url': art_img_url
                }
                articles.append(article)  

            print("Writing articles in json file") 
            with open("articles.json", 'w') as f:
                json.dump(articles, f, indent=4)

            print("closing the headless chrome browser!")
            driver.close()

        except ConnectionError:
            print("No Internet access, Please check your internet connection!")
            driver.close()

        
scrape_article = ScrapeArticle()

scrape_article.search("नेपाल") # pass the argument that you want to search