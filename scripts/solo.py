"""
Projet minimal A1 - CSI/BIOST - 2024 - Brest/Caen/Nantes
agar.io like implementation, with turtle.
"""

import random, turtle, time, sys
from math import cos, sin
size = 20 # Taille d'une tortue

def square(width: int, height: int) -> None:
    """
    Create a square with the given width and height.
    :param width:
    :param height:
    :return:
    """
    tt_square = turtle.Turtle()
    tt_square.color('black')
    tt_square.penup()
    tt_square.goto(-width/2, -height/2)
    tt_square.pendown()
    tt_square.goto(width/2, -height/2)
    tt_square.goto(width/2, height/2)
    tt_square.goto(-width/2, height/2)
    tt_square.goto(-width/2, -height/2)
    tt_square.hideturtle()


def move(tort: turtle.Turtle, speed: float) -> None:
    """
    Moves forword the turtle by *speed* pixels on the screen.
    :param tort:
    :param speed:
    :return: None
    """
    tort.forward(speed)


def turtle_to_radius(tort: turtle.Turtle) -> int:
    """
    Returns turtle's radius in pixels.
    :param tort: Turtle object
    :return: Turtle's radius
    """
    return int(10 * tort.turtlesize()[0])


def size_to_scale(pixel: int) -> float:
    """
    Returns scale from size in pixels
    :param pixel: Size in pixels
    :return: Scale (x times 20 px)
    """
    global size
    return pixel / size


def bounce(tort: turtle.Turtle, width: int, height: int, player_turtle: turtle.Turtle) -> None:
    """
    Checks if turtle can bounce and chances it's parameters accordingly.
    :param tort: Turtle object
    :param width: Window width in pixels
    :param height: Windows height in pixels
    :return:
    """
    pos = tort.pos()
    alpha = tort.heading()
    radius = turtle_to_radius(tort)
    newpos = (pos[0], pos[1])
    delta = alpha
    # If X pos is equal or over half of the screen width.
    if pos[0] > width / 2 - radius:
        delta = 180 - alpha
        newpos = (width / 2 - radius, newpos[1])
    # If X pos is equal or over minus half of the screen width.
    if pos[0] < (- width / 2) + radius:
        delta = 180 - alpha
        newpos = (- width / 2 + radius, newpos[1])
    # If Y pos is equal or over half of the screen height.
    if pos[1] > height / 2 - radius:
        delta = - alpha
        newpos = (newpos[0], height / 2 - radius)
    # If Y pos is equal or over minus half of the screen height.
    if pos[1] < - (height / 2) + radius:
        delta = - alpha
        newpos = (newpos[0], - height / 2 + radius)
    if tort != player_turtle:
        tort.setheading(delta)
    tort.goto(newpos)


def eat(tort: turtle.Turtle, TList: list, foodlist: list) -> list:
    """
    Checks and eat turtle whenever possible.
    :param tort: Turtle object
    :param TList: List of turtle objects
    :return: Resfreshed list of turtle objects
    """
    # Getting parameters from the turtle.
    pos = tort.pos()
    radius = turtle_to_radius(tort)
    size = tort.turtlesize()
    for selectedIndex in range(len(TList)): # Loop for each turtle
        try:
            selectedTort = TList[selectedIndex]
            if selectedTort != tort: # Avoid the turtle from eating itself
                pos_selectedTort = selectedTort.pos()
                selectedSize = selectedTort.turtlesize()
                distance = ((pos[0] - pos_selectedTort[0])** 2 + (pos[1] - pos_selectedTort[1]) ** 2) ** (1/2)
                if distance <= radius and size[0] > selectedSize[0]:
                    selectedTort.hideturtle()
                    TList.pop(selectedIndex)
                    tort.turtlesize(size[0] + selectedSize[0] / 5)
        except IndexError:
            pass
    for selectedIndex in range(len(foodlist)): # Loop for each turtle
        try:
            selectedfood = foodlist[selectedIndex]
            pos_selectedfood = selectedfood.pos()
            distance = ((pos[0] - pos_selectedfood[0])** 2 + (pos[1] - pos_selectedfood[1]) ** 2) ** (1/2)
            if distance <= radius:
                selectedfood.hideturtle()
                foodlist.pop(selectedIndex)
                tort.turtlesize(size[0] + 0.2)
        except IndexError:
            pass
    return TList, foodlist


def createfood(foodlist: list, width: int, height: int) -> list:
    """
    Create static food turtles.
    :param n: Number of turtles
    :param side: Side length
    """
    if random.randint(0, 300) == 1:
        # Add turtle to list of all turtles, second argument is turtle's speed
        # here speed = 0 because it's stationary food
        tortx = random.randint(int(-width / 2) + 10, int(width / 2) - 10)  # Creates random X position based on width.
        torty = random.randint(int(-height / 2) + 10, int(height / 2) - 10)  # Creates random Y position based on height.
        temp_turtle = turtle.Turtle()  # Every turtle has 3 parameters: turtle object, speed,
        # exact coordinates
        # Turtle customization
        temp_turtle.pu()
        temp_turtle.shape("circle")
        temp_turtle.fillcolor("orange")  # turtle color
        temp_turtle.goto(tortx, torty)
        # Randomize initial parameters
        temp_turtle.turtlesize(0.6)  # Change turtle's size randomly between 0.5 and 2.
        foodlist.append(temp_turtle)
    return foodlist


def hunt(tort, TortList: list, foodlist: list, player_turt: turtle.Turtle) -> None:
    """
    Les plus grosses tortues sont attirées vers les plus petites
    """
    # Récuperation de la position et de la taille de la bulle mangeuse
    pos = tort.pos()
    size = tort.turtlesize()[0]
    param = float()
    # Comparaison avec toutes les autres bulles
    if tort != player_turt:
        if size > 2:
            for selected_tort in TortList:
                if tort != selected_tort:
                    # Récuperation de la position et de la taille d'une bulle
                    pos_selected = selected_tort.pos()
                    selected_size = selected_tort.turtlesize()[0]
                    # Distance entre les deux bulles
                    distance = ((pos[0] - pos_selected[0]) ** 2 + (pos[1] - pos_selected[1]) ** 2) ** (1 / 2)

                    # hunts prey if it's in the hunting zone
                    # if distance < 200:
                    if size >= selected_size:
                        # Calculer le vecteur de direction
                        param = tort.towards(pos_selected)
                        tort.setheading(param)
                    '''if size < selected_size:
                        param = 180 + tort.towards(pos_selected)'''

        else:
            for selected_food in foodlist:
                pos_selected = selected_food.pos()
                selected_size = selected_food.turtlesize()[0]
                # Distance entre les deux bulles
                distance = ((pos[0] - pos_selected[0]) ** 2 + (pos[1] - pos_selected[1]) ** 2) ** (1 / 2)
                if distance < 100:
                    if size >= selected_size:
                        # Calculer le vecteur de direction
                        param = tort.towards(pos_selected)
                        tort.setheading(param)


def follow_cursor(tort: turtle.Turtle) -> None:
    # Heads turtle towards player's cursor
    canvas = turtle.getcanvas()
    cursX, cursY = canvas.winfo_pointerx() - canvas.winfo_screenwidth() // 2, int(canvas.winfo_screenheight() // 2) - canvas.winfo_pointery()
    pos = tort.pos()
    angle = tort.towards(cursX, cursY)
    tort.setheading(angle)


def createplayer(side: int) -> turtle.Turtle:
    p_turt = turtle.Turtle()
    # Turtle customization
    p_turt.shape("circle")
    p_turt.color("black")  # turtle color
    # Randomize initial parameters
    p_turt.turtlesize(random.randint(8, 12) / 10)  # Change turtle's size randomly between 0.5 and 2.
    tortx = random.randint(int(-side / 2), int(side / 2))  # Creates random X position based on width.
    torty = random.randint(int(-side / 2), int(side / 2))  # Creates random Y position based on height.
    p_turt.up()  # Pen up
    p_turt.goto(tortx, torty)
    return p_turt


def main(n: int):
    """
    Creates the turtle window and all the components needed to set up the game and make the turtles behave.
    :param width: Window width in pixels
    :param height: Window height in pixels
    :return: None
    """
    # Set up the game window
    window = turtle.Screen()
    window.title("Projet minimal A1 2024")
    window.setup(width=1.0, height=1.0)
    # Remove close, minimize, maximize buttons:
    canvas = window.getcanvas()
    width = canvas.winfo_screenwidth() * 0.95
    height = canvas.winfo_screenheight() * 0.95
    root = canvas.winfo_toplevel()
    root.overrideredirect(True)
    window.tracer(0)
    window.colormode(255)
    square(width, height)
    player_turt = createplayer(width)
    TortList = []
    for tortIndex in range(n):
        TortList.append(turtle.Turtle()) # Add turtle to list of all turtles
        tort = TortList[tortIndex]
        # Turtle customization
        tort.shape("circle")
        tort.pencolor('black')  # border color
        tort.fillcolor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # turtle color
        # Randomize initial parameters
        tort.turtlesize(random.randint(5, 20) / 10) # Change turtle's size randomly between 0.5 and 2.
        tort.up()  # Pen up
        tortX = random.randint(int(-width / 2), int(width / 2)) # Creates random X position based on width.
        tortY = random.randint(int(-height / 2), int(height / 2)) # Creates random Y position based on height.
        tort.goto(tortX, tortY)
        tort.setheading(random.randint(0, 359))
        # tort.pd()
    foodlist = []
    TortList.append(player_turt)
    while len(TortList) > 1:
        window.update()  # Dislplay refresh
        follow_cursor(player_turt)
        for tort in TortList: # Loop for each turtle
            #flee(tort, TortList)
            foodlist = createfood(foodlist, width, height)
            move(tort, 3)  # Move turtle
            hunt(tort, TortList, foodlist, player_turt)
            bounce(tort, width, height, player_turt)
            TortList, foodlist = eat(tort, TortList, foodlist)
        time.sleep(0.017)  # delays display refresh, here, 17ms / 60fps
    endgame = turtle.Turtle()
    endgame.hideturtle()
    endgame.penup()
    endgame.color("red")
    endgame.write("GAME OVER", font=("Arial", 50, "bold"), align="center")
    endgame.goto(0, -40)
    if player_turt in TortList:
        endgame.color("green")
        endgame.write("YOU WON", font=("Arial", 30, "bold"), align="center")
    else:
        endgame.write("YOU LOSE", font=("Arial", 30, "bold"), align="center")
    window.update()
    time.sleep(1)
    turtle.exitonclick()


if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 800
    # Run the game
