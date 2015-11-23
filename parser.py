#!/usr/bin/env python
import requests
import csv
import StringIO
import re
import base64

csv_vpngate = "http://www.vpngate.net/api/iphone/"
response = requests.get(csv_vpngate)
#response.encoding = 'ISO-8859-1'
text_raw = response.text.encode("utf-8")
#print (text)

# remove *vpn_servers
text_remove_1 = re.sub(r"\*vpn_servers\r\n", "", text_raw)
text = re.sub(r"#HostName","HostName", text_remove_1)
#print text

csv_reader = csv.DictReader(StringIO.StringIO(text))

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
                f.write(decoded)
