from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup

display = Display(visible=0, size=(800, 600))
display.start()


url = 'https://www.zillow.com/user/Login.htm'

driver = webdriver.Chrome()

driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
pint('We got the first soup')

driver.quit()


####


driver = webdriver.Chrome()

driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
pint('We got the second soup')

driver.quit()

#ex_zip = [24555]
#d_houses = sc.get_houses(driver, ex_zip)
#print(d_houses) 
display.stop()



