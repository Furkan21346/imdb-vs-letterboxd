import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://letterboxd.com/films/top/rated-this-week/page/1/"
response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print("\nİlk 3000 karakter:")
print(response.text[:3000])