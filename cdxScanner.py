# Wayback Machine CDX Scanner
# made by pew
#
# makeWebReq and writeLogs are from rbxdl.py

import requests
import time
import os
import cdxScanner.config as config

scriptName = os.path.splitext(os.path.basename(__file__))[0]

logFileName = f"{scriptName}.log"

def writeLogs(msg):
    with open(logFileName, "a") as logFile:
        logFile.write(f"{msg}\n\n")

def makeWebReq(url):
    try:
        resp = requests.get(url)
        resp.close()
        return [resp.status_code, resp]
    except requests.RequestException as e:
        print("Exception occured whilst making request. This has been logged.")
        writeLogs(e)

loopWait = 1

stopContinue = False

for index, requestUrl in enumerate(config.computedUrls):
    prefix = config.scanPrefixes[index]
    if not stopContinue:
        print(f"Skipping {prefix}")
        if prefix == config.continueAfter:
            stopContinue = True
        continue
    if prefix in config.skipPrefixes:
        print(f"(HARDCODED) Skipping {prefix}")
        continue
    info = None
    while True:
        info = makeWebReq(requestUrl)
        if info is None or info[0] != 200:
            
            print(f"Sleeping {loopWait*5} seconds!!!")
            time.sleep(loopWait*5)
            loopWait = ((loopWait - 1) % 5) + 1
        else:
            break
    content = info[1].content
    if len(content) == 0:
        print(f'{prefix} is empty')
    else:
        print(f"Writing {prefix}.txt")
        with open(f'{prefix}.txt','wb+') as f:
            f.write(content)
    time.sleep(1)
