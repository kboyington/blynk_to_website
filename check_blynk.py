#!/root/vir_envs/flag_status/bin/python3
import requests
import datetime
from pytz import timezone

#set defaults
sub_message_1 = ''
sub_message_2 = ''

#read in API key
with open('/Users/kboyington/PycharmProjects/meadows_webpage/apikey.txt', 'r') as key:
    api_key = key.readline()

#make sure hardware is connected
hardware_connected = requests.get('http://45.55.96.146/{}/isHardwareConnected'.format(api_key))

# now get the status of the button
button_state = requests.get('http://45.55.96.146/{}/get/V2'.format(api_key))
button_state = int((button_state.json()[0]))
print(hardware_connected.text)

if button_state == 0:
    open_status = 'CLOSED'
if button_state == 1:
    open_status = 'OPEN'

#set error message if not connected
if hardware_connected.text == 'false':
    print("Hardware not connected!")
    open_status =  open_status + '*'
    sub_message_2 = 'Hardware not connected!'



# Read in the file
with open('/home/projects/webpage/index.html', 'r') as file :
  filedata = file.read()

#set timezone
eastern = timezone('US/Eastern')

# Replace the target string
filedata = filedata.replace('xxx_opened_or_closed_xxx', open_status)
filedata = filedata.replace('sub_message_1', "Last Checked {}".format(datetime.datetime.now(tz=eastern) .strftime('%b %d, %-I:%M %p')))
filedata = filedata.replace('sub_message_2', sub_message_2)


# Write the file out again
with open('/var/www/html/index.html', 'w') as file:
  file.write(filedata)
