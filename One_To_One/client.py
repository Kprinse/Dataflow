import socket
from pickle import dumps, loads
import hmac
import hashlib
from device_model import Hardware

HOST = '127.0.0.1'
PORT = 65433
SECRET = b'e177047a-96b0-4996-8a38-a9faa9f1'

hardware = Hardware(
    {
        'Temp': (50, 55),
        'Carbon Monoxide': (0, 10),
        'Proximity': (5, 10)
     }
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = hardware.serialize()
    h = hmac.new(SECRET, message, hashlib.sha256)
    s.sendall(dumps((h.hexdigest(), message)))
    data = s.recv(1024)

received = loads(data)
print('Received: ', received)

test = hmac.new(SECRET, received[1], hashlib.sha256)
if hmac.compare_digest(received[0], test.hexdigest()):
    print('Data Received has been secured.')
else:
    print('Data isnt the same')
