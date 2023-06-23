import socket
import time
import requests
import json
from flask import Flask, jsonify

# # get rendezvous server ip
# rendezvous = requests.get('https://rendezvous-server.herokuapp.com/').text
# rendezvous = rendezvous.split(':')
# rendezvous = (rendezvous[0], int(rendezvous[1]))

print('starting server')

# find available port
# sock:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(('0.0.0.0', 0))
# server_port = sock.getsockname()[1]
# sock.close()
# sock:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('0.0.0.0', server_port))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 0))
server_port = sock.getsockname()[1]


# get and print ip and port
print('getting ip...')
reponse = requests.get('https://api.ipify.org?format=json')
server_ip = reponse.json()['ip']
print(f'using ip: {server_ip}')
print(f'using port: {server_port}')


# # write ip and port to file
# info = {'server_ip': server_ip, 'server_port': server_port}
# with open('info.json', 'w') as f:
#     json.dump(info, f)


# set up API to get ip and port
app = Flask(__name__)
@app.route('/api/info', methods=['GET'])
def get_info():
    reponse = {'server_ip': server_ip, 'server_port': server_port}
    return jsonify(reponse)


connections = {}

while True:
    print('waiting for client to check in...')

    key, client1 = sock.recvfrom(1024)
    key = key.decode()

    print(f'connection from: {client1}')

    sock.sendto(b'ready', client1)


    # we have a peer to connect with
    if key in connections:
        print('sending peer info to client')
        # get infor for both clients
        addr1, port1 = client1
        client2 = connections.pop(key)
        addr2, port2 = client2
        # send info to both clients to connect
        # sock.sendto(f'{addr1} {port1} {server_port}'.encode(), client2)
        # sock.sendto(f'{addr2} {port2} {server_port}'.encode(), client1)
        sock.sendto(f'{addr1} {port1} {50002}'.encode(), client2)
        sock.sendto(f'{addr2} {port2} {50002}'.encode(), client1)
    # client1 is the first to enter a given key
    else:
        connections[key] = client1