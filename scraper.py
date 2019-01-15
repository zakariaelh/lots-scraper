#!/usr/bin/env python
# coding: utf-8

# In[1]:


#start by importing necessary libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re

#import geocoder
#import gmplot
import urllib.parse
import progressbar
#import datefinder
import requests
import numpy as np
import time
from multiprocessing import Pool
import pandas as pd
from functools import partial
from selenium import webdriver
from scipy.spatial.distance import cdist
from geopy.distance import vincenty
from termcolor import colored
from selenium.webdriver.firefox.options import Options



# In[3]:

def connect():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options = options)
    login_url = "https://www.zillow.com/user/Login.htm"
    #access the login page
    driver.get(login_url)
    username = driver.find_element_by_id("email")
    password = driver.find_element_by_id("password")

    email = "elhjouji.zakaria@gmail.com"
    pwd = "zillow123" 
    username.send_keys(email)
    password.send_keys(pwd)
    login_attempt = driver.find_element_by_xpath("//*[@type='submit']")
    login_attempt.submit()
    return(driver)

#driver = connect()
# In[4]:


### Shapefile for l_places

# import fiona
# shape = fiona.open("/Users/zakariaelhjouji/Downloads/ZillowNeighborhoods-FL/ZillowNeighborhoods-FL.shp")

# l_places = [shape[i]['properties']['Name'] for i in range(len(shape))]


# ## Utils

# In[5]:


headers = requests.utils.default_headers()
headers.update({
    'User-Agent': '1' #'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})


# In[6]:


def get_info(ex):
    '''
    This function takes as input ex which is a listing in html and gives youall info we need about that listing
    '''
    #log
    d_info = dict()
    #latitude
    latitude = ex['data-latitude']
    #longitude
    longitude = ex['data-longitude']
    #url
    url = ex.a['href']
    #bed bath area
    bba = ex.find("span", class_ = "zsg-photo-card-info").get_text()
    bba = bba.split('·')
    #bed
    try:
        beds = [i for i in bba if 'bd' in i][0]
        beds = int([i for i in beds.split() if i.isdigit()][0])
    except Exception as e:
        print(colored('problem with beds in with', 'red'), ' ', url)
        print(e)
        beds = 'NA'
    #baths
    try:
        baths = [i for i in bba if 'ba' in i][0]
        #baths = int([i for i in baths.split() if i.isdigit()][0])
        baths = float(baths[:baths.find('ba')])
    except Exception as e:
        print('problem with baths in ', url)
        print(e)
        baths = 'NA'
    #area
    try:
        area = [i for i in bba if 'sqf' in i][0]
        area = area.replace(',', '')
        area = int([i for i in area.split() if i.isdigit()][0])
    except Exception as e:
        print('problem with area in ', url)
        print(e)
        area = 'NA'
    #price
    try:
        price = ex.find("span", class_ = "zsg-photo-card-price").get_text()
        price = price.replace(',', '')
    except Exception as e:
        print('problem with price in ', url)
        print(e)     
        price = 'NA'
    #address
    try:
        address = ex.find("span", class_ = "zsg-photo-card-address").get_text()
    except Exception as e:
        print('No address in ', url)
        print(e)
        address = ' NA'
    #log info
    d_info['lat'] = latitude
    d_info['lng'] = longitude
    d_info['url'] = 'https://zillow.com' + url
    d_info['beds'] = beds
    d_info['baths'] = baths
    d_info['area'] = area
    d_info['price'] = price
    d_info['address'] = address
    return(d_info)




# In[7]:


def get_npages(base_url):
    page = requests.get(base_url, headers = headers)
    soup = BeautifulSoup(page.content, "lxml")
    try:
        l_n = soup.find("ol", class_ = "zsg-pagination").find_all("li")
        l_n = [i.get_text() for i in l_n]
        l_n = [int(i) for i in l_n if i.isdigit()]
        n_pages = max(l_n)
    except Exception as e:
        #print(base_url)
        print(e)
        n_pages = 1
    return(n_pages)


# In[8]:


def get_houses(driver, places_int, n_pages = 'auto'):
    '''
    places_int: places of interest (i.e. places we would like to scrape) 
    NOTE: places_int should be a list of indices
    n_pages: number of pages we would like to scrape per neighborhood. If this was set to 'auto', then we scrape everything 
    in that neighborhood. 
    '''
    l_e = []
    d_all_info = dict()
    j = 0
    for place in places_int:
        #place_det = shape[ip]['properties']
        #place = place_det['Name']
        print('place visited: ', place)
        place = place.replace(' ', '-')
        url_neigh = 'https://www.zillow.com/homes/for_sale/' + place + '/house,condo,apartment_duplex_type/' #-Orlando-FL_rb/'
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': str(np.random.randint(1e4)) #'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        n_pages_auto = get_npages(url_neigh)
        if n_pages == 'auto':
            #get the number of pages in that place automatically
            n_pages = n_pages_auto
            print('Number of pages in this url are: ', n_pages)
        else:
            #we only extract the number of pages requested per place
            n_pages = min(n_pages, n_pages_auto)
        bar = progressbar.ProgressBar()
        for p in bar(range(n_pages)):
            url = url_neigh + str(p) +'_p/'
            #sess = requests.session()
            #page = sess.get(url, headers = headers)
            #soup = BeautifulSoup(page.content, "lxml")
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            #get list of all listings in that page
            l_listings = soup.find("div", {'id' : 'list-results'}).ul.find_all("article")
            n_e = 0
            for ex in l_listings:
                a = get_info(ex)
                a['neigh'] = place
                #a['city'] = place_det['City']
                #a['county'] = place_det['County']
                d_all_info[j] = a
                if 'AuthRequired' in a['url']:
                    n_e += 1
                #print(a)
                j += 1
            #log the number of auth required errors per page 
            l_e.append([url_neigh, n_e])
            if n_e > 0:
                headers.update({'User-Agent': str(np.random.randint(1e4))})
            time.sleep(5)
    #format results 
    d_all_info = pd.DataFrame.from_dict(d_all_info).T
    l_e = pd.DataFrame(l_e, columns = ['url', 'n_e'])
    return(d_all_info, l_e)


# In[37]:


def get_info_lot(ex):
    d_info = dict()
    #url
    link = ex.find("a")['href']
    d_info['url'] = 'https://zillow.com' + link
    #area
    try:
        area = ex.find("span", class_ = "zsg-photo-card-info").get_text()
        d_info['area'] = area
    except:
        print('problem with area in ', link)
        d_info['area'] = 'NA'
    #price
    try:
        price = ex.find("span", class_ = "zsg-photo-card-price").get_text()
        d_info['price'] = price
    except:
        print('problem with price in ', link)
        d_info['price'] = 'NA'
    #coordinates lat lon
    try:
        lat = ex.find("meta", {'itemprop': 'latitude'})['content']
        lng = ex.find("meta", {'itemprop': 'longitude'})['content']
        d_info['lat'] = lat
        d_info['lng'] = lng
    except Exception as e:
        try:
            #print('laitude: ', ex['data-latitude'])
            #print('longitude: ', ex['data-longitude'])
            lat = float(ex['data-latitude'])/1e6
            lng = float(ex['data-longitude'])/1e6
            d_info['lat'] = lat
            d_info['lng'] = lng
        except:
            print('problem with lat-lon')
            print(lot)
            d_info['lat'] = 'NA'
            d_info['lng'] = 'NA'
    #address
    try:
        address = ex.find("span", class_ = "zsg-photo-card-address").get_text()
        d_info['address'] = address
    except Exception as e:
        print('No address in ', url)
        print(e)
        address = ' NA'
        d_info['address'] = address
    return(d_info)


# In[30]:


def get_lots(driver, places_int, n_pages = 'auto'):
    l_e = []
    #dictionary storing lots
    d_lots = dict()    
    j = 0
    for place in places_int:
        #place_det = shape[ip]['properties']
        #place = place_det['Name']
        print('place visited: ', place)
        place = place.replace(' ', '-')
        url_neigh = 'https://www.zillow.com/homes/for_sale/' + place + '/land_type/' #-Orlando-FL_rb/'
        print('place url: ', url_neigh)
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': str(np.random.randint(1e4)) #'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        n_pages_auto = get_npages(url_neigh)
        if n_pages == 'auto':
            #get the number of pages in that place automatically
            n_pages = n_pages_auto
            print('Number of pages in this url are: ', n_pages)
        else:
            #we only extract the number of pages requested per place
            n_pages = min(n_pages, n_pages_auto)
        bar = progressbar.ProgressBar()
        for p in bar(range(1, n_pages+1)):
            url = url_neigh + str(p) +'_p/'
            #page = requests.get(url, headers = headers)
            #soup = BeautifulSoup(page.content, "lxml")
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            #get list of all listings in that page
            l_lots = soup.find("div", {'id': 'search-results'}).find_all("article")
            if len(l_lots) == 0:
                print('no lots available in ', url)
            n_e = 0 #number of errors iwth authrequired
            for lot in l_lots:
                a = get_info_lot(lot)
                a['neigh'] = place
                #a['city'] = place_det['City']
                #a['county'] = place_det['County']
                d_lots[j] = a
                if 'AuthRequired' in a['url']:
                    n_e += 1
                    time.sleep(5)
                j += 1
            #log the number of auth required errors per page 
            l_e.append([url, n_e])
            time.sleep(10)
    #format results 
    d_lots = pd.DataFrame.from_dict(d_lots).T
    l_e = pd.DataFrame(l_e, columns = ['url', 'n_e'])
    return(d_lots, l_e)

def clean_price(x):
    '''
    takes as input price column and clean prices
    '''
    try:
        return int(''.join(re.findall(r'\d+', x)))
    except:
        #print(x)
        return None
    
def clean_area(x):
    '''
    takes as input area column and clean areas
    '''
    try:
        return int(''.join(re.findall(r'\d+', x)))
    except:
        #print(x)
        return None
    
def get_psqft(x):
    '''
    takes as input df and creates as df column with psqft
    '''
    try:
        return x['price'] / x['area']
    except Exception as e:
        return None

def clean_lots(d_lots):
    '''
    takes as input d_lots (output of scraper function) and cleans it
    '''
    d_lots['price' ] = d_lots.price.apply(clean_price)
    d_lots['area'] = d_lots.area.apply(clean_area)
    return d_lots

def clean_houses(d_houses):
    '''
    takes as input d_houses (output of scraper function) and cleans it
    '''
    #lat,lng
    boo = d_houses.lat.apply(lambda x : x != 'NA')
    d_houses.loc[boo, 'lat'] = d_houses[boo].lat.astype(int) / 1e6
    d_houses.loc[boo, 'lng'] = d_houses[boo].lng.astype(int) / 1e6
    #price
    d_houses['price'] = d_houses.price.apply(clean_price)
    #pm2
    d_houses['price_sqft'] = d_houses[['price', 'area']].apply(get_psqft, axis = 1)
    return(d_houses)

def dis(a, b):
    '''
    takes as input two matrices and calculates distance between them
    '''
    m_dist = cdist(a, b,# Coordinates matrix or tuples list
               # Vicenty distance in lambda function
               lambda u, v: vincenty(u, v).kilometers)
    return m_dist

def g(i, d_lots, d_houses):
    '''
    takes as input index of a lot and calculate distances between this lot and all houses
    '''
    l = np.array(list(d_lots[['lat', 'lng']].iloc[i])).reshape((1,2))
    #l_dist = d_houses[['lat', 'lng']].apply(lambda x: distance(l, x).m, axis = 1)
    l_dist = dis(l, d_houses[['lat', 'lng']])
    return l_dist

def get_distance(d_lots, d_houses):
    '''
    takes d_lots and find distances between each lot and the houses
    return: a list of list of ditances between each lot and all the houses
    '''
    print('getting distances')
    p = Pool(10)
    l_h = p.map(partial(g, d_lots = d_lots, d_houses = d_houses), range(d_lots.shape[0]))
    p.terminate()
    p.join()
    print('distances completed')
    return(l_h)

def get_avg(i, l_h, max_dist, d_houses):
    '''
    takes as input the index of the lot and outputs the average price of houses within a specific radius 
    set by max_dist
    '''
    l = d_houses[l_h[i][0] < max_dist].price_sqft
    l_ = l[pd.notnull(l)]
    avg_price = np.mean(l_)
    return avg_price

#TEST


# In[173]:
# driver = connect()
# d = dict()
# d['driver'] = driver
# print(d)
# url = 'https://www.zillow.com/homes/for_sale/Wingina-VA-24599/land_type/68239_rid/37.751037,-78.617992,37.556418,-78.865185_rect/11_zm/'
# a = d['driver']
# a.get(url)
# html = driver.page_source
# print('success')
# print('Closing....')
# driver.quit()
# print('driver closed')


