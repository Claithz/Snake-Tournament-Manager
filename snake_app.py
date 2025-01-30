import turtle
from turtle import Screen
from snake_models import Snake, Food, ScoreBoard
import time


def run_snake_game(player):
    playing = True
    screen = Screen()
    turtle.TurtleScreen._RUNNING = True
    screen.setup(600, 600)
    screen.bgcolor("grey")
    screen.title("snakegame")
    screen.tracer(0)

    snake = Snake()
    food = Food()
    score_board = ScoreBoard(player)

    screen.listen()
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")

    while playing:
        screen.update()
        time.sleep(0.1)
        snake.move()

        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()
            score_board.increase_score()
            score_board.refresh()

        if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
            score_board.reset_score_board()
            snake.reset_snake()
            playing = False

        for segments in snake.segments[1:]:
            if snake.head.distance(segments) < 10:
                score_board.reset_score_board()
                snake.reset_snake()
                playing = False

    screen.bye()
