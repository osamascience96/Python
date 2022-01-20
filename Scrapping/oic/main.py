import requests
from bs4 import BeautifulSoup
from Excel import Excel

url = "https://www.oic-oci.org/home/?lan=en"

base_addr = "https://www.oic-oci.org"

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


class Department:

    def __init__(self, title, link):
        self.title = title
        self.link = link
    
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
title = soup.title.get_text()


# get the hot news of the website
row_tag = soup.find_all(class_="row")
web_all_contents = row_tag[1].find(class_="col-lg-8");
hot_news_tag_list = web_all_contents.find(class_="row");
hot_news_tag_anchor_list = hot_news_tag_list.find_all('a');

list_of_anchortag = set();

for link in hot_news_tag_anchor_list:
    news_title = link.get_text()
    complete_link = link.get('href').replace('..', base_addr)
    if(news_title != "more"):
        hotnewsObj = HotNews(news_title, complete_link)
        list_of_anchortag.add(hotnewsObj)


# get all the departments
departments = web_all_contents.find_all("div", class_="panel-default")[1]
departments_heading = departments.find(class_="panel-heading").get_text()
departments_contents = departments.find(class_="panel-body").find("ul").find_all("li");

depart_list = list();
for li_elem in departments_contents:
    anchor = li_elem.find('a')
    depart_list.append(Department(anchor.get_text(), anchor.get('href').replace('..', base_addr)))


# get the address
address = soup.find('address').get_text().replace('Organisation of Islamic Cooperation', '')



excelObj = Excel()
excelObj.setTitle(title)

# set the hotnews
excelObj.setNewsTitle("Hot News")
excelObj.setHotNewsList(list_of_anchortag)

# set the department list
excelObj.setDepartmentTitle(departments_heading)
excelObj.setDepartmentList(depart_list)

# set the Address
excelObj.setAddresstoExcel(address)

# close the excelobj
excelObj.closeWorkBook()