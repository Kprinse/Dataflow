import socket
from pickle import loads
import hmac
import hashlib

HOST = '127.0.0.1'
PORT = 65433
SECRET = b'e177047a-96b0-4996-8a38-a9faa9f1'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by: ', addr)
        while True:
            data = conn.recv(1024)
            print(data)
            if not data:
                break
            digest, message = loads(data)
            h = hmac.new(SECRET, message, hashlib.sha256)
            if hmac.compare_digest(digest, h.hexdigest()):
                print('Message Secured')
                print(loads(message))
            conn.sendall(data)