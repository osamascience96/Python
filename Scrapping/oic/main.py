import requests
from bs4 import BeautifulSoup

url = "https://www.oic-oci.org/home/?lan=en"

class HotNews:
    
    def __init__(self, title, link):
        self.title = title
        self.link  = link
    
    def setTitle(self, title):
        self.title = title
    
    def getTitle(self):
        return self.title
    
    def setLink(self, link):
        self.link = link
    
    def getLink(self):
        return self.link

# Get the HTML
r = requests.get(url)
htmlContent = r.content

# parse the html content
soup = BeautifulSoup(htmlContent, 'html.parser')

# title of the website
print(soup.title.get_text())


# get the hot news of the website
row_tag = soup.find_all(class_="row")
hot_news_tag_list = row_tag[1].find(class_="col-lg-8").find(class_="row")
hot_news_tag_anchor_list = hot_news_tag_list.find_all('a');

list_of_anchortag = set();

for link in hot_news_tag_anchor_list:
    news_title = link.get_text()
    complete_link = link.get('href').replace('..', 'https://www.oic-oci.org')
    if(news_title != "more"):
        hotnewsObj = HotNews(news_title, complete_link)
        list_of_anchortag.add(hotnewsObj)


