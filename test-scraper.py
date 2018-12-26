from selenium import webdriver
from bs4 import BeautifulSoup

url = 'https://www.zillow.com/user/Login.htm'

driver = sc.connect()

driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

#ex_zip = [24555]
#d_houses = sc.get_houses(driver, ex_zip)
#print(d_houses) 

print(soup)



