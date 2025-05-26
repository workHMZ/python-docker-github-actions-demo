import requests
from bs4 import BeautifulSoup

url = "https://www.baidu.com/"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string
    print(f"爬虫结果 网站的标题是: {title}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    print("Please check your internet connection or the URL.")