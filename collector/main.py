import os
import requests
import base64
from datetime import datetime, timedelta
import pytz
from time import sleep



SAVE_DIR = '/SAVED_FRAMES'



# Hikvision Camera frame grabber
def hikvision_getFrame(timeNow, camera_ip, camera_userpass):
    headers = {
        'Authorization': f'Basic {base64.b64encode(camera_userpass.encode()).decode("utf-8")}',
    }
    response = requests.get(f'http://{camera_ip}/Streaming/channels/101/picture', headers=headers).content

    os.makedirs(f'{SAVE_DIR}/{camera_ip}', exist_ok=True)
    with open(f'{SAVE_DIR}/{camera_ip}/{timeNow}.jpg', 'wb') as f:
        f.write(response)





previousHour = None
while True:
    timeNow = datetime.now().strftime("%Y-%m-%d %H%M")
    currentHour = datetime.now().hour

    # First run, skip
    if(previousHour is None):
        previousHour = currentHour
        continue

    # New hour, fetch frames
    if(previousHour != currentHour):
        previousHour = currentHour
        print(f"New hour: {currentHour}")

        for i in range(20):
            CAMERA_TYPE = os.environ.get(f'CAMERA_TYPE_{i}')
            CAMERA_IP = os.environ.get(f'CAMERA_IP_{i}')
            CAMERA_USERPASS = os.environ.get(f'CAMERA_USERPASS_{i}')

            if(CAMERA_TYPE is None):
                continue

            try:
                for retry in range(5):
                    if(CAMERA_TYPE.upper() == "HIKVISION"):
                        hikvision_getFrame(timeNow, CAMERA_IP, CAMERA_USERPASS)
                        break
                    else:
                        print(f"Camera type not supported: {CAMERA_TYPE}")
                        break
                        
            except Exception as e:
                print(f"Exception fetching frame from {CAMERA_IP}: {e}")
                
    
    sleep(1)