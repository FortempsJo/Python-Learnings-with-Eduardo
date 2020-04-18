from turtle import *

def DrawMandala (color1,color2,Angle) :
    turtle2 = Turtle()
    turtle2.shape('circle')
    turtle2.color(color1,color2)
    turtle2.begin_fill()
    while True:
        turtle2.forward(200)
        turtle2.left(Angle)
        if abs(turtle2.pos()) < 1:
            break
    turtle2.end_fill()
    done()

screen = Screen()
turtle = Turtle()
turtle.shape("turtle")
turtle.forward(50)
turtle.left(90)
turtle.forward(50)
turtle.left(90)
turtle.forward(50)
turtle.left(90)
turtle.forward(50)
turtle.left(90)

turtle.reset()

turtle2 = Turtle()
turtle2.shape('circle')
turtle2.color('red', 'yellow')
turtle2.begin_fill()
while True:
    turtle2.forward(200)
    turtle2.left(170)
    if abs(turtle2.pos()) < 1:
        break
turtle2.end_fill()
done()

screen.exitonclick()

