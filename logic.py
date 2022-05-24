import random
from xxlimited import new

class Snake:
    def __init__(self) -> None:
        self.directions = {"upwards":[0,1], "right":[1,0], "downwards":[0,-1], "left":[-1,0]}
        self.snake_body = [Point(6,5), Point(5,5), Point(4,5)]
        self.current_direction = self.directions["upwards"]
    def snake_update(self, direction:list, WIDTH, HEIGHT, apple_pos):
        new_head = Point(self.snake_body[0].x + direction[0], self.snake_body[0].y + direction[1])
        self.snake_body.insert(0, new_head)
        if new_head.x == apple_pos.x and new_head.y == apple_pos.y:
            return 1
        else:
            self.snake_body.pop()
        if (
            new_head.x<0 or new_head.x>WIDTH-1
            or new_head.y<0 or new_head.y>HEIGHT-1
            or Snake.check_collision(new_head, self.snake_body[1:])
        ):
            return -1
    def check_collision(point, body):
        for body_part in body:
            if point.x == body_part.x and point.y == body_part.y:
                return True
        
    
class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Enviroment:
    def generate_apple(CELLS_VERTICAL, CELLS_HORIZONTAL, snake):
        snake_body_arr =[]
        for body in snake.snake_body:
            snake_body_arr.append([body.x, body.y])
        apple_pos = random.randint(0, CELLS_VERTICAL - 1), random.randint(0, CELLS_HORIZONTAL - 1)
        while apple_pos in snake_body_arr:
            apple_pos = random.randint(0, CELLS_VERTICAL - 1), random.randint(0, CELLS_HORIZONTAL - 1)
        return Point(apple_pos[0], apple_pos[1])

