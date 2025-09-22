# fractalartmaker
A module for creating fractal art in Python's turtle module.

Fractals are recursive, self-similar shapes. The `fractalartmaker` module (abbreviated as `fam`) lets you create fractals in Python's built-in `turtle` module. This module is based on the "Fractal Art Maker" chapter of my free book, [The Recursive Guide to Recursion](https://inventwithpython.com/recursion/).

Quickstart
===========

To install, run `pip install fractalartmaker` in the command line terminal. Run `python -m fractalartmaker` on Windows or `python3 -m fractalartmaker` on macOS to run the demo and view nine pieces of fractal art made by Al Sweigart.

First, you must know a little bit of Python programming and Python's `turtle` module. [RealPython.com has a `turtle` module tutorial.](https://realpython.com/beginners-guide-python-turtle/)

You can view a demo fractal by running the following code from the interactive shell (aka the REPL):

    >>> import fractalartmaker as fam
    >>> fam.demo_four_corners()

This draws the Four Corners fractal in a new turtle window.

The main function we'll use in the `fam` module is `fam.draw_fractal()`. We'll need to pass it a *drawing function*, which is a function that takes a `size` argument and draws a simple shape. Here's the code for `square()` function that draws a square:

    def my_square_drawing_function(size):
        # Move to the top-right corner before drawing:
        turtle.penup()
        turtle.forward(size // 2)
        turtle.left(90)
        turtle.forward(size // 2)
        turtle.left(180)
        turtle.pendown()

        # Draw a square with sides of length `size`:
        for i in range(4):  # Draw four lines.
            turtle.forward(size)
            turtle.right(90)

On its own, this function will just draw a square of a given size. (Note that this function isn't recursive; it just draws one square.) But the `fam.draw_fractal()` function can use functions like this to create fractals.

To make a fractal, call `fam.draw_fractal()` and pass it this drawing function, a starting size (let's go with `100`), and a list of *recursion specification dictionaries*. By recursion specification dictionary, I mean a list of dictionaries with (optional) keys `'size'`, `'x'`, `'y'`, and `'angle'`. I'll explain what these keys do later, but try calling this:

    fam.draw_fractal(my_square_drawing_function, 100, [{'size': 0.96, 'y': 0.5, 'angle': 11}])

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/my_square1.webp" style="max-width: 50%">

This draws a fractal similar to the `fam.demo_horn()` fractal. The `100` is the initial size for the first square to draw. The list of recursion specification dictionaries `[{'size': 0.96, 'y': 0.5, 'angle': 11}]` has one dictionary in it. This means for each shape drawn with the drawing function, we will draw one more recursive shape. The new square is drawn at 96% the original size (because the `'size'` key is `0.96`), located 50% of the size above the square (because the `'y'` key is `0.5`), after rotating it counterclockwise by 11 degrees (because the `'angle'` is set to `11`).

By default, `fam.draw_fractal()` only goes 8 recursive levels deep. You can change this by passing a `max_depth` argument.

    fam.draw_fractal(my_square_drawing_function, 100, [{'size': 0.96, 'y': 0.5, 'angle': 11}], max_depth=50)

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/my_square2.webp" style="max-width: 50%">


Let's make each square draw *two* squares by putting a *second* recursion specification dictionary in the list. Because each square will draw two squares (and both of those two squares will draw two squares each, and so on and so on), be sure to set `max_depth` to something small like it's default `8`. Otherwise, the exponentially large amount of drawing will slow your program down to a crawl.

Let's make the second recursion specification dictionary the same as the first, but it's `'angle'` key is `-11` instead of `11`. This will make it veer off clockwise by 11 degrees instead of the normal counterclockwise:

    fam.draw_fractal(my_square_drawing_function, 100, [{'size': 0.96, 'y': 0.5, 'angle': 11}, {'size': 0.96, 'y': 0.5, 'angle': -11}], max_depth=8)


<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/my_square3.webp" style="max-width: 50%">



As you can see, it doesn't take much to fill up the window with too many shapes. The key to making aesthetically pleasing fractals is to take a light touch and spend a lot of time experimenting. For example, we could pass a list of three recursion specification dictionaries to draw squares in three of the corners of the parent square:

    fam.draw_fractal(my_square_drawing_function, 350,
        [{'size': 0.5, 'x': -0.5, 'y': 0.5},
         {'size': 0.5, 'x': 0.5, 'y': 0.5},
         {'size': 0.5, 'x': -0.5, 'y': -0.5}], max_depth=4)

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/my_square4.webp" style="max-width: 50%">

If we increase the max depth to `10`, we can see a new pattern emerge:

    fam.draw_fractal(my_square_drawing_function, 350,
        [{'size': 0.5, 'x': -0.5, 'y': 0.5},
         {'size': 0.5, 'x': 0.5, 'y': 0.5},
         {'size': 0.5, 'x': -0.5, 'y': -0.5}], max_depth=10)

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/my_square5.webp" style="max-width: 50%">

The `fractalartmaker` module comes with a `fam.square` and `fam.triangle` drawing functions that you can play with. Also take a look at the code for the demo functions inside the *\_\_init\_\_.py* file for more ideas. Check out the rest of this documentation for advanced tips. Good luck!

NOTE: Calling `fam.draw_fractal()` automatically calls `turtle.reset()` to clear the window and move the turtle cursor back to 0, 0. If you don't want this behavior, pass `reset=False` to `fam.draw_fractal()`

NOTE: To free you from having to import the `turtle` module yourself, you can call most `turtle` functions from the `fam` module: `fam.reset()`, `fam.update()`, and so on.

Gallery of Demo Fractals
=================

    def demo_four_corners(size=350, max_depth=5, **kwargs):
        # Four Corners:
        if 'colors' not in kwargs:
            kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
        draw_fractal(square, size,
            [{'size': 0.5, 'x': -0.5, 'y': 0.5},
             {'size': 0.5, 'x': 0.5, 'y': 0.5},
             {'size': 0.5, 'x': -0.5, 'y': -0.5},
             {'size': 0.5, 'x': 0.5, 'y': -0.5}], max_depth=max_depth, **kwargs)

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/four-corners.webp" style="max-width: 50%">

    def demo_spiral_squares(size=600, max_depth=50, **kwargs):
        # Spiral Squares:
        if 'colors' not in kwargs:
            kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
        draw_fractal(square, size, [{'size': 0.95,
            'angle': 7}], max_depth=max_depth, **kwargs)

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/spiral-squares.webp" style="max-width: 50%">


    def demo_double_spiral_squares(size=600, **kwargs):
        # Double Spiral Squares:
        if 'colors' not in kwargs:
            kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
        draw_fractal(square, 600,
            [{'size': 0.8, 'y': 0.1, 'angle': -10},
             {'size': 0.8, 'y': -0.1, 'angle': 10}], **kwargs)

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/double-spiral-squares.webp" style="max-width: 50%">


    def demo_triangle_spiral(size=20, max_depth=80, **kwargs):
        # Triangle Spiral:
        draw_fractal(triangle, size,
            [{'size': 1.05, 'angle': 7}], max_depth=max_depth, **kwargs)

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/triangle-spiral.webp" style="max-width: 50%">


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

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/glider.webp" style="max-width: 50%">


    def demo_sierpinski_triangle(size=600, **kwargs):
        # Sierpinski Triangle:
        toMid = math.sqrt(3) / 6
        draw_fractal(triangle, 600,
            [{'size': 0.5, 'y': toMid, 'angle': 0},
             {'size': 0.5, 'y': toMid, 'angle': 120},
             {'size': 0.5, 'y': toMid, 'angle': 240}], **kwargs)


<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/sierpinski-triangle.webp" style="max-width: 50%">



    def demo_wave(size=280, **kwargs):
        # Wave:
        draw_fractal(triangle, size,
            [{'size': 0.5, 'x': -0.5, 'y': 0.5},
             {'size': 0.3, 'x': 0.5, 'y': 0.5},
             {'size': 0.5, 'y': -0.7, 'angle': 15}], **kwargs)


<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/wave.webp" style="max-width: 50%">



    def demo_horn(size=100, max_depth=100, **kwargs):
        # Horn:
        if 'colors' not in kwargs:
            kwargs['colors'] = (('black', 'white'), ('black', 'gray'))
        draw_fractal(square, size,
            [{'size': 0.96, 'y': 0.5, 'angle': 11}], max_depth=max_depth, **kwargs)


<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/horn.webp" style="max-width: 50%">


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

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/snowflake.webp" style="max-width: 50%">



Advanced Features of FAM's Shape-Drawing Functions
==========================

All shape-drawing functions are passed a `size` argument. We can make the white-and-gray alternating colors by adding the optional `depth` parameter to our drawing function. The `draw_fractal()` function will pass the recursion depth (`1` for the first depth level, `2` for the next, and so on) to the drawing function. In the following `square_alternating_white_gray()` drawing function, the fill color for the square is set to white or gray depending on the `depth` argument:

    def square_alternating_white_gray(size, depth):
        # Move to the top-right corner before drawing:
        turtle.penup()
        turtle.forward(size // 2)
        turtle.left(90)
        turtle.forward(size // 2)
        turtle.left(180)
        turtle.pendown()

        # Set fill color based on recursion depth level:
        if depth % 2 == 0:
            turtle.fillcolor('white')
        else:
            turtle.fillcolor('gray')

        # Draw a square:
        turtle.begin_fill()
        for i in range(4):  # Draw four lines.
            turtle.forward(size)
            turtle.right(90)
        turtle.end_fill()

    draw_fractal(square_alternating_white_gray, 300, 
        [{'size': 0.5, 'x': -0.5, 'y': 0.5},
        {'size': 0.5, 'x': 0.5, 'y': 0.5},], max_depth=5)


<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/alternating-white-gray-squares.webp" style="max-width: 50%">



You can also pass any custom keyword argument to `draw_fractal()`, and it will be forwarded to the drawing function. For example, I set up `square_random_fill()` draw function with a `custom_fill_colors` parameter. If you pass `custom_fill_colors=['blue', 'red', 'yellow', 'black', 'white']` to `draw_fractal()`, this list will be forwarded to the draw function. Note that if you pass a custom argument like `custom_fill_colors` to `draw_fractal()`, the drawing function must have a parameter named `custom_fill_colors`.
    
    import random

    def square_random_fill(size, custom_fill_colors):
        # Move to the top-right corner before drawing:
        turtle.penup()
        turtle.forward(size // 2)
        turtle.left(90)
        turtle.forward(size // 2)
        turtle.left(180)
        turtle.pendown()

        # Set fill color randomly:
        turtle.fillcolor(random.choice(custom_fill_colors))
        
        # Draw a square:
        turtle.begin_fill()
        for i in range(4):  # Draw four lines.
            turtle.forward(size)
            turtle.right(90)
        turtle.end_fill()

    draw_fractal(square_random_fill, 300, 
        [{'size': 0.5, 'x': -0.5, 'y': 0.5},
        {'size': 0.5, 'x': 0.5, 'y': 0.5},], max_depth=5, custom_fill_colors=['blue', 'red', 'yellow', 'black', 'white'])

<img src="https://raw.githubusercontent.com/asweigart/fractalartmaker/main/random-fill-squares.webp" style="max-width: 50%">




Python Turtle Module Cheat Sheet
===============================

    import turtle
    turtle.forward(100)   # Move forward 100 steps.
    turtle.backward(100)  # Move backwards 100 steps.
    turtle.left(90)       # Turn left/clockwise 90 degrees.
    turtle.right(90)      # Turn right/counterclockwise 90 degrees.

    turtle.position()  # Return (0, 0), the current XY position of the turtle.
    turtle.heading()   # Return 0.0, the current heading/direction of the turtle. (0 is right, 90 is up, 180 is left, 270 is down)

    turtle.goto(30, 25)     # Move turtle to X of 30 and Y of 25.
    turtle.setx(30)         # Move turtle left/right to X of 30 and current Y coordinate.
    turtle.sety(25)         # Move turtle up/down to Y of 25 and current X coordinate.
    turtle.towards(30, 25)  # Return degrees to turn left to face XY 30, 25 from current position/heading.
    turtle.setheading(90)   # Make the turtle face up (90 degrees).

    turtle.penup()    # "Raise the pen" and stop drawing as the turtle moves.
    turtle.pendown()  # "Lower the pen" and start drawing as the turtle moves.

    turtle.pensize(4)       # Set pen thickness size to 4. (Default is 1.)
    turtle.width()          # Return 4, the current pen thickness size.
    turtle.pencolor('red')  # Lines drawn will now be red. (Also use color formats '#FF0000' or (255, 0, 0))

    turtle.fillcolor('white')  # Set fill color of begin_fill() and end_fill() to white.
    turtle.begin_fill()        # Start drawing a filled-in shape.
    turtle.end_fill()          # End drawing a filled-in shape and draw the fill color.

    turtle.home()   # Move the turtle to 0, 0 and facing right (0 degrees).
    turtle.clear()  # Erase all drawings on the screen, but leave the turtle in its place.
    turtle.reset()  # Erase all drawings and move turtle to 0, 0 and facing right.

    turtle.hideturtle()  # Don't show the turtle cursor in the window.
    turtle.showturtle()  # Show the turtle cursor in the window.

    turtle.bgcolor('blue')  # Make the background color of the window blue. (Default is white.)

    turtle.tracer(1000, 0)  # Do 1000 turtle commands with 0 delay all at once. (Increase 1000 to make drawing speed faster.)
    turtle.update()         # Call this when done to update the screen with any remaining turtle commands' drawings.

    turtle.exitonclick()  # Close the window when the user clicks it.

    turtle.fd()  # Same as forward()
    turtle.bk()  # Same as backward()
    turtle.lt()  # Same as left()
    turtle.rt()  # Same as right()

    turtle.pos()  # Same as position()

    turtle.pd()  # Same as pendown()
    turtle.pu()  # Same as penup()

