#1
import time
import pyrebase
import os
import queue
import can
from threading import Thread


#2 setup firebase and
#firebase
config = {
  "apiKey": "AIzaSyAyXz2HwHbXhOx-Wp7uBEAzwiDgoMS5rdY",
  "authDomain": "idtc-47cf5.firebaseapp.com",
  "databaseURL": "https://idtc-47cf5.firebaseio.com",
  "projectId": "idtc-47cf5",
  "storageBucket": "idtc-47cf5.appspot.com",
}
firebase = pyrebase.initialize_app(config)


#3 authentication
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("test@gmail.com", "abc123")
db = firebase.database()


# Open the CAN channel on Raps
# https://github.com/skpang/PiCAN-Python-examples/blob/master/obdii_logger.py
print('Bring up CAN0....')
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)	
print('Ready')

# Create a bus connection
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board')
    exit()


# Define the function to receive message and save them to a queue
def can_rx_task()
    while True:
        # TODO: Add filter to only listen to 1 message
        message = bus.recv()


rx = Thread(target=can_rx_task)
rx.start()

#4 start time when script runs
startTime = time.time()
refreshTimer = time.time()

#5 Main loop
try:
    while True:

        #6 check current time when loop starts
        currentTime = time.time()

        #7 Update firebase every 5s
        if (currentTime - startTime) >= 5:
            #timestamp = time.strftime("%c")
            #data = {"spn": "590000", "ftb": "40", "time": timestamp}
            #db.child("idtc").push(data, user["idToken"])
            #print(message)
            data = {"data": message.data[3], "time": time.time()}
            db.child("soc").push(data,user["refreshToken"])
            startTime = currentTime
            
        #8 refresh user token
        if (currentTime - refreshTimer) >= 1800:
            user = auth.refresh(user["refreshToken"])
            refreshTimer = currentTime
            print("token refresh: %s" % (time.strftime("%c")))
        
        time.sleep(1)
except KeyboardInterrupt:
    # Catch keyboard interrupt
    os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')
