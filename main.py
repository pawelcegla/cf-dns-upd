import json
import requests
import sqlite3
import sys

ip = requests.get('https://api.ipify.org').text
print(ip)
con = sqlite3.connect(sys.argv[1])
with con:
    cur = con.cursor()
    (token, zone_id, dns_record_id, dns_record_name) = cur.execute('SELECT token, zone_id, dns_record_id, dns_record_name FROM config').fetchone()
    res = requests.patch('https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(zone_id, dns_record_id),
                         headers={'Authorization': 'Bearer {}'.format(token)},
                         json={'name': dns_record_name, 'content': ip, 'type': 'A'})
    print(res.status_code)
    print(res.text)
con.close()
