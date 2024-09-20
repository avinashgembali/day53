import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

from bs4 import BeautifulSoup
import requests

URL = ("https://appbrewery.github.io/Zillow-Clone/")
headers = {
    "Accept": f"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
              f"image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Dnt": "1",
    "Priority": "u=0, i",
}

response = requests.get(url=URL, headers=headers)
html_data = response.text
soup = BeautifulSoup(html_data, "html.parser")
price_tags = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
prices = []
for tag in price_tags:
    prices.append(tag.text.split('+')[0])
place_tags = []
for link in soup.find_all('a', class_="property-card-link", href=True):
    place_tags.append(link["href"])
address_tags = soup.find_all(name="address")
addresses = []
for tag in address_tags:
    addresses.append(tag.text.strip())
# continuing with selenium for sheets to interact

driver = webdriver.Chrome(options=chrome_options)
driver.get(url=f"https://docs.google.com/forms/d/e/1FAIpQLSdallzzYXWgapdFX"
               f"3OtzW1mPkDjFHPJgpn0jCr7yOS-9HW3Aw/viewform?usp=sf_link")
for i in range(44):
    time.sleep(3)
    address_fill = driver.find_element(By.XPATH, value="//input[@type='text' and @aria-describedby='i2 i3']")
    address_fill.click()
    address_fill.send_keys(addresses[i])

    price_fill = driver.find_element(By.XPATH, value="//input[@type='text' and @aria-describedby='i6 i7']")
    price_fill.click()
    price_fill.send_keys(prices[i])

    link_fill = driver.find_element(By.XPATH, value="//input[@type='text' and @aria-describedby='i10 i11']")
    link_fill.click()
    link_fill.send_keys(place_tags[i])

    button = driver.find_element(By.XPATH, value="//div[@role='button']")
    button.click()

    time.sleep(3)
    submit_another_response = driver.find_element(By.LINK_TEXT, value="Submit another response")
    submit_another_response.click()
    time.sleep(2)

driver.quit()