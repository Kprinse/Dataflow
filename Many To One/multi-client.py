import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b'Client message 1', b'Client message 2']

def service_connections(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(f'Received {repr(recv_data)} from {data.conn_id}')
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f'Closing Connection {data.conn_id}')
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f'Sending {repr(data.outb)} to Connection {data.conn_id}')
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def start_connections(host, port, num_of_connections):
    server_addr = host, port
    for i in range(0, num_of_connections):
        conn_id = i + 1
        print(f'Starting Connection {conn_id} to {server_addr}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            conn_id=conn_id,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=list(messages),
            outb=b''
        )
        sel.register(sock, events, data=data)

    events = sel.select(timeout=None)
    while events:
        for key, mask in events:
            service_connections(key, mask)