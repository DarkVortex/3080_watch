print('Code loaded. Beginning Imports!')
import requests
import time
from datetime import datetime
import os
import json
from pathlib import Path
from difflib import SequenceMatcher
print('Imports complete.')
def similar(a,b):
    return SequenceMatcher(None,a,b).ratio()

webhooks = []

with open('webhooks.json') as json_file:
    data = json.load(json_file)
    webhooks = data['WEBHOOKS']

print('Stored Webhooks:')
print(webhooks)

NVIDIA_URL = 'https://store.nvidia.com/store?Action=AddItemToRequisition&SiteID=nvidia&Locale=en_US&productID=5438481700&quantity=1'
EVENT = '3080_available'
GET_URL = 'https://maker.ifttt.com/trigger/'+EVENT+'/with/key/'

log_file = 'success_log.txt'

print('Starting Page Watch.')
getPage = requests.get(NVIDIA_URL)
getPage.raise_for_status()
prev_text = getPage.text
COUNT_TIME = 15
TOLERANCE = 0.99
changed = False
while True: #loop forever
    for i in range(1,COUNT_TIME+1):
        print(i)
        time.sleep(1)

    getPage = requests.get(NVIDIA_URL)
    getPage.raise_for_status()

    ratio = similar(prev_text,getPage.text)
    changed = ratio < TOLERANCE
    prev_text = getPage.text
    print("Changed: {} | Ratio: {:.5f}".format(changed,ratio))
    if changed:
        f = open(log_file,'a+')
        f.write('Success at {}, ratio: {:.5f} \n'.format(datetime.now(),ratio))
        f.close()
        print('making requests!')
        for key in webhooks:
            requests.post(GET_URL+key)
        