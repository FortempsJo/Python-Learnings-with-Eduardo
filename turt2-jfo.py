from turtle import *

def DrawMandala (turtle,color1,color2,direction,angle) :
    turtle = Turtle()
    turtle.shape('circle')
    turtle.color(color1,color2)
#    turtle.begin_fill()
    while True:
        turtle.forward(direction)
        turtle.left(angle)
        if abs(turtle.pos()) < 1:
            break
#    turtle.end_fill()
    done()

turtle2 = Turtle()
screen2 = Screen()
turtle2.pos()

print (turtle2.pos())

DrawMandala (turtle2,'blue','green',-200,170)

print (turtle2.pos())

turtle3 = Turtle()
DrawMandala (turtle3,'blue','green',-200,160)

screen2.exitonclick()

