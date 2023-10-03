from requests_html import HTMLSession
from bs4 import BeautifulSoup
session = HTMLSession()
url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtUmxHZ0pFUlNnQVAB?hl=de&gl=DE&ceid=DE%3Ade'

r = session.get(url)
r.html.render(sleep=1, scrolldown=5)

articels = r.html.find('article')

newslist = []

for item in articels:
    try:
        newsitem = item.find('h3', first=True)
        newsarticle = {
        'title' : newsitem.text,
        'link' : newsitem.absolute_links,
        }
        newslist.append(newsarticle)
    except:
        pass

print(len(newslist))