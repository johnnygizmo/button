#! /usr/bin/env python


import requests
from socket import gethostname, gethostbyname


headers = {
    'cache-control': "no-cache",
}

payload = gethostname()+" "+gethostbyname(gethostname())
hook = {"value1": payload,
        "value2": response.status_code, 
        "value3": ""}

response = requests.request("POST", 
                            "https://maker.ifttt.com/trigger/button_triple/with/key/dhh2AN6ZYlKW4o6Bl6ImY0", 
                            data=hook, 
                            headers=headers)
