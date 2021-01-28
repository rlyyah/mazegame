import socket
import pickle
from collections import defaultdict
from model import Point
from game_displayer import handle_client_map
from helpers import clear_screen, key_pressed

HOST = '127.0.0.1'
PORT = 13337
ADDR = (HOST, PORT)
HEADER_LENGHT = 64

DISSCONECT_MSG = '!DISCONNECT'
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

walls_positions = defaultdict()

messages_types = {
    1: 'walls',
    2: 'options',
    3: 'new_position',
    4: 'restart_maze',
    5: 'disconnect'}

def listen_server():

    (walls_positions, options) = listen_to_initial_data()
    
    # create map object for the player
    hcm = handle_client_map(walls_positions, options)
    #display initial vision and wait for client move 
    hcm.handle_player_vision()
    connected = True
    while connected:
        if hcm.listen_to_input:
            if handle_user_input(client):
                break
        (message, msg_type) = handle_server_message(client)
        if msg_type == 3:
            hcm.update_position(message)
            hcm.handle_player_vision()
        elif msg_type == 1:
            walls_positions = message
            (message, msg_type) = handle_server_message(client)
            options = message
            hcm = handle_client_map(walls_positions, options)
            hcm.handle_player_vision()
    print(f'closing connection with the server')

def connect():
    client.connect(ADDR)
    listen_server()

def listen_to_initial_data():
    # recieve walls_game object from the server
    (walls_positions, msg_type) = handle_server_message(client)
    # recieve options object from the server
    (options, msg_type) = handle_server_message(client)
    return (walls_positions, options)

def handle_user_input(client):
    key = key_pressed()
    client.send(key.encode('utf-8'))
    if key == 'p':
        return True
    else: 
        return False

def handle_server_message(client):
    msg_length = client.recv(64).decode(FORMAT).strip()
    msg_type = client.recv(64).decode(FORMAT).strip()
    full_msg = b''
    if msg_length:
        msg_length = int(msg_length)
        while len(full_msg) < msg_length:
            packet = client.recv(msg_length - len(full_msg))
            if not packet:
                return None
            full_msg += packet
        message = pickle.loads(full_msg)
    return message, int(msg_type)


print("Conecting to the server...")
connect()