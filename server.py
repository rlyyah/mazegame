import socket
import threading
import pickle
import game
import time
import helpers

HOST = '127.0.0.1'
PORT = 13337
ADDR = (HOST, PORT)
HEADER_LENGHT = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f'New connection from: {addr}')
    map_width = 10
    map_height = 10
    player_vision = 5
    g = create_game_object(map_width, map_height, player_vision)
    send_initial_data_to_user(conn, g)
    
    client_connected = True
    while client_connected:
        if not g.restart_game:
            (message, bb) = receive_message_from_client(conn, g)
            if bb:
                break
            send_message_to_client(conn, message)
            helpers.clear_screen()
            g.display_map()
            print('\n')
        else:
            map_width += 5
            map_height += 5
            g = create_game_object(map_width, map_height, player_vision)
            send_initial_data_to_user(conn, g)
    print(f'closing connection with {addr}')
    conn.close()

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        print(f'Connections count: {threading.activeCount() - 1}')

def create_game_object(width, height, player_vision):
    g = game.Game(width, height, player_vision)
    g.prepare_game()
    return g

def send_initial_data_to_user(conn, g):
    # first walls msg
    (msg, msg_length, msg_type) = create_object_message(g.walls_positons, 1)
    time.sleep(0.01)
    conn.send(msg_length)
    time.sleep(0.01)
    conn.send(msg_type)
    time.sleep(0.01)
    conn.send(msg)
    #options message
    (msg, msg_length, msg_type) = create_object_message({
        'start':{'x': g.start_point.x, 'y': g.start_point.y},
        'finish':{'x': g.finish_point.x, 'y': g.finish_point.y}, 
        'player-options':{'player-vision': g.set_up_player.player_vision_length},
        'map-options':{'width': g.prepared_map.map_width, 'height': g.prepared_map.map_heigth}}, 2)
    time.sleep(0.01)
    conn.send(msg_length)
    time.sleep(0.01)
    conn.send(msg_type)
    time.sleep(0.01)
    conn.send(msg)
    time.sleep(0.01)


def create_message(msg, msg_type):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER_LENGHT - msg_length)
    send_type = str(msg_type).encode(FORMAT)
    send_type += b' ' * (HEADER_LENGHT - msg_length)
    return (message, send_length, send_type)

def create_object_message(object_msg, msg_type):
    message = pickle.dumps(object_msg)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER_LENGHT - msg_length)
    send_type = str(msg_type).encode(FORMAT)
    send_type += b' ' * (HEADER_LENGHT - msg_length)
    return (message, send_length, send_type)
    
def receive_message_from_client(client, g):
    player_move = client.recv(1).decode('utf-8')
    g.change_positon(player_move)
    if player_move == 'p':
        bb = True
    else:
        bb = False
    return (g.read_new_position(), bb)

def send_message_to_client(conn, new_position):
    (msg, msg_length, msg_type) = create_object_message({'x': new_position.x, 'y': new_position.y}, 3)
    conn.send(msg_length)
    time.sleep(0.01)
    conn.send(msg_type)
    time.sleep(0.01)
    conn.send(msg)

print('Server is up and running...')
start()