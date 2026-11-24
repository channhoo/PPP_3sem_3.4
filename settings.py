"""Размеры окна, параметры заставки и палитра игры."""

WIDTH, HEIGHT = 960, 640
FPS = 60

START_LIVES = 3
BACKGROUND_SPEED = 22  # Скорость дальних астероидов в пикселях в секунду.
BACKGROUND_ALPHA = 36  # Прозрачность дальнего слоя по шкале от 0 до 255.
STAR_COUNT = 85

SPACE_COLOR = "#0e132d"
PANEL_COLOR = "#171b38"
CREAM = "#fff0c9"
LILAC = "#aa9ed4"

# Скорости в пикселях и градусах, время в секундах.
SHIP_TURN_SPEED = 200  # Градусов в секунду.
SHIP_ACCELERATION = 320  # Пикселей в секунду за секунду тяги.
SHIP_MAX_SPEED = 350  # Максимальная скорость в пикселях в секунду.
SHIP_BRAKING = 170  # Насколько быстро падает скорость без тяги.

ROCKET_SPEED = 560  # Пикселей в секунду.
ROCKET_LIFETIME = 0.9  # Ракета пролетает 504 пикселя при высоте окна 640.
ROCKET_NOSE_OFFSET = 27  # Расстояние от центра корабля до носа.

ASTEROID_INTERVAL = 1.8  # Секунд между попытками появления астероида.
ASTEROID_LIMIT = 10  # Максимум игровых астероидов на экране.
ASTEROID_MIN_SPEED = 35  # Пикселей в секунду.
ASTEROID_MAX_SPEED = 80  # Пикселей в секунду.
ASTEROID_SPAWN_DISTANCE = 135  # Минимальное расстояние от корабля.

# Радиусы столкновения в пикселях экрана.
SHIP_RADIUS = 18
ROCKET_RADIUS = 5
ASTEROID_RADIUS = 25

# Каждый кадр взрыва занимает 32 × 32 пикселя на листе спрайтов.
EXPLOSION_FRAME_SIZE = 32
EXPLOSION_SCALE = 2
EXPLOSION_FRAME_TIME = 0.07  # Секунд на один кадр.

CAPSULE_INTERVAL = 25.0  # Секунд до следующей капсулы.
CAPSULE_SPEED = 30  # Скорость дрейфа в пикселях в секунду.
CAPSULE_RADIUS = 14
CAPSULE_SPAWN_DISTANCE = 160  # Минимальное расстояние от корабля.

BONUS_LIFETIME = 7.0  # Сколько секунд можно подобрать бонус.
BONUS_RADIUS = 12
BONUS_BLINK_TIME = 2.0  # Бонус мигает перед исчезновением.
BONUS_BLINK_INTERVAL = 0.15  # Сколько длится одна фаза мигания.