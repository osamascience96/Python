import requests
from bs4 import BeautifulSoup

url = "https://codewithharry.com"

# Get the HTML
r = requests.get(url)
htmlContnt = r.content
# print(htmlContnt)

# Parse the html content
soup = BeautifulSoup(htmlContnt, "html.parser")
# print(soup.prettify())

title = soup.title
print(title)

print("--------------------------")

paras = soup.find_all('p')
print(paras)

print("--------------------------")

anchors = soup.find_all('a')
all_links = set()
for link in anchors:
    data = link.get("href")
    if(data != "#" and data != "/" and ('facebook' not in data and 'instagram' not in data)):
        all_links.add(url + data)

print(all_links)    

print("--------------------------")

first_para = soup.find('p')
print(first_para)

print("--------------------------")
first_para_class = first_para['class']
print(first_para_class)

print("--------------------------")
elements_of_lead = soup.find_all('p', class_='mt-2')
print(elements_of_lead)

print("---------------------------")
print(first_para.get_text())

print("----------------------------")
print(soup.get_text())

