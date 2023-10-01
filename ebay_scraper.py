import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.ebay.de/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rammstein+vinyl&_sacat=0&LH_TitleDesc=0&_odkw=gitarren&_osacat=0"

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__wrapper clearfix'})
    for item in results:
        product = {
            'tittle': item.find('span', {'role': 'heading'}).text,
            'soldprice': item.find('div', {'class': "s-item__detail s-item__detail--primary"}).text,
            #'soldprice': item.find('div', {'class': "s-item__detail s-item__detail--primary"}).text,
            'bids': item.find('span', {'class': 'SECONDARY_INFO'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        productslist.append(product)
    return productslist

def prices(soup):
    pricelist = []
    optimaleprice = soup.find_all('div', {'class': "s-item__detail s-item__detail--primary"})
    for item in optimaleprice:
        price = {
            'soldprice': float(item.find('div', {'class': 's-item__detail s-item__detail--primary'}).text.replace('£', '').replace(',', '').strip()),
            #'soldprice': item.find('div', {'class': "s-item__detail s-item__detail--primary"}).text,
        }
        if 'soldprice' < 130:
            print("Sehr teuer")
        else:
            print("Ganz ok")

        pricelist.append(price)
    return pricelist


def output(productslist, pricelist, url):
    productsdf =  pd.DataFrame(productslist, pricelist)
    productsdf.to_csv('D:\Python Projects\Scrraper\' '+ 'output.csv', index=False)
    print('Saved to CSV')
    return


soup = get_data(url)
productslist = parse(soup)
pricelist = parse(soup)
output(productslist, pricelist, url)










