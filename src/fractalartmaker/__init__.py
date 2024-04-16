import turtle, math, random, functools

turtle.tracer(50000, 0) # Increase the first argument to speed up the drawing.
turtle.hideturtle()


def std_fam_args(func):
    """A decorator that adds the standard fractalartmaker arguments to drawing functions: pen, fill, colors, skip, jiggle, int"""
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        size = args[0]
        depth = args[1]

        # kwargs include pen, fill, colors, skip, jiggle, int, pensize
        
        if 'skip' in kwargs and random.random() < kwargs['skip']:
            return

        # Set pen size, if specified:
        if 'pensize' in kwargs:
            original_pen_size = turtle.pensize()
            turtle.pensize(kwargs['pensize'])

        # Set the pen and fill color, if specified
        if 'colors' in kwargs:
            original_pen = turtle.pencolor()
            original_fill = turtle.fillcolor()
            i = depth % len(kwargs['colors'])
            turtle.pencolor(kwargs['colors'][i][0])
            turtle.fillcolor(kwargs['colors'][i][1])
        else:
            if 'pen' in kwargs:
                original_pen = turtle.pencolor()
                turtle.pencolor(kwargs['pen'])
            if 'fill' in kwargs:
                original_fill = turtle.fillcolor()
                turtle.fillcolor(kwargs['fill'])

        if 'jiggle' in kwargs:
            turtle.penup()
            turtle.forward(random.random() * (size * kwargs['jiggle'] * 2) - (size * kwargs['jiggle']))
            turtle.left(90)
            turtle.forward(random.random() * (size * kwargs['jiggle'] * 2) - (size * kwargs['jiggle']))
            turtle.right(90)
            origx, origy = turtle.pos()
            turtle.pendown()

        if 'int' in kwargs and kwargs['int']:
            args[0] = int(args[0])  # Make `size` an int instead of a float.

        # Call the drawing function:
        return_value = func(*args, **kwargs)

        if 'jiggle' in kwargs:
            # go back to original point
            turtle.penup()
            turtle.goto(origx, origy)
            turtle.pendown()
        
        # Restore the original pen and fill color, if specified
        if 'colors' in kwargs:
            turtle.pencolor(original_pen)
            turtle.fillcolor(original_fill)
        if 'pen' in kwargs:
            turtle.pencolor(original_pen)
        if 'fill' in kwargs:
            turtle.fillcolor(original_fill)
        if 'pensize' in kwargs:
            turtle.pensize(original_pen_size)

        return return_value
    return wrapper_decorator


@std_fam_args
def square(size, depth, **kwargs):
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


@std_fam_args
def triangle(size, depth, **kwargs):
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
    if _depth > max_depth or size < 1:
        return  # BASE CASE

    if _depth == 0 and reset:
        turtle.reset()

    # Save the position and heading at the start of this function call:
    initialX = turtle.xcor()
    initialY = turtle.ycor()
    initialHeading = turtle.heading()

    # Call the draw function to draw the shape:
    turtle.pendown()
    shape_drawing_function(size, _depth, **kwargs)
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
        draw_fractal(shape_drawing_function, size * sizeCh, specs, max_depth,
        _depth + 1, **kwargs)

def draw_random(shape_drawing_function=None, size=None, max_depth=None, seed=None, **kwargs):
    """TODO: Currently this doesn't draw anything interesting and needs more tweaking."""
    if shape_drawing_function is None:
        shape_drawing_function = random.choice((square, triangle))
    if size is None:
        size = random.random() * 50 + 50
    if max_depth is None:
        max_depth = random.randint(3, 6)
    if seed is not None:
        random.seed = seed

    specs = []

    for i in range(random.randint(1, 5)):
        specs.append({'size': random.random() * 1 + 0.5,
                      'x': random.random() * 1 + 0.5,
                      'y': random.random() * 1 + 0.5,
                      'angle': random.random() * 360})

    draw_fractal(shape_drawing_function, size, specs, max_depth)

    return specs

def reset():
    turtle.reset()

def hideturtle():
    turtle.hideturtle()

def showturtle():
    turtle.showturtle()



def demo_four_corners(size=350, max_depth=5, **kwargs):
    # Four Corners:
    if 'colors' not in kwargs:
        kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
    draw_fractal(square, size,
        [{'size': 0.5, 'x': -0.5, 'y': 0.5},
         {'size': 0.5, 'x': 0.5, 'y': 0.5},
         {'size': 0.5, 'x': -0.5, 'y': -0.5},
         {'size': 0.5, 'x': 0.5, 'y': -0.5}], max_depth=max_depth, **kwargs)


def demo_spiral_squares(size=600, max_depth=50, **kwargs):
    # Spiral Squares:
    if 'colors' not in kwargs:
        kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
    draw_fractal(square, size, [{'size': 0.95,
        'angle': 7}], max_depth=max_depth, **kwargs)


def demo_double_spiral_squares(size=600, **kwargs):
    # Double Spiral Squares:
    if 'colors' not in kwargs:
        kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
    draw_fractal(square, 600,
        [{'size': 0.8, 'y': 0.1, 'angle': -10},
         {'size': 0.8, 'y': -0.1, 'angle': 10}], **kwargs)


def demo_triangle_spiral(size=20, max_depth=80, **kwargs):
    # Triangle Spiral:
    draw_fractal(triangle, size,
        [{'size': 1.05, 'angle': 7}], max_depth=max_depth, **kwargs)


def demo_glider(size=600, **kwargs):
    # Conway's Game of Life Glider:
    if 'colors' not in kwargs:
        kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
    third = 1 / 3
    draw_fractal(square, 600,
        [{'size': third, 'y': third},
         {'size': third, 'x': third},
         {'size': third, 'x': third, 'y': -third},
         {'size': third, 'y': -third},
         {'size': third, 'x': -third, 'y': -third}], **kwargs)


def demo_sierpinski_triangle(size=600, **kwargs):
    # Sierpinski Triangle:
    toMid = math.sqrt(3) / 6
    draw_fractal(triangle, 600,
        [{'size': 0.5, 'y': toMid, 'angle': 0},
         {'size': 0.5, 'y': toMid, 'angle': 120},
         {'size': 0.5, 'y': toMid, 'angle': 240}], **kwargs)


def demo_wave(size=280, **kwargs):
    # Wave:
    draw_fractal(triangle, size,
        [{'size': 0.5, 'x': -0.5, 'y': 0.5},
         {'size': 0.3, 'x': 0.5, 'y': 0.5},
         {'size': 0.5, 'y': -0.7, 'angle': 15}], **kwargs)


def demo_horn(size=100, max_depth=100, **kwargs):
    # Horn:
    if 'colors' not in kwargs:
        kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
    draw_fractal(square, size,
        [{'size': 0.96, 'y': 0.5, 'angle': 11}], max_depth=max_depth, **kwargs)


def demo_snowflake(size=200, **kwargs):
    # Snowflake:
    if 'colors' not in kwargs:
        kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
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


