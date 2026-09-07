from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
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
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

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

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод для отрисовки объекта на игровом поле.
        Этот метод должен быть переопределен в подклассах.
        """
        pass  # Этот метод будет переопределен в подклассах


class Apple(GameObject):
    """
    Класс, представляющий яблоко в игре.

    Attributes:
        position (tuple): Координаты яблока на игровом поле.
        body_color (tuple): Цвет яблока.
    """

    def __init__(self, position):
        super().__init__(position, APPLE_COLOR)

    def draw(self):
        """
        Отрисовывает яблоко на игровом поле.

        Args:
            self (Apple): Экземпляр класса Apple, который нужно отрисовать.
            Returns: None
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, snake_positions=None):
        """
        Случайным образом изменяет позицию яблока на игровом поле,
        избегая пересечения с позицией змейки.

        Args:
            snake_positions (list): Список координат сегментов змейки.
        Returns:
            None
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in (snake_positions or []):
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

    def __init__(self, position):
        super().__init__(position, SNAKE_COLOR)
        self.positions = [position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.length = 1
        self.last = None  # Последний сегмент змейки для затирания

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

        new_head_position = (
            (self.positions[0][0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (self.positions[0][1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
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
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
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


def update_direction(self):
    """
    Обновляет направление движения змейки на основе следующего направления.

    Args:
        self (Snake): Экземпляр класса Snake, для которого обновляется
        направление.
    Returns:
        None
    """
    if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None


def reset(snake, apple):
    """
    Сбрасывает состояние игры, возвращая змейку и яблоко в нач
    альное положение.

    Args:
        snake (Snake): Экземпляр класса Snake, который нужно сбросить.
        apple (Apple): Экземпляр класса Apple, который нужно сбросить.
    Returns:
        None
    """
    snake.positions = [(200, 200)]
    snake.direction = choice([UP, DOWN, LEFT, RIGHT])
    snake.next_direction = None
    snake.length = 1
    snake.last = None
    apple.randomize_position()


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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


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
    screen.blit(board, (0, 0))
    apple = Apple((100, 100))
    snake = Snake((200, 200))
    while True:
        handle_keys(snake)
        snake.move()
        if apple.position == snake.positions[0]:
            snake.grow()
            apple.randomize_position()
        if snake.positions[0] in snake.positions[1:]:
            reset(snake, apple)
        # Тут нужно вызвать методы отрисовки объектов.
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
