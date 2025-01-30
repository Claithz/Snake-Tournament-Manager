from turtle import Turtle
import random
import db
from tkinter import messagebox


STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
FONT = ("Times New Roman", 10, "normal")
ALIGNMENT = "center"

def get_user_model():
    from models import User
    return User

class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        self.tail = self.segments[-1]

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        new_segment = Turtle(shape="square")
        new_segment.up()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def reset_snake(self):
        for segments in self.segments:
            segments.goto(1000, 1000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]

    def extend(self):
        self.add_segment(self.tail.position())

    def move(self):
        for segment_number in range(len(self.segments) - 1, 0, -1):
            next_x = self.segments[segment_number - 1].xcor()
            next_y = self.segments[segment_number - 1].ycor()
            self.segments[segment_number].setpos(next_x, next_y)
        self.head.fd(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.seth(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.seth(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.seth(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.seth(RIGHT)


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.up()
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.color("white")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        x_position = random.choice(range(-280, 280, 20))
        y_position = random.choice(range(-280, 280, 20))
        self.goto(x_position, y_position)


class ScoreBoard(Turtle):
    def __init__(self, player):
        super().__init__()
        self.score = 0
        self.player = player
        self.high_score = self.player.score
        self.hideturtle()
        self.up()
        self.goto(0, 270)
        self.refresh()

    def increase_score(self):
        self.score += 1

    def refresh(self):
        self.clear()
        self.write(f"SCORE: {self.score}  HIGH SCORE: {self.high_score}", False, ALIGNMENT, FONT)

    def reset_score_board(self):
        User = get_user_model()
        if self.score > self.high_score:
            messagebox.showinfo(title="New High Score", message=f"You got a new High Score\n"
                                                                f"Your score was {self.score}")
            current_user = db.session.query(User).filter(User.user == self.player.user).first()
            current_user.score = self.score
            self.high_score = self.score
            db.session.commit()
        else:
            messagebox.showinfo(title="You Lost", message=f"You lost\n"
                                                          f"Your score was {self.score}")
        self.score = 0
        self.refresh()

