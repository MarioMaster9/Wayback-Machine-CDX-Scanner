# CDX Scanner Configuration
url = "" # Url to traverse

fromTime = None # Range Start (EX: 200501)
toTime = None # Range End (EX: 200605)


fields = [
    "timestamp",
    "original"
]

continueAfter = None # Set this to start scanning after a specific prefix (if you stopped the script)

# Prefixes to skip (Example: wat (It would probably cause issues with youtube))
skipPrefixes = [

]

# Key filters
filters = [
    "statuscode:200"
]


# CHARSET
charset = "abcdefghijklmnopqrstuvwxyz0123456789"

# Size of prefix for traversing
prefixSize = 3






# Computed Stuff

# CDX RANGE
cdxTime = ""
if not fromTime is None:
    cdxTime += f"&from={fromTime}"
if not toTime is None:
    cdxTime += f"&to={toTime}"


# Remove slash from end of url if it exists
url.removesuffix("/")


# SCAN PREFIXES (makes traversing CDX better)
scanPrefixes = []
def createPrefixes(prefix, size):
    if size == 0:
        scanPrefixes.append(prefix)
    else:
        for char in charset:
            createPrefixes(prefix+char, size-1)
createPrefixes("", prefixSize)

# URLS
computedUrls = []

for prefix in scanPrefixes:
    fullUrl = f"https://web.archive.org/cdx/search/cdx?url={url}/{prefix}*{cdxTime}"
    if len(fields) != 0:
        fullUrl += f"&fl="
        for i, field in enumerate(fields):
            if i != 0:
                fullUrl += ","
            fullUrl += field
    if not fields is None:
        fullUrl += f"&fl={fields}"
    for cdxFilter in filters:
        fullUrl += f'&filter={cdxFilter}'
    fullUrl += "&showResumeKey=true"
    computedUrls.append(fullUrl)
