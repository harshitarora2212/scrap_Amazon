import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import time

browser = webdriver.Firefox()

#lists
title=[]
availability=[]
brand = []
ships_from=[]
sold_by= []
price=[]
price_per_weight =[]
size =[]
asin = []
asin_final = []
master_url = []

#all urls
url_list = [
    'https://www.amazon.com/dp/B07N1BVM9R',
    'https://www.amazon.com/dp/B0BRTDMQ3M',
    'https://www.amazon.com/dp/B010SCPNX8',
    'https://www.amazon.com/dp/B006609HYI',
    'https://www.amazon.com/dp/B079VP4D9N',
    'https://www.amazon.com/dp/B08XD9KBK3',
    'https://www.amazon.com/dp/B076DS3Y56',
    'https://www.amazon.com/dp/B0C595THZ1',
    'https://www.amazon.com/dp/B072KGKDZ5'
]


browser.get('https://www.amazon.com/dp/B07N1BVM9R')

#enter captcha
sleep(6)

#for chaning the pin location
pincode = browser.find_element(By.XPATH,'//*[@id="nav-global-location-popover-link"]')
pincode.click()
sleep(3)

#inputing the pincode
input = browser.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput"]')
input.send_keys('07054')
sleep(3)

#clicking apply
search_apply = browser.find_element(By.XPATH,'//*[@id="GLUXZipUpdate"]/span/input')
search_apply.click()
sleep(3)

#clicking apply
from selenium.webdriver.common.action_chains import ActionChains
x_coordinate = 100
y_coordinate = 200

# Create an ActionChains object
actions = ActionChains(browser)

# Move to the desired location and perform a click
actions.move_by_offset(x_coordinate, y_coordinate).click().perform()

sleep(3)


for url in url_list:
  #looping through each url
  browser.get(url)
  
  #variations
  product_types = browser.find_elements(By.XPATH,'//ul[@data-csa-c-type="widget"]/li[@data-csa-c-item-type]')
  print('variations:'+ str(len(product_types)))
  
  #since first url has no variations till line 154 is jus the copy
  if not product_types:
    title.append(browser.find_element(By.ID, 'productTitle').text)
    print(title)
    sleep(1)
    
    master_url.append(url)
    
    try:
      sleep(2)
      price_temp = browser.find_element(By.XPATH, '//*[@id="sns-base-price"]/div/span[1]')
      price.append(price_temp.text)
      print(price)
    except NoSuchElementException:
        try:
            sleep(2)
            price_temp =browser.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]')
            price_temp = price_temp.text.strip().split('\n')
            price.append(price_temp[0] + '.' + price_temp[1])
            price_per_weight.append(price_temp[2] + price_temp[3])
            print(price)
        except NoSuchElementException:
            price.append('Currently Unavailable')
            price_per_weight.append('Currently Unavailable')
    
    try:
      sleep(2)
      availability_element = WebDriverWait(browser, 25).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='availability']"))
      )
      availability.append(availability_element.text.replace('\n', ''))
      print(availability)
        
    except TimeoutException:
      try:
        availability_element = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="outOfStock"]/div/div[1]'))
        )
        availability.append(availability_element.text.replace('\n', ''))
        print(availability)
      
      except TimeoutException:
        try:
          availability_element = WebDriverWait(browser, 15).until(
          EC.visibility_of_element_located((By.XPATH, '//*[@id="availability"]/span[2]'))
          )
          availability.append(availability_element.text.replace('\n', ''))
          print(availability)
        except TimeoutException:
          availability.append('In stock')
          print(availability)
            
            

    try:
      brand_temp = browser.find_element(By.XPATH, '//*[@id="productOverview_feature_div"]/div/table/tbody/tr[1]/td[2]/span').text
      brand.append(brand_temp)
    except NoSuchElementException:
      brand.append('Currently Unavailable')
    
    try:
      ships_from.append(browser.find_element(By.XPATH,'//*[@id="sfsb_accordion_head"]/div[1]/div/span[2]').text)
    except NoSuchElementException:
      ships_from.append('Currently Unavailable')

    print(ships_from)
            
    try:
      sold_by.append(browser.find_element(By.XPATH,'//*[@id="sfsb_accordion_head"]/div[2]/div/span[2]').text)
    except NoSuchElementException:
      sold_by.append('Currently Unavailable') 

    print(sold_by)
    
    
    try:
      size_temp = browser.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr[2]/td[2]/span').text
      size.append(size_temp)
      
    except NoSuchElementException:
      size.append('Currently Unavailable')
      
    print(size)
    
    try:
      asin_temp = WebDriverWait(browser, 10).until(
          EC.visibility_of_element_located((By.XPATH, "//*[@id='detailBullets_feature_div']/ul/li/span[contains(., 'ASIN')]"))
      )
      asin.append(asin_temp.text)
    except TimeoutException:
      asin.append('Unavailable')  


  else:
      pass
    
  for variations in product_types:
    
    sleep(2)
    variations.click()
    sleep(3)
    
    master_url.append(url)
     
    title.append(browser.find_element(By.ID, 'productTitle').text)
    print(title)
    sleep(1)
    
    try:
      sleep(2)
      price_temp = browser.find_element(By.XPATH, '//*[@id="sns-base-price"]/div/span[1]')
      price.append(price_temp.text)
      print(price)
    except NoSuchElementException:
        try:
            sleep(2)
            price_temp =browser.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]')
            price_temp = price_temp.text.strip().split('\n')
            price.append(price_temp[0] + '.' + price_temp[1])
            price_per_weight.append(price_temp[2] + price_temp[3])
            print(price)
        except NoSuchElementException:
            price.append('Currently Unavailable')
            price_per_weight.append('Currently Unavailable')
    
    try:
      sleep(2)
      availability_element = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='availability']"))
      )
      availability.append(availability_element.text.replace('\n', ''))
      print(availability)
        
    except TimeoutException:
      try:
        availability_element = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="outOfStock"]/div/div[1]'))
        )
        availability.append(availability_element.text.replace('\n', ''))
        print(availability)
      
      except TimeoutException:
        try:
          availability_element = WebDriverWait(browser, 15).until(
          EC.visibility_of_element_located((By.XPATH, '//*[@id="availability"]/span[2]'))
          )
          availability.append(availability_element.text.replace('\n', ''))
          print(availability)
        except TimeoutException:
          availability.append('In stock')
          print(availability)
            

    try:
      brand_temp = browser.find_element(By.XPATH, '//*[@id="productOverview_feature_div"]/div/table/tbody/tr[1]/td[2]/span').text
      brand.append(brand_temp)
    except NoSuchElementException:
      brand.append('Currently Unavailable')
    
    try:
      ships_from.append(browser.find_element(By.XPATH,'//*[@id="sfsb_accordion_head"]/div[1]/div/span[2]').text)
    except NoSuchElementException:
      ships_from.append('Currently Unavailable')

    print(ships_from)
            
    try:
      sold_by.append(browser.find_element(By.XPATH,'//*[@id="sfsb_accordion_head"]/div[2]/div/span[2]').text)
    except NoSuchElementException:
      sold_by.append('Currently Unavailable') 

    print(sold_by)
    
    
    try:
      size_temp = browser.find_element(By.XPATH,'//*[@id="productOverview_feature_div"]/div/table/tbody/tr[2]/td[2]/span').text
      size.append(size_temp)
      
    except NoSuchElementException:
      size.append('Currently Unavailable')
      
    print(size)
    
    try:
      asin_temp = WebDriverWait(browser, 10).until(
          EC.visibility_of_element_located((By.XPATH, "//*[@id='detailBullets_feature_div']/ul/li/span[contains(., 'ASIN')]"))
      )
      asin.append(asin_temp.text)
    except TimeoutException:
      asin.append('Unavailable')
   
     
    print('end of variations')
  
  print('end of url_list')
        
        
        
'''for i in range(len(availability)):
  if availability[i]=='':
    availability[i] = 'Currently Unavailable'''
    
for i in range(len(ships_from)):
  if ships_from[i]=='':
    ships_from[i] = 'Currently Unavailable'

for i in range(len(sold_by)):
  if sold_by[i]=='':
    sold_by[i] = 'Currently Unavailable'
    
for asin_value in asin:
    asin_clean = asin_value.split(':')[1].strip()
    asin_final.append(asin_clean)


print('title:',title)
print('availability:',availability) 
print('brand:',brand)
print('ships_from:',ships_from)
print('sold_by:',sold_by)
print('price:',price)
print('size:',size)
print('asin_final:',asin_final)
print('master_url:',master_url)

pro_list = [title,availability,brand,ships_from,sold_by,price,size,asin_final,master_url]

df = pd.DataFrame(zip(*pro_list),columns = ['title','availability','brand','ships_from','sold_by','price','size','asin','master_url'])

df.index.name = 'product_id'

df.to_csv('productsfinal.csv')
 
browser.quit()

  
