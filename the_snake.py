"""Модуль для работы со случайным значениями."""
from random import choice, randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -20)
DOWN = (0, 20)
LEFT = (-20, 0)
RIGHT = (20, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс, описывающий игровой объект."""

    position = (320, 240)
    body_color = None

    def __init__(self, position, color):
        """Конструктор игрового объекта.

        Отвечает за инициализацию позиции и цвета объекта.
        """
        self.position = position
        self.body_color = color

    def draw(self):
        """Функция, отвечающая за отрисовку объекта на игровом поле."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Конструктор яблока.

        Отвечает за инициализацию цвета и случайной позиции на игровом поле.
        """
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Функция, отвечающая за генерацию случайной позиции яблока."""
        self.position = (randrange(0, 620, 20), randrange(0, 460, 20))

    def draw(self):
        """Функция, отвечающая за отрисовку яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Конструктор класса Snake.

        Отвечает за инициализацию основных параметров змейки.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Функция, отвечающая за обновление направления змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Функция, отвечающая за передвижение змейки."""
        self.update_direction()
        new_x = ((self.get_head_position[0] + self.direction[0])
                 % SCREEN_WIDTH)
        new_y = ((self.get_head_position[1] + self.direction[1])
                 % SCREEN_HEIGHT)
        if (new_x, new_y) in self.positions:
            self.reset()
        else:
            self.positions.insert(0, (new_x, new_y))
            self.last = self.positions.pop()

    def draw(self):
        """Функция, отвечающая за отрисовку змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self):
        """Функция для получения координат головы змейки."""
        return self.positions[0]

    def reset(self):
        """Функция для сброса змейки."""
        self.length = 1
        self.positions = [[320, 240]]
        self.direction = choice(RIGHT, LEFT, UP, DOWN)
        self.next_direction = None


def handle_keys(game_object):
    """Функция для обработки нажатий с клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция, в которой происходит основной игровой цикл."""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()
        if snake.get_head_position == apple.position:
            snake.positions.append(snake.last)
            apple.randomize_position()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
