import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.amazon.de/s?k=rammstein+vinyl&crid=3RZX9RJFF9XE0&sprefix=%2Caps%2C137&ref=nb_sb_ss_recent_3_0_recent'

r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')

script = soup.find_all('script')

data = json.loads(script)

print(data)