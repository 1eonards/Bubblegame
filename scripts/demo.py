"""
Projet minimal A1 - CSI/BIOST - 2024 - Brest/Caen/Nantes
agar.io like implementation, with turtle.
"""

import random, turtle, time, sys

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


def bounce(tort: turtle.Turtle, width: int, height: int) -> None:
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
    tort.setheading(delta)
    tort.goto(newpos)


def eat(tort: turtle.Turtle, TList: list) -> list:
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
    return TList


def main(n: int, width: int, height: int):
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
    root = canvas.winfo_toplevel()
    root.overrideredirect(True)
    window.tracer(0)
    window.colormode(255)
    square(width, height)
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
    while len(TortList) > 1:
        window.update()  # Dislplay refresh
        for tort in TortList: # Loop for each turtle
            move(tort, 10) # Move turtle
            bounce(tort, width, height)
            TortList = eat(tort, TortList)
        time.sleep(0.017)  # delays display refresh, here, 17ms / 60fps
    sys.exit("Il ne reste plus qu'une tortue")


if __name__ == "__main__":
    WIDTH, HEIGHT = 1200, 900
    # Run the game