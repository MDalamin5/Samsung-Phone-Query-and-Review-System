import requests
from bs4 import BeautifulSoup

## read the html documents

with open("sample.html", "r") as f:
    html_docs = f.read()
    
soup = BeautifulSoup(html_docs, "html.parser")

# print(soup.prettify())
# print(soup.div) # for single div

# print(soup.find_all("div"))
# print(soup.find_all("div")[2])

# print(soup.find(class_=="hello1"))

# for link in soup.find_all("a"):
#     print(link)

# for link in soup.find_all("a"):
#     # print(link.string)
#     print(link.get_text())

# s = soup.find(id="link3")
# print(s.string)
# print(s.get_text())

# print(soup.select_one("div.hello"))

# print(soup.div.get("class"))

# print(soup.span.get("class"))

# print(soup.find(class_="hello1"))

# for child in soup.find(id="container").children:
#     print(child)

i = 1

for parent in soup.find(class_="box").parents:
    print(parent.get_text())
    if i == 2:
        break
    i += 1
    