from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_SZ = (GRID_SIZE, GRID_SIZE)
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

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

# Изначальная позиция змейки:
INITIAL_SNAKE_POSITION = (200, 200)

# Координаты верхнего левого угла игрового поля:
BOARD_TOPLEFT = (0, 0)

DIRECTIONS_KEY = {
    (LEFT, pygame.K_UP): UP,
    (RIGHT, pygame.K_UP): UP,
    (LEFT, pygame.K_DOWN): DOWN,
    (RIGHT, pygame.K_DOWN): DOWN,
    (UP, pygame.K_LEFT): LEFT,
    (DOWN, pygame.K_LEFT): LEFT,
    (UP, pygame.K_RIGHT): RIGHT,
    (DOWN, pygame.K_RIGHT): RIGHT,
}

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.


class GameObject:
    """
    Базовый класс для всех объектов игры.
    Attributes:
        position (tuple): Координаты объекта на игровом поле.
        body_color (tuple): Цвет объекта.
    """

    def __init__(self, position=None, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод для отрисовки объекта на игровом поле.
        Этот метод должен быть переопределен в подклассах.
        """


class Apple(GameObject):
    """
    Класс, представляющий яблоко в игре.

    Attributes:
        occupied_positions (list): Список координат, занятых змейкой,
        чтобы яблоко не появлялось на них.
    """

    def __init__(self, occupied_positions=None):
        super().__init__(None, APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def draw(self):
        """
        Отрисовывает яблоко на игровом поле.

        Args:
            self (Apple): Экземпляр класса Apple, который нужно отрисовать.
            Returns: None
        """
        rect = pygame.Rect(self.position, GRID_SZ)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, occupied_positions=None):
        """
        Случайным образом изменяет позицию яблока на игровом поле,
        избегая пересечения с позицией змейки.

        Args:
            occupied_positions (list): Список координат, занятых змейкой.
        Returns:
            None
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in (occupied_positions or []):
                self.position = new_position
                break


class Snake(GameObject):
    """
    Класс, представляющий змейку в игре.
    Attributes:
        positions (list): Список координат сегментов змейки.
        direction (tuple): Текущее направление движения змейки.
        next_direction (tuple): Следующее направление движения змейки.
        length (int): Длина змейки.
        last (tuple): Последний сегмент змейки для затирания.
    """

    def __init__(self, position=None):
        super().__init__(position, SNAKE_COLOR)
        self.positions = [position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.length = 1
        self.last = None  # Последний сегмент змейки для затирания

    def get_head_position(self):
        """
        Возвращает текущую позицию головы змейки.

        Args:
            self (Snake): Экземпляр класса Snake, для которого нужно получить
            позицию головы.
        Returns:
            tuple: Координаты головы змейки.
        """
        return self.positions[0]

    def move(self):
        """
        Перемещает змейку в текущем направлении и обновляет ее позиции.

        Args:
            self (Snake): Экземпляр класса Snake, который нужно переместить.
        Returns:
            None
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_head_position = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Добавление новой позиции головы в начало списка
        self.positions.insert(0, new_head_position)

        # Удаление последнего сегмента змейки и сохранение его для затирания
        if len(self.positions) > self.length + 1:
            self.last = self.positions.pop()

    def draw(self):
        """
        Отрисовывает змейку на игровом поле.

        Args:
            self (Snake): Экземпляр класса Snake, который нужно отрисовать.
        Returns:
            None
        """
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, GRID_SZ)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(), GRID_SZ)
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, GRID_SZ)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def grow(self):
        """
        Увеличивает длину змейки на 1 сегмент.

        Args:
            self (Snake): Экземпляр класса Snake, который нужно увеличить.
        Returns:
            None
        """
        self.length += 1

    def reset(self, apple):
        """
        Сбрасывает состояние змейки и яблока при столкновении змейки с
        самой собой.

        Args:
            self (Snake): Экземпляр класса Snake, который нужно сбросить.
            apple (Apple): Экземпляр класса Apple, который нужно сбросить.
        Returns:
            None
        """
        self.positions = [INITIAL_SNAKE_POSITION]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.length = 1
        self.last = None
        apple.randomize_position(self.positions)

    def update_direction(self, new_direction):
        """
        Обновляет направление движения змейки, если новое направление
        не противоположно текущему.

        Args:
            self (Snake): Экземпляр класса Snake, для которого нужно обновить
            направление.
            new_direction (tuple): Новое направление движения змейки.
        Returns:
            None
        """
        if (
            new_direction == UP
            and self.direction != DOWN
            or new_direction == DOWN
            and self.direction != UP
            or new_direction == LEFT
            and self.direction != RIGHT
            or new_direction == RIGHT
            and self.direction != LEFT
        ):
            self.next_direction = new_direction


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш пользователя.

    Args:
        snake (Snake): Экземпляр класса Snake, для которого обрабатываются
        нажатия
    Returns:
        None
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if (snake.direction, event.key) in DIRECTIONS_KEY:
                new_direction = DIRECTIONS_KEY[(snake.direction, event.key)]
                if new_direction:
                    snake.next_direction = new_direction


def main():
    """
    Главная функция игры, которая инициализирует PyGame, создает объекты
    игры и запускает основной игровой цикл.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    board = pygame.Surface(screen.get_size())
    board.fill(BOARD_BACKGROUND_COLOR)
    screen.blit(board, BOARD_TOPLEFT)
    snake = Snake(INITIAL_SNAKE_POSITION)
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if apple.position == snake.get_head_position():
            snake.grow()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset(apple)
        # Тут нужно вызвать методы отрисовки объектов.
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
