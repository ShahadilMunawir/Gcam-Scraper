import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.celsoazevedo.com/files/android/google-camera/").content
soup = BeautifulSoup(r, "html.parser")

main_block = soup.find("ul", class_="listapks")
latest = main_block.find_all("li")[0]
gcam = latest.a.text
link = latest.a["href"]
print(gcam, link)