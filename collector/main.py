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

            if(CAMERA_TYPE.upper() != "HIKVISION"):
                print(f"Camera type not supported: {CAMERA_TYPE}")
                continue

            for attempt in range(3):
                try:
                    hikvision_getFrame(timeNow, CAMERA_IP, CAMERA_USERPASS)
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1}/3 failed for {CAMERA_IP}: {e}")
                    if attempt < 2:
                        sleep(10)
                
    
    sleep(1)