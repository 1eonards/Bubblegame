# -------------IMPORT LIBRARIES--------------------
import socket
import threading
import time
import random
import uuid
import json
from math import cos, sin

# -------------VARIABLES----------------------------
IP = "0.0.0.0"
PORT = 6789

users = {}  # User dictionary
food = {}  # Food dictionary
users_info = {}  # User IP and socket dictionary
running = False

speed = 0.5  # Players speed
game_side = 2000  # Border length
half_game_side = game_side / 2
turtle_radius = 10  # Turtle size for size = 1

print("Starting server\n")
connex = 0  # Connection counter

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Assigning an IP and a listening port
print("ok.")

refresh_period = 0.001


# -----------MAIN-----------------------------------


def start():
    """
    Starts listening to incoming connections.
    :return:
    """
    global connex, running
    running = True
    thread_update_positions.start()
    thread_eat.start()
    thread_food.start()
    while True:
        connex += 1
        try:
            sock.bind((IP, PORT))
        except OSError:
            pass
        try:
            sock.listen(20)
        except OSError:
            pass
        print(f"Listening on {IP} on port {PORT}")
        user_socket, user_ip = sock.accept()
        print(f"IP {user_ip} accepted.")
        new_connection = threading.Thread(target=th_connection, args=(user_ip, user_socket), daemon=True)
        new_connection.start()


def receive_message(user_socket: socket.socket) -> list:
    """
    Receive message from connected client then returns the content in a list.
    :param user_socket:
    :return:
    """
    recv = 0
    while recv == 0:
        try:
            recv = user_socket.recv(8192)
            recv = recv.decode('utf8')
        except ConnectionResetError:
            return 0
        except ConnectionAbortedError:
            return 0
        try:
            recv = recv.split('::')
        except ValueError:
            recv = 0
            print(f"\nDecoding error.")
    return recv


def create_player() -> tuple:
    """
    Creates random parameters for the player then return it into a tuple.
    :return:
    """
    user_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Player's color
    # Randomize initial parameters
    user_size = random.randint(10, 20) / 10  # Randomly choose a size between 0.8 and 1.2.
    user_x = random.randint(int(-game_side / 2), int(game_side / 2))  # Creates random X position based on side length.
    user_y = random.randint(int(-game_side / 2), int(game_side / 2))  # Creates random Y position based on side length.
    return user_x, user_y, user_size, user_color


def send_player(mess_type: str, message: str, user_socket: socket.socket, user_id: str) -> None:
    global users
    """
    Sends a formatted message to a socket
    :param mess_type:
    :param message:
    :param user_socket:
    :return:
    """
    try:
        temp_message = f'{mess_type}::{message}'
        user_socket.send(bytes(temp_message, 'utf8'))
    except ConnectionAbortedError:
        del users[user_id]


def th_connection(user_ip: str, user_socket: socket.socket) -> None:
    """
    Thread for each connected players
    :param user_ip:
    :param user_socket:
    :return:
    """
    received = receive_message(user_socket)
    user_name = received[1]
    print(user_name)
    user_id = str(uuid.uuid1())
    user_x, user_y, user_size, user_color = create_player()
    temp_message = f"{user_id}::{user_name}::{user_x}::{user_y}::{user_size}::{user_color[0]}::{user_color[1]}::{user_color[2]}::{game_side}"
    send_player("success", temp_message, user_socket, user_id)
    user_heading = 0
    user_kills = 0
    users[user_id] = {
        "name": user_name,
        "x": user_x,
        "y": user_y,
        "size": user_size,
        "color": user_color,
        "heading": user_heading,
        "kills": user_kills
    }
    users_info[user_id] = {"ip": user_ip, "socket": user_socket}
    time.sleep(refresh_period)
    while user_id in users:
        dumped_users = json.dumps(users)
        dumped_food = json.dumps(food)
        # dumped_food = {}
        user_size = users[user_id]["size"]
        send_player("game", f"{users[user_id]["x"]}::{users[user_id]["y"]}::{user_size}::{user_kills}::{dumped_users}::{dumped_food}", user_socket, user_id)
        received = receive_message(user_socket)
        if received != 0:
            try:
                user_heading = float(received[1])
                users[user_id]["heading"] = user_heading
            except KeyError:
                send_player("lose", "disconnect", user_socket, user_id)
            except IndexError:
                user_heading = 0
        else:
            print(f"Player {users_info[user_id]["ip"]} | {users[user_id]["name"]} disconnected.]")
            del users[user_id]
        time.sleep(refresh_period)


def th_update_positions() -> None:
    """
    Updating position of all players
    :return:
    """
    global speed, users
    while running:
        for selected in users:
            # Determines player's next position
            angle = users[selected]["heading"]
            user_radius = int(users[selected]["size"] * turtle_radius)
            delta_x = speed * cos(angle)
            delta_y = speed * sin(angle)
            users[selected]["x"] += delta_x
            users[selected]["y"] += delta_y
            # Checking if player hits the border
            if users[selected]["x"] > half_game_side - user_radius - 21:
                users[selected]["x"] = float(half_game_side - user_radius - 21)
            # If X pos is equal or over minus half of the screen width.
            elif users[selected]["x"] < (- half_game_side) + user_radius + 21:
                users[selected]["x"] = float(- half_game_side + user_radius + 21)
            # If Y pos is equal or over half of the screen height.
            if users[selected]["y"] > half_game_side - user_radius - 21:
                users[selected]["y"] = float(half_game_side - user_radius - 21)
            # If Y pos is equal or over minus half of the screen height.
            if users[selected]["y"] < - half_game_side + user_radius + 21:
                users[selected]["y"] = float(- half_game_side + user_radius + 21)
        time.sleep(refresh_period)


def th_create_food() -> None:
    """
    Create static food.
    """
    global food, running
    while running:
        if len(food) < 10:
            food_x = random.randint(int(-half_game_side + 10), int(half_game_side - 10))  # Creates random X position based on width.
            food_y = random.randint(int(-half_game_side + 10), int(half_game_side - 10))  # Creates random Y position based on height.
            food[str(uuid.uuid1())] = (food_x, food_y)
        time.sleep(0.5)


def th_eat() -> None:
    """
    Checks and eat turtle whenever possible.
    :return:
    """
    # Getting parameters from the player.
    global users
    while running:
        del_list = []
        for selected in users:
            user_x, user_y = users[selected]["x"], users[selected]["y"]
            user_radius = int(users[selected]["size"] * turtle_radius)
            user_size = users[selected]["size"]
            for selected_secondary in users:  # Loop for each turtle
                try:
                    if selected != selected_secondary:  # Avoid the player from eating itself
                        selected_x, selected_y = users[selected_secondary]["x"], users[selected_secondary]["y"]
                        selected_size = users[selected_secondary]["size"]
                        delta_x = (user_x - selected_x)
                        delta_y = (user_y - selected_y)
                        distance = (delta_x ** 2 + delta_y ** 2) ** (1/2)
                        if distance <= user_radius and user_size > selected_size:
                            users[selected]["size"] += users[selected_secondary]["size"] / 6
                            users[selected]["kills"] += 1
                            del_list.append(selected_secondary)
                except KeyError:
                    pass
            del_flist = []
            for selected_secondary in food:
                try:
                    selected_x, selected_y = food[selected_secondary][0], food[selected_secondary][1]
                    delta_x = (user_x - selected_x)
                    delta_y = (user_y - selected_y)
                    distance = (delta_x ** 2 + delta_y ** 2) ** (1/2)
                    if distance <= user_radius:
                        users[selected]["size"] += 0.1
                        del_flist.append(selected_secondary)
                except KeyError:
                    pass
            for selected_del in del_flist:
                del food[selected_del]
        for selected_del in del_list:
            del users[selected_del]
        time.sleep(0.03)


thread_update_positions = threading.Thread(target=th_update_positions, daemon=True)
thread_eat = threading.Thread(target=th_eat, daemon=True)
thread_food = threading.Thread(target=th_create_food, daemon=True)
start()
