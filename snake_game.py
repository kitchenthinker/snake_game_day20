import random
import turtle
import math
import time

GAP_BETWEEN_CELLS = 20
TIME_SLEEP = 0.07
SNAKE_STEPS = 25


def check_collisions_2_obj(f_obj: turtle.Turtle, s_obj: turtle.Turtle):
    x_collision = (math.fabs(f_obj.xcor() - s_obj.xcor()) * 2) < (f_obj.pensize() + s_obj.pensize())
    y_collision = (math.fabs(f_obj.ycor() - s_obj.ycor()) * 2) < (f_obj.pensize() + s_obj.pensize())
    return x_collision and y_collision


def check_collisions_2_obj_food(f_obj: turtle.Turtle, s_obj: turtle.Turtle):
    return f_obj.distance(s_obj) < s_obj.pensize()*2


def _set_game_screen_default(v_screen):
    if v_screen is None:
        v_screen = turtle.Screen()
        v_screen.setup(width=600, height=600)
        v_screen.title("My snake game")
        v_screen.bgcolor("black")
        v_screen.tracer(0)
        v_screen.update()
    return v_screen


class MainGame:

    def __init__(self, v_graphic=None, v_screen=None):
        self.game_screen = _set_game_screen_default(v_screen)
        self.graphics = None
        self.create_game_graphic()
        self.snake = Snake()
        self.apple = Apple()
        self.game_is_on = True
        self.game_points = 0

    def create_game_graphic(self):
        self.graphics = turtle.Turtle(visible=False)
        self.graphics.color("white")
        self.graphics.hideturtle()
        self.graphics.penup()

    def write_game_score(self):
        self.graphics.clear()
        self.graphics.setposition(0, self.game_screen.window_width()/2 - 50)
        self.graphics.write(f"GAME POINTS:    {self.game_points}", False, align="center", font=("Small fonts", 18, "bold"))

    def start_game(self):
        self.game_screen.listen()
        self.game_screen.onkey(self.snake.turn_north, 'w')
        self.game_screen.onkey(self.snake.turn_south, 's')
        self.game_screen.onkey(self.snake.turn_west, 'a')
        self.game_screen.onkey(self.snake.turn_east, 'd')
        self.game_screen.onkey(self.reset_game, 'c')

        while self.game_is_on:
            time.sleep(TIME_SLEEP)
            self.write_game_score()
            self.game_screen.update()
            self.snake.move()
            self.check_collisions_with_walls()
            self.check_collisions_with_tail()
            self.check_collision_with_apple()
            self.check_game_is_over()
        self.game_screen.exitonclick()

    def check_collision_with_apple(self):
        if check_collisions_2_obj_food(self.snake.head, self.apple):
            self.apple.hide_up_apple()
            self.apple.set_is_eaten(True)
            self.apple.show_up_apple(self.game_screen.window_width(), self.game_screen.window_height())
            self.increase_game_point_counter()
            self.snake.add_segment_2_tail()

    def check_game_is_over(self):
        if not self.snake.moving:
            self.game_is_on = False
            self.graphics.setposition(0, 0)
            self.graphics.write(f"GAME OVER:", False, align="center",
                                font=("Small fonts", 18, "bold"))
            return True
        return False

    def reset_game(self):
        #self.snake.game_is_reset()
        self.game_screen.clear()
        self.__init__()
        self.start_game()

    def increase_game_point_counter(self):
        self.game_points += 1

    def check_collisions_with_tail(self):
        snake = self.snake
        for segment in range(1, len(snake.body) - 1, 1):
            if check_collisions_2_obj(snake.head, snake.body[segment]):
                self.snake.set_moving_var(False)

    def check_collisions_with_walls(self):
        x_cor = self.snake.head.xcor()
        y_cor = self.snake.head.ycor()
        w_width = self.game_screen.window_width()
        w_height = self.game_screen.window_height()
        ###
        left_wall = - (w_width/2)
        right_wall = (w_width/2)
        up_wall = (w_height/2)
        down_wall = - (w_height/2)
        ###
        if (x_cor >= right_wall) or (x_cor <= left_wall) or (y_cor >= up_wall) or (y_cor <= down_wall):
            self.snake.set_moving_var(False)


class Snake:

    def __init__(self):
        self.body = []
        self.create_body()
        self.head = self.body[0]
        self.head.pensize(10)
        self.x_cor = self.head.xcor()
        self.y_cor = self.head.ycor()
        self.moving = True

    def create_body(self):
        for _ in range(3):
            self.add_segment_2_tail()

    def game_is_reset(self):
        for segment in self.body:
            segment.reset()
        self.__init__()

    def set_moving_var(self, variable: bool):
        self.moving = variable

    def set_head_coordinates(self):
        self.x_cor = self.head.xcor()
        self.y_cor = self.head.ycor()

    def move(self):
        if self.moving:
            for segment in range(len(self.body) - 1, 0, -1):
                new_x = self.body[segment - 1].xcor()
                new_y = self.body[segment - 1].ycor()
                self.body[segment].goto(new_x, new_y)
            self.head.forward(SNAKE_STEPS)
            self.set_head_coordinates()

    def add_segment(self, start_x=0, start_y=0):
        segment = turtle.Turtle(shape="square")
        segment.penup()
        segment.color("white")
        segment.setposition(start_x, start_y)
        self.body.append(segment)

    def add_segment_2_tail(self, x_cor=0, y_cor=0):
        if self.body.__len__() == 0:
            self.add_segment(x_cor, y_cor)
        else:
            last_segment_x = self.body[-1].xcor()
            last_segment_y = self.body[-1].ycor()
            self.add_segment(last_segment_x - GAP_BETWEEN_CELLS, last_segment_y)

    def turn_north(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def turn_south(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def turn_west(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def turn_east(self):
        if self.head.heading() != 180:
            self.head.setheading(0)


class Apple(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("green")
        self.pensize(10)
        self.penup()
        self.show_up_apple()
        self.is_eaten = False

    def show_up_apple(self, w_boundary=150, h_boundary=150):
        width = int(w_boundary/2)
        height = int(h_boundary/2)
        gap_align = 50
        x_cor = random.randint(-width + gap_align, width - gap_align)
        y_cor = random.randint(-height + gap_align, height - gap_align)
        #self.hideturtle()
        self.setposition(x_cor, y_cor)
        # #self.showturtle()
        # self.set_is_eaten(False)

    def hide_up_apple(self):
        time.sleep(0.1)
        #self.clear()

    def apple_is_eaten(self):
        return self.is_eaten

    def set_is_eaten(self, variable: bool):
        self.is_eaten = variable
