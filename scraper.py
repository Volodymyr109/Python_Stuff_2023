from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import argparse

s = HTMLSession()
dealslist = []
searchterm = 'rammstein+vinyl'
url = f'https://www.amazon.de/s?k={searchterm}&crid=3RZX9RJFF9XE0&sprefix=%2Caps%2C137&ref=nb_sb_ss_recent_3_0_recent'

def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup


def getdeals(soup):
    products = soup.find_all('div', {'data-component-type': ''})
    for item in products:
        title = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        short_title = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()[:25]
        link = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
        try:
            saleprice = item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('€', '').strip()
            oldprice = item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('€', '').strip()
        except:
            oldprice = item.find('span', {'class': 'a-offscreen'})[1].text.replace('€', '').strip()
        try:
            reviews = item.find('span', {'class': 'a-size-base'}).text.strip()
        except:
            reviews = 0

        saleitem = {
            'title' : title,
            'short_title' : short_title,
            'link' : link,
            'saleprice' : saleprice,
            'oldprice': oldprice,
            'reviews': reviews,
            }
        dealslist.append(saleitem)
    return


def getnextpage(soup):
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disable a-last'}):
        url = 'https://www.amazon.de' + str(pages.find('li', {'class': 'a-disable a-last'}).find('a')['href'])
        return url
    else:
        return


while True:
    data = getdata(url)
    getdeals(data)
    url = getnextpage(data)
    if not url:
        break
    else:
        print(url)
        print(len(dealslist))

df = pd.DataFrame(dealslist)
df['percentoff'] = 100 - ((df.saleprice / df.oldprice) * 100)
df = df.sort_values(by=['percentoff'], ascending=False)
df.to_csv('D:\Python Projects\Scrraper\ '+ 'output_scraper_amazon.csv', index=False)
print('Fin.')