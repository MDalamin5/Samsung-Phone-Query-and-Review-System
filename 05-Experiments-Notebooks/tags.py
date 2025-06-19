import requests
from bs4 import BeautifulSoup

## read the html documents

with open("sample.html", "r") as f:
    html_docs = f.read()
    
soup = BeautifulSoup(html_docs, "html.parser")

print(soup.prettify())