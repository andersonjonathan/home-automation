from subprocess import Popen, PIPE

import re

from secrets import AUTH


def get_raw_DNS_page():
    p = Popen(['curl', '-X', 'GET', '-H', 'Cookie: Authorization=Basic {auth};path=/'.format(auth=AUTH), '-H', 'Cache-Control: no-cache',  'http://192.168.1.1/../userRpm/LoginRpm.htm?Save=Save'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(output))[0]
    url = url.replace('Index', 'AssignedIpAddrListRpm')
    p = Popen(['curl', '-X', 'GET', '-H', 'Cookie: Authorization=Basic {auth};path=/'.format(auth=AUTH), '-H', 'Cache-Control: no-cache',  url], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    return output


def get_connected_devices():
    devices = []
    content = []
    for t in range(0, 2, 1):
        output = get_raw_DNS_page()
        try:
            content = re.findall('var DHCPDynList = new Array\((.*?)0,0 \);', str(output), flags=re.MULTILINE | re.DOTALL)[0].split('\n')[1:-1]
            break
        except IndexError:
            pass
    if not content:
        raise ValueError("Couldn't get or parse the data")
    for row in content:
        data = row[1:-2].split('", "')
        devices.append({
            "name": data[0],
            "mac": data[1],
            "ip": data[2],
            "lease": data[3]
        })
    return devices


def get_global_ip():
    p = Popen(['curl', 'http://ipinfo.io/ip'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    return output.strip()

if __name__ == '__main__':
    print(get_global_ip())