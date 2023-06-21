import socket
import time

known_port:int = 50002

sock:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 55555))

connections = {}

while True:
    while True:

        key, client1 = sock.recvfrom(128)

        print(f'connection from: {client1}')

        sock.sendto(b'ready', client1)


        # first one to enter a given key
        if key not in connections:
            connections[key] = client1
            break
        # we have a peer to connect with
        else:
            print('sending peer info to client')
            # get infor for both clients
            addr1, port1 = client1
            client2 = connections.pop(key)
            addr2, port2 = client2
            # send info to both clients to connect
            sock.sendto(f'{addr1} {port1} {known_port}'.encode(), client2)
            sock.sendto(f'{addr2} {port2} {known_port}'.encode(), client1)
            break