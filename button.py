#! /usr/bin/env python

import RPi.GPIO as GPIO
import requests
import time
import datetime
from socket import gethostname


headers = {
    'cache-control': "no-cache",
}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

r = requests.get("http://www.google.com")
if r.status_code == 200:
    GPIO.output(17, GPIO.HIGH)

runTime = time.time()
prevTime = 0
pressed = 0
pressSession = 0
presses = 0
try:
    while True:
        if GPIO.input(18) == True and pressed == 0:
            if presses == 0:
                pressSession = time.time()
                presses = 1
            else:
                presses = presses + 1

            pressed = 1
            time.sleep(0.15)
        elif GPIO.input(18) == False and pressed == 1:
            pressed = 0

            if presses == 3:
                presses = 0

                l = time.localtime()
                d = datetime.datetime(
                    l.tm_year, l.tm_mon, l.tm_mday, l.tm_hour, l.tm_min)

                url = "https://trigger.omnilert.net/cap/180999ef9ebe69ae746f8d91a0c8938d_c217bc526095013b4445"

                payload = """<alert xmlns = \"urn:oasis:names:tc:emergency:cap:1.2\">
							<identifier>1</identifier>
							<sender>jmatthews</sender>
							<sent>""" + d.isoformat() + """</sent>
							<status>Actual</status>
							<msgType>Alert</msgType>
							<source>Actual</source>
							<scope>Public</scope>
							<code>green</code>
							<info>
							<category>Safety</category>
							<event>Security Call Button</event>
							<urgency>Immediate</urgency>
							<severity>Severe</severity>
							<certainty>Observed</certainty>
							<headline>"""+gethostname()+"""</headline>
							<description>"""+gethostname()+"""</description>
							<instruction>instruction goes here</instruction>
							</info>
							</alert>"""

                response = requests.request(
                    "POST", url, data=payload, headers=headers)
                hook = {"value1": payload,
                        "value2": response.status_code, "value3": ""}
                response = requests.request(
                    "POST", "https://maker.ifttt.com/trigger/button_triple/with/key/dhh2AN6ZYlKW4o6Bl6ImY0", data=hook, headers=headers)

                for i in range(20):
                    GPIO.output(27, GPIO.LOW)
                    time.sleep(100)
                    GPIO.output(27, GPIO.HIGH)
		    time.sleep(100)
			
        if presses > 0 and time.time() - pressSession > 5:
            presses = 0

        prevTime = runTime
        runTime = round(time.time())
        if runTime % 120 == 0 and runTime != prevTime:
            r = requests.get("http://www.google.com")
            if r.status_code == 200:
                GPIO.output(17, GPIO.HIGH)
            else:
                GPIO.output(17, GPIO.LOW)
except:
    print("Execution Error - Stopping")

finally:
    GPIO.cleanup()
