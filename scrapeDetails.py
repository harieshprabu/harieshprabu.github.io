import sys
import time
import json
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import collections



#########################
## Crawl site
#########################

settings = json.load(open("settings.json"))
chrome_options = Options()
if(settings['headless']):
   chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get(settings['login_page'])
    print(settings['username'])
    driver.find_element(By.ID,"userName").send_keys(settings['username'])
    driver.find_element(By.ID,"userPassword").send_keys(settings['password'])
    time.sleep(settings['wait_timer'])
    driver.find_element(By.ID,"submit_button").click()
    time.sleep(settings['wait_timer'])
    driver.get(settings['booking_page'])
    time.sleep(settings['wait_timer'])

    with open('page.html', 'w') as f:
         f.write(driver.page_source)
         f.close()
    driver.quit()
except:
    driver.quit()
    exit(1)



#########################
## Parse Data 
#########################

data = {"slots": []}


result = {}

tempdatetime = {}
tempresource = {}




with open("page.html") as fp:
    soup = BeautifulSoup(fp,"html.parser")

i=0

for tag in soup.find_all("span", class_=["datetime","resource"]):
   #print(tag.string)
   #print(tag.attrs)
   if tag.get('class')[0] == "datetime":
       #print("datetime")
       key1="date"      
       value1=tag.string       
       #print(data)
   elif tag.get('class')[0] == "resource":
       #print("resource")
       key2="slot"
       value2=tag.string       
       #print(data)
       data['slots'].append({key1:value1,key2:value2})
   else:
      print("None")
   
json_data = json.dumps(data)
#print("RESULT")
#print(json_data)


## group by 


new_data = []
not_found = True
for item in data['slots']:
   for curdate in new_data:
      not_found=True
      if item['date'] == curdate['date']:
          not_found= False
          curdate['Court'].append({'slot':item['slot']})


   if not_found:
       new_data.append({'date':item['date'], 'Court' :[{'slot':item['slot']}]})

with open('results.json', 'w') as f:
     f.write(json.dumps(new_data))
     f.close()



#########################
## Updated Date
#########################

from datetime import datetime
now = datetime.now()


with open('update-time.txt', 'w') as f:
     f.write(now.strftime("%Y-%b-%d %H:%M:%S"))
     f.close()
