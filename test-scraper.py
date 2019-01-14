# from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import scraper as sc

# display = Display(visible=0, size=(800, 600))
# display.start()


url = 'https://www.zillow.com/user/Login.htm'

# driver = webdriver.Chrome()

# driver.get(url)

# html = driver.page_source
# soup = BeautifulSoup(html, 'lxml')
# print('We got the first soup')

# driver.quit()

# driver = webdriver.Firefox()
# login_url = "https://www.zillow.com/user/Login.htm"
# #access the login page
# driver.get(login_url)
# username = driver.find_element_by_id("email")
# password = driver.find_element_by_id("password")

# email = "elhjouji.zakaria@gmail.com"
# pwd = "Samsung123" 
# username.send_keys(email)
# password.send_keys(pwd)
# login_attempt = driver.find_element_by_xpath("//*[@type='submit']")
# login_attempt.submit()


####


# driver = webdriver.Chrome()

# driver.get(url)

# html = driver.page_source
# soup = BeautifulSoup(html, 'lxml')
# print('We got the second soup')

# driver.quit()

ex_zip = ['24555']

driver = sc.connect()
d_houses = sc.get_houses(driver, ex_zip)
driver.close()
print(d_houses) 
# display.stop()



