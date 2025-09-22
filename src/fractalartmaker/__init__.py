import turtle, math, random, functools, copy
from turtle import forward, backward, left, right, position, heading, goto, setx, sety, towards, setheading, penup, pendown, pensize, width, pencolor, fillcolor, begin_fill, end_fill, home, clear, reset, hideturtle, showturtle, bgcolor, tracer, exitonclick, done, fd, bk, lt, rt, pos, pd, pu, update

__version__ = '0.3.0'
__all__ = ['draw_fractal', 'square', 'triangle', 'demo_four_corners', 'demo_spiral_squares', 'demo_double_spiral_squares', 'demo_triangle_spiral', 'demo_glider', 'demo_sierpinski_triangle', 'demo_wave', 'demo_horn', 'demo_snowflake', 'forward', 'backward', 'left', 'right', 'position', 'heading', 'goto', 'setx', 'sety', 'towards', 'setheading', 'penup', 'pendown', 'pensize', 'width', 'pencolor', 'fillcolor', 'begin_fill', 'end_fill', 'home', 'clear', 'reset', 'hideturtle', 'showturtle', 'bgcolor', 'tracer', 'exitonclick', 'done', 'fd', 'bk', 'lt', 'rt', 'pos', 'pd', 'pu', 'update']

turtle.tracer(50000, 0) # Increase the first argument to speed up the drawing.
turtle.hideturtle()



def square(size, **kwargs):
    # Move to the top-right corner before drawing:
    turtle.penup()
    turtle.forward(size // 2)
    turtle.left(90)
    turtle.forward(size // 2)
    turtle.left(180)
    turtle.pendown()

    # Draw a square:
    if 'fill' in kwargs or 'colors' in kwargs:
        turtle.begin_fill()
    for i in range(4):  # Draw four lines.
        turtle.forward(size)
        turtle.right(90)
    if 'fill' in kwargs or 'colors' in kwargs:
        turtle.end_fill()


def triangle(size, **kwargs):
    # Move the turtle to the top of the equilateral triangle:
    height = size * math.sqrt(3) / 2
    turtle.penup()
    turtle.left(90)  # Turn to face upwards.
    turtle.forward(height * (2/3))  # Move to the top corner.
    turtle.right(150)  # Turn to face the bottom-right corner.
    turtle.pendown()

    # Draw the three sides of the triangle:
    for i in range(3):
        turtle.forward(size)
        turtle.right(120)


def draw_fractal(shape_drawing_function, size, specs, max_depth=8, _depth=0, reset=True, **kwargs):
    # BASE CASE
    if _depth > max_depth or size < 1:
        return  

    if _depth == 0 and reset:
        turtle.reset()

    # Mirror _depth in the kwargs dictionary. This is so it's available to
    # the drawing functions, but we need to update it at each recursive depth level.
    kwargs['depth'] = _depth

    # Save the position and heading at the start of this function call:
    initialX = turtle.xcor()
    initialY = turtle.ycor()
    initialHeading = turtle.heading()

    # Call the draw function to draw the shape:
    turtle.pendown()
    for kwarg in list(kwargs.keys()):
        if kwarg not in shape_drawing_function.__code__.co_varnames:
            del kwargs[kwarg]
    shape_drawing_function(size, **kwargs)
    turtle.penup()

    # RECURSIVE CASE
    for spec in specs:
        # Each dictionary in specs has keys 'size', 'x',
        # 'y', and 'angle'. The size, x, and y changes
        # are multiplied by the size parameter. The x change and y
        # change are added to the turtle's current position. The angle
        # change is added to the turtle's current heading.
        sizeCh = spec.get('size', 1.0)
        xCh = spec.get('x', 0.0)
        yCh = spec.get('y', 0.0)
        angleCh = spec.get('angle', 0.0)

        # Reset the turtle to the shape's starting point:
        turtle.goto(initialX, initialY)
        turtle.setheading(initialHeading + angleCh)
        turtle.forward(size * xCh)
        turtle.left(90)
        turtle.forward(size * yCh)
        turtle.right(90)

        # Make the recursive call:
        draw_fractal(shape_drawing_function, size * sizeCh, specs, max_depth, _depth + 1,
            **kwargs)



def demo_four_corners(size=350, max_depth=5, **kwargs):
    # Four Corners:
    kwargs.setdefault('colors', (('black', 'white'), ('black', 'gray')))
    draw_fractal(square, size,
        [{'size': 0.5, 'x': -0.5, 'y': 0.5},
         {'size': 0.5, 'x': 0.5, 'y': 0.5},
         {'size': 0.5, 'x': -0.5, 'y': -0.5},
         {'size': 0.5, 'x': 0.5, 'y': -0.5}], max_depth=max_depth, **kwargs)


def demo_spiral_squares(size=600, max_depth=50, **kwargs):
    # Spiral Squares:
    kwargs.setdefault('colors', (('black', 'white'), ('black', 'gray')))
    draw_fractal(square, size, [{'size': 0.95,
        'angle': 7}], max_depth=max_depth, **kwargs)


def demo_double_spiral_squares(size=600, **kwargs):
    # Double Spiral Squares:
    kwargs.setdefault('colors', (('black', 'white'), ('black', 'gray')))
    draw_fractal(square, 600,
        [{'size': 0.8, 'y': 0.1, 'angle': -10},
         {'size': 0.8, 'y': -0.1, 'angle': 10}], **kwargs)


def demo_triangle_spiral(size=20, max_depth=80, **kwargs):
    # Triangle Spiral:
    draw_fractal(triangle, size,
        [{'size': 1.05, 'angle': 7}], max_depth=max_depth, **kwargs)


def demo_glider(size=600, **kwargs):
    # Conway's Game of Life Glider:
    kwargs.setdefault('colors', (('black', 'white'), ('black', 'gray')))
    draw_fractal(square, 600,
        [{'size': 1 / 3, 'y': 1 / 3},
         {'size': 1 / 3, 'x': 1 / 3},
         {'size': 1 / 3, 'x': 1 / 3, 'y': -1 / 3},
         {'size': 1 / 3, 'y': -1 / 3},
         {'size': 1 / 3, 'x': -1 / 3, 'y': -1 / 3}], **kwargs)


def demo_sierpinski_triangle(size=600, **kwargs):
    # Sierpinski Triangle:
    draw_fractal(triangle, 600,
        [{'size': 0.5, 'y': math.sqrt(3) / 6, 'angle': 0},
         {'size': 0.5, 'y': math.sqrt(3) / 6, 'angle': 120},
         {'size': 0.5, 'y': math.sqrt(3) / 6, 'angle': 240}], **kwargs)


def demo_wave(size=280, **kwargs):
    # Wave:
    draw_fractal(triangle, size,
        [{'size': 0.5, 'x': -0.5, 'y': 0.5},
         {'size': 0.3, 'x': 0.5, 'y': 0.5},
         {'size': 0.5, 'y': -0.7, 'angle': 15}], **kwargs)


def demo_horn(size=100, max_depth=100, **kwargs):
    # Horn:
    kwargs.setdefault('colors', (('black', 'white'), ('black', 'gray')))
    draw_fractal(square, size,
        [{'size': 0.96, 'y': 0.5, 'angle': 11}], max_depth=max_depth, **kwargs)


def demo_snowflake(size=200, **kwargs):
    # Snowflake:
    kwargs.setdefault('colors', (('black', 'white'), ('black', 'gray')))
    draw_fractal(square, size,
        [{'x': math.cos(0 * math.pi / 180),
          'y': math.sin(0 * math.pi / 180), 'size': 0.4},
         {'x': math.cos(72 * math.pi / 180),
          'y': math.sin(72 * math.pi / 180), 'size': 0.4},
         {'x': math.cos(144 * math.pi / 180),
          'y': math.sin(144 * math.pi / 180), 'size': 0.4},
         {'x': math.cos(216 * math.pi / 180),
          'y': math.sin(216 * math.pi / 180), 'size': 0.4},
         {'x': math.cos(288 * math.pi / 180),
          'y': math.sin(288 * math.pi / 180), 'size': 0.4}], **kwargs)
