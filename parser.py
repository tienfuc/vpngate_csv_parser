#!/usr/bin/env python
import requests
import csv
import StringIO
import re
import base64

csv_vpngate = "http://www.vpngate.net/api/iphone/"
response = requests.get(csv_vpngate)
text_raw = response.text.encode("utf-8")

text_remove_1 = re.sub(r"\*vpn_servers\r\n", "", text_raw)
text = re.sub(r"#HostName","HostName", text_remove_1)

csv_reader = csv.DictReader(StringIO.StringIO(text))
count = 0

for csv in csv_reader:
    hostname = csv["HostName"]
    ip = csv["IP"]

    try:
        decoded = base64.b64decode(csv["OpenVPN_ConfigData_Base64"])
    except:
        pass
    finally:
        if( hostname and ip and decoded ):
            filename = "%s_%s.ovpn" % (hostname, ip)
            with open(filename, "w+") as f:
                count+=1
                f.write(decoded)

print "Total parsed %d files" % count
