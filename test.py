import requests
import json

r = requests.get('https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706', auth=('user', 'pass'))
r.status_code
r.encoding
with open("test_caching", 'w') as f:
    f.write(r.text)

