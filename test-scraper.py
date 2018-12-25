import scraper as sc

driver = sc.connect()

ex_zip = [24555]

d_houses = sc.get_houses(driver, ex_zip)

print(d_houses) 


