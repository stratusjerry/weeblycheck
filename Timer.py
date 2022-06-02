import requests
import random
import time
from datetime import datetime

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
## Variables to edit:
storeURL = "www.WEEBLYSTORE.com"
user = "131267684"
site = "874863029496319949"
prodPerPage = "60" #Default 60, can set lower if less expected
OHcat = "11ea6d492c1c3ceda2130cc47a2ae378"
BurialCat = "11ec73f0f798faa4bb6c6abbb74a6a8e"
cat = OHcat
useProxy = False
sleepMin = 60; sleepMax = 300
#randTimer = True
#randRange = 10

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
url = "https://" + storeURL + "/app/store/api/v8/editor/users/" + user + "/sites/" + site + "/products?page=1&per_page=" + prodPerPage + "&sort_by=category_order&sort_order=asc&categories[]=" + cat
timer = 60
# Don't change below

#TODO: add proxies
# This bell character nonprintable may not work on all systems 
def alert():
    print('/a')


def web_call(url, useProxy=False):
    try:
        #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        headers = {'User-Agent': user_agent}
        # Make web request and don't verify SSL/TLS certs
        if useProxy:
            response = requests.get(url, headers=headers, verify=False, proxies=proxies)
        else:
            response = requests.get(url, headers=headers, verify=False)
        #return response.text
        return response
    except Exception as e:
        print('[!]   ERROR - Web Call issue: {}'.format(str(e)))
        exit(1)


def parse_data(web_data):
    #text = web_data.text
    # Who knew requests had a json function!
    data = web_data.json()
    meta = data.get('meta')
    pagination = meta.get('pagination')
    total_items = pagination.get('total')
    return total_items


first_request_time = datetime.now()
first_response = web_call(url)
first_total = parse_data(first_response)

next_response = web_call(url)
next_total = parse_data(next_response)

web_count = 2
#TODO: logic for changing first_call if inventory goes below first_call
while next_total <= first_total:
    web_count += 1
    time.sleep(random.uniform(sleepMin, sleepMax))  # Throttle requests, uniform vs randint for floating numbers
    last_request_time = datetime.now()
    next_response = web_call(url)
    next_total = parse_data(next_response)


alert()
alert()
first_total = 17
next_total = 1
while next_total <= first_total :
    next_total += 1
    print(next_total)

pretty_first_time = first_request_time.strftime("%H:%M:%S")
pretty_last_time = last_request_time.strftime("%H:%M:%S")
time_diff = last_request_time - first_request_time
minutes = divmod(time_diff.total_seconds(), 60)
print(f'Total Count: {web_count} First Request: {pretty_first_time} Last Request: {pretty_last_time} Total Time: {int((minutes[0]))} minutes {int((minutes[0]))} seconds')
