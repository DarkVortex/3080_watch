print('Code loaded. Beginning Imports!')
import requests
import time
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
print('Starting Page Watch.')
getPage = requests.get(NVIDIA_URL)
getPage.raise_for_status()
prev_text = getPage.text
changed = False
COUNT_TIME = 15
TOLERANCE = 0.999
while not changed:
    for i in range(1,COUNT_TIME+1):
        print(i)
        time.sleep(1)

    getPage = requests.get(NVIDIA_URL)
    getPage.raise_for_status()

    ratio = similar(prev_text,getPage.text)
    changed = ratio < TOLERANCE
    prev_text = getPage.text
    print("Changed: {} | Ratio: {:.5f}".format(changed,ratio))

print('making requests!')
for key in webhooks:
    requests.post(GET_URL+key)