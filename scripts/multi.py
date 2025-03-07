import socket
import turtle
import time
import threading
import json
import sys
from math import radians


server_ip = 'localhost'
server_port = 6789
turtle_size = 20  # Size of a turtle
running = False
refresh_period = 0.01
background_image = "assets/multi-bg.gif"


users = {}
user_name = ""
user_id = ""
user_x = 0
user_y = 0
user_size = 1
user_color = (0, 0, 0)
game_side = 500
user_angle = 0

player_turtles = {}
food = {}


def connect_to_server() -> socket.socket:
    """
    Connects to the server and returns the socket object.
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    sock.settimeout(0.5)
    return sock


def send_server(mess_type: str, message: str, user_socket: socket.socket) -> None:
    """
    Sends a formatted message to a socket
    :param mess_type:
    :param message:
    :param user_socket:
    :return:
    """
    temp_message = f'{mess_type}::{message}'
    user_socket.send(bytes(temp_message, 'utf8'))


def receive_message(user_socket: socket.socket) -> list:
    """
    Receive message from connected server
    :param user_socket:
    :return:
    """
    recv = 0
    while recv == 0:
        recv = user_socket.recv(8192)
        recv = recv.decode('utf8')
        try:
            recv = recv.split('::')
        except ValueError:
            recv = 0
            print(f"\nDecoding error")
    return recv


def square_border(side: int) -> turtle.Turtle:
    """
    Create a square turtle.
    :param side: int
    :return:
    """
    square_turtle = turtle.Turtle()
    square_turtle.pu()
    square_turtle.fillcolor('white')
    square_turtle.pencolor((230, 243, 235))
    square_turtle.pensize(10)
    square_turtle.shape(background_image)
    square_turtle.turtlesize(side / 20)
    return square_turtle


def cursor_angle(player_turtle: turtle.Turtle) -> float:
    """
    Returns the cursor angle in degrees.
    :param player_turtle:
    :return:
    """
    curs_x = canvas.winfo_pointerx() - canvas.winfo_screenwidth() // 2
    curs_y = canvas.winfo_screenheight() // 2 - canvas.winfo_pointery()
    angle = player_turtle.towards(curs_x, curs_y)
    return radians(angle)


def game_setup(side: int):
    """
    Sets up the turtle environment.
    :param side:
    :return:
    """
    # Set up the game window
    game_window = turtle.Screen()
    game_window.title("AGR.IO")
    game_window.setup(width=1.0, height=1.0)
    game_window.colormode(255)
    game_window.bgcolor((247, 248, 250))
    turtle.register_shape(background_image)
    # Remove close, minimize, maximize buttons
    canvas = game_window.getcanvas()
    root = canvas.winfo_toplevel()
    root.overrideredirect(True)
    game_window.tracer(0)
    # Set up the border
    square_turtle = square_border(side)
    return game_window, square_turtle


def create_player(size: float, color: tuple[float, float, float]) -> turtle.Turtle:
    """
    Creates player's turtle with some parameters then return it.
    :param size:
    :param color:
    :return:
    """
    player_turtle = turtle.Turtle()
    # Turtle customization
    player_turtle.up()  # Pen up
    player_turtle.shape("circle")
    player_turtle.color(color)  # turtle color
    player_turtle.turtlesize(size)  # Change turtle's size randomly between 0.5 and 2.
    return player_turtle


def th_update_game(user_socket, n) -> None:
    """
    Receive and update the position of objects.
    :param user_socket:
    :param n:
    :return:
    """
    global users, user_x, user_y, user_size, running, user_angle, food, user_kills
    n += 1  # le threading avec argument se comporte étrangement lorsqu'il n'y a qu'un seul argument
    while running:
        try:
            received = receive_message(user_socket)
            if received[0] == "game":
                # print(received[3])
                user_x, user_y, user_size = float(received[1]), float(received[2]), float(received[3])
                # print(user_size)
                user_kills = int(received[4])
                users = json.loads(received[5])
                food = json.loads(received[6])
                send_server("hdg", str(user_angle), user_socket)
            elif received[0] == "lose":
                running = False
            time.sleep(refresh_period)
        except TimeoutError:
            running = False


def update_other_pos() -> None:
    """
    Updates position of other objects
    :return:
    """
    global user_x, user_y, user_id, player_turtles, users, food
    for selected in users:
        if selected != user_id:
            try:
                new_pos = (users[selected]["x"], users[selected]["y"])
                radius_text = player_turtles[selected]["turtle"].turtlesize()[0] * 10 / 1.4
                player_turtles[selected]["turtle"].goto(new_pos[0] - user_x + radius_text, new_pos[1] - user_y + radius_text)
                player_turtles[selected]["turtle"].clear()
                player_turtles[selected]["turtle"].write(player_turtles[selected]["name"])
                player_turtles[selected]["turtle"].goto(new_pos[0] - user_x, new_pos[1] - user_y)
                player_turtles[selected]["turtle"].turtlesize(users[selected]["size"])
            except KeyError:
                temp_turtle = turtle.Turtle()
                temp_turtle.up()
                temp_turtle.shape("circle")
                try:
                    temp_turtle.color(users[selected]["color"])
                    temp_turtle.turtlesize(users[selected]["size"])
                    temp_turtle.goto(users[selected]["x"], users[selected]["y"])
                    player_turtles[selected] = {"name": users[selected]["name"], "turtle": temp_turtle, "type": "player"}
                except KeyError:
                    pass
    for selected in food:
        try:
            new_pos = (food[selected][0], food[selected][1])
            player_turtles[selected]["turtle"].goto(new_pos[0] - user_x, new_pos[1] - user_y)
        except KeyError:
            temp_turtle = turtle.Turtle()
            temp_turtle.up()
            temp_turtle.shape("circle")
            temp_turtle.fillcolor("orange")  # turtle color
            temp_turtle.turtlesize(0.6)
            try:
                temp_turtle.goto(food[selected][0] - user_x, food[selected][1] - user_y)
            except KeyError:
                temp_turtle.hideturtle()
            player_turtles[selected] = {"name": "", "turtle": temp_turtle, "type": "food"}
    del_list = []
    for selected in player_turtles:
        if selected not in users and selected not in food:
            player_turtles[selected]["turtle"].hideturtle()
            player_turtles[selected]["turtle"].clear()
            time.sleep(0.01)
            del_list.append(str(selected))
    for selected in del_list:
        del player_turtles[selected]


def size_dict(dictionary):
    """
    Creates a dictionary with the player's name as key and score as value.
    :param dictionary:
    :return:
    """
    size_dictionary={}   #Création d'un dictionnaire
    for element in dictionary:
        size_dictionary[f"{users[element]["name"]}::{users[element]["kills"]}"] = round(users[element]["size"], 2)
        # Nous prendrons dans chaque element du dictionnaire le nom associé à username et la taille associé à size
        # Le nom associé à la clé username devient la clé du nouveau dictionaire et la taille est l'élément qui lui est associé
    return size_dictionary


def sort_dict(dictionary: dict):
    """
    Sorts dictionary by size
    :param dictionary:
    :return:
    """
    sorted_dictionary = {}
    for key in sorted(dictionary, key=dictionary.get, reverse=True):
        sorted_dictionary[key] = dictionary[key]
    """La fonction sorted sert à trier en fonction du score du plus grand au plus petit"""
    return sorted_dictionary


def display(score_dictionary: dict, scoreboard_turtle: turtle.Turtle) -> None:
    """
    Displays the score dictionary on top right of the screen.
    :param score_dictionary:
    :param scoreboard_turtle:
    :return:
    """
    global canvas, users
    """Nous nous servirons de la liste triée puis nous afficher chaque clé avec son score"""
    n = 1
    scoreboard_turtle.clear()
    x, y = canvas.winfo_screenwidth()//2 * 0.97, canvas.winfo_screenheight() // 2 * 0.9
    scoreboard_turtle.goto(x, y)
    scoreboard_turtle.write("Classement", font=("Arial", 25, "bold"), align="right")
    for lines in score_dictionary:
        score = lines
        lines = lines.split("::")
        scoreboard_turtle.goto(x, y - n*60)
        score = f"{int(score_dictionary[score]*100)} points - {lines[0]}({lines[1]} kills)"
        scoreboard_turtle.write(score, font=("Arial", 18, "normal"), align="right")
        n = n + 1


def setup_scoreboard() -> turtle.Turtle:
    """
    Sets up the scoreboard turtle then returns it.
    :return: Scoreboard Turtle
    """
    scoreboard_turtle = turtle.Turtle()
    scoreboard_turtle.penup()
    scoreboard_turtle.hideturtle()
    return scoreboard_turtle


def display_score(users_dict: dict, scoreboard_turtle: turtle.Turtle) -> None:
    """
    Displays the score dictionary on top right of the screen.
    :param users_dict:
    :param scoreboard_turtle:
    :return:
    """
    size_dictionary = size_dict(users_dict)
    sorted_size_dictionary = sort_dict(size_dictionary)
    display(sorted_size_dictionary, scoreboard_turtle)


def play_loop(game_window, player_turtle: turtle.Turtle, square_turtle: turtle.Turtle, scoreboard_turtle: turtle.Turtle) -> None:
    """
    Loop when player is alive
    :param game_window:
    :param player_turtle:
    :param square_turtle:
    :param scoreboard_turtle:
    :return:
    """
    global users, user_x, user_y, user_size, running, user_angle
    while running:
        game_window.update()  # Display refresh
        user_angle = cursor_angle(player_turtle)  # Determines the angle from center of the screen to player cursor
        square_turtle.goto(- user_x, - user_y)
        player_turtle.turtlesize(user_size)
        update_other_pos()
        display_score(users, scoreboard_turtle)
        time.sleep(refresh_period)  # delays display refresh, here, 60ms ~ 20fps


def main(name: str) -> None:
    """
    Main loop of the game
    :return:
    """
    global user_id, user_name, user_x, user_y, user_size, user_color, game_side, user_angle, running, canvas
    user_socket = connect_to_server()
    user_name = name
    send_server("join", user_name.replace("::", ""), user_socket)
    received = receive_message(user_socket)
    while received[0] != "success":
        received = receive_message(user_socket)
    running = True
    user_id, user_name, game_side = received[1], received[2], int(received[9])
    user_x, user_y = float(received[3]), float(received[4])
    user_size, user_color = float(received[5]), (int(received[6]), int(received[7]), int(received[8]))
    game_window, square_turtle = game_setup(game_side)
    canvas = turtle.getcanvas()
    player_turtle = create_player(user_size, user_color)
    scoreboard_turtle = setup_scoreboard()
    thread_receive_game = threading.Thread(target=th_update_game, args=(user_socket, 1), daemon=True)
    thread_receive_game.start()
    play_loop(game_window, player_turtle, square_turtle, scoreboard_turtle)
    endgame = turtle.Turtle()
    endgame.hideturtle()
    endgame.penup()
    endgame.color("red")
    endgame.goto(0, 20)
    endgame.write("GAME OVER", font=("Arial", 150, "bold"), align="center")
    endgame.goto(0, -150)
    endgame.write("YOU DIED", font=("Arial", 100, "bold"), align="center")
    endgame.goto(0, -250)
    endgame.write("Left click to leave", font=("Courier", 30, "bold"), align="center")
    game_window.update()
    turtle.exitonclick()
    sys.exit("Game over.")
