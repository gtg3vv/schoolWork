import urllib.request
import re
import os.path

real_open = urllib.request.urlopen
def cachingURLOpen(url, *args, **kwargs):
    global real_open
    cacheName = ".cache-"+re.sub("[^a-zA-Z0-9]","_",url)
    if not os.path.exists(cacheName):
        tmp = real_open(url, *args, **kwargs)
        content = tmp.read()
        tmp.close()
        with open(cacheName, 'wb') as f:
            f.write(content)
    return open(cacheName, 'rb')
urllib.request.urlopen = cachingURLOpen


