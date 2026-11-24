"""Игровые объекты и их движение."""

import pygame

import settings as cfg
from random import uniform

class Ship:
    """Корабль игрока с инерцией и двумя состояниями двигателя."""

    def __init__(self, hull, flame):
        """Собрать два спрайта с одинаковым положением корпуса."""
        width = hull.get_width() + 2 * flame.get_width()
        height = max(hull.get_height(), flame.get_height())
        self.idle_image = pygame.Surface((width, height), pygame.SRCALPHA)
        hull_rect = hull.get_rect(center=self.idle_image.get_rect().center)
        self.idle_image.blit(hull, hull_rect)

        self.thrust_image = self.idle_image.copy()
        flame_rect = flame.get_rect(
            midright=(hull_rect.left + 12, hull_rect.centery)
        )
        self.thrust_image.blit(flame, flame_rect)

        self.position = pygame.Vector2(cfg.WIDTH / 2, cfg.HEIGHT / 2)
        self.velocity = pygame.Vector2()
        self.angle = 0.0
        self.thrusting = False

    def update(self, dt, turn, thrust):
        """Повернуть корабль и обновить его скорость и координаты."""
        self.angle = (self.angle + turn * cfg.SHIP_TURN_SPEED * dt) % 360
        self.thrusting = thrust

        if thrust:
            direction = pygame.Vector2(1, 0).rotate(self.angle)
            self.velocity += direction * cfg.SHIP_ACCELERATION * dt
            if self.velocity.length() > cfg.SHIP_MAX_SPEED:
                self.velocity.scale_to_length(cfg.SHIP_MAX_SPEED)
        else:
            speed = self.velocity.length()
            if speed <= cfg.SHIP_BRAKING * dt:
                self.velocity.update(0, 0)
            else:
                self.velocity.scale_to_length(speed - cfg.SHIP_BRAKING * dt)

        self.position += self.velocity * dt
        self.position.x %= cfg.WIDTH
        self.position.y %= cfg.HEIGHT

    def draw(self, screen):
        """Нарисовать корабль с учётом перехода через края."""
        source = self.thrust_image if self.thrusting else self.idle_image
        draw_wrapped(screen, source, self.position, self.angle)

def draw_wrapped(screen, source, position, angle):
    """Нарисовать спрайт по обе стороны границы при пересечении."""
    image = pygame.transform.rotate(source, -angle)
    rect = image.get_rect(center=(round(position.x), round(position.y)))
    field = screen.get_rect()

    for dx in (-cfg.WIDTH, 0, cfg.WIDTH):
        for dy in (-cfg.HEIGHT, 0, cfg.HEIGHT):
            copy_rect = rect.move(dx, dy)
            if field.colliderect(copy_rect):
                screen.blit(image, copy_rect)


class Rocket:
    """Ракета, которая летит с постоянной скоростью и исчезает по таймеру."""

    def __init__(self, image, ship):
        """Создать ракету у носа корабля в направлении выстрела."""
        self.image = image
        self.angle = ship.angle
        direction = pygame.Vector2(1, 0).rotate(self.angle)
        self.position = ship.position + direction * cfg.ROCKET_NOSE_OFFSET
        self.velocity = direction * cfg.ROCKET_SPEED
        self.remaining = cfg.ROCKET_LIFETIME

    def update(self, dt):
        """Переместить ракету и уменьшить оставшееся время полёта."""
        self.position += self.velocity * dt
        self.position.x %= cfg.WIDTH
        self.position.y %= cfg.HEIGHT
        self.remaining -= dt

    def draw(self, screen):
        """Нарисовать ракету с учётом перехода через края."""
        draw_wrapped(screen, self.image, self.position, self.angle)


class Asteroid:
    """Астероид со случайным направлением, скоростью и вращением."""

    def __init__(self, image, position):
        """Создать астероид в выбранной точке поля."""
        self.image = image
        self.position = pygame.Vector2(position)
        self.angle = uniform(0, 360)
        self.spin = uniform(-90, 90)  # Градусов в секунду.
        speed = uniform(cfg.ASTEROID_MIN_SPEED, cfg.ASTEROID_MAX_SPEED)
        self.velocity = pygame.Vector2(speed, 0).rotate(uniform(0, 360))

    def update(self, dt):
        """Переместить и повернуть астероид."""
        self.position += self.velocity * dt
        self.position.x %= cfg.WIDTH
        self.position.y %= cfg.HEIGHT
        self.angle = (self.angle + self.spin * dt) % 360

    def draw(self, screen):
        """Нарисовать астероид с учётом перехода через края."""
        draw_wrapped(screen, self.image, self.position, self.angle)

def touching(first, second, radius):
    """Проверить столкновение по кратчайшему расстоянию через края."""
    dx = abs(first.x - second.x) % cfg.WIDTH
    dy = abs(first.y - second.y) % cfg.HEIGHT
    dx = min(dx, cfg.WIDTH - dx)
    dy = min(dy, cfg.HEIGHT - dy)
    return dx**2 + dy**2 <= radius**2


class Explosion:
    """Показывает кадры взрыва в одной точке поля."""

    def __init__(self, frames, position):
        """Запомнить кадры и координаты центра взрыва."""
        self.frames = frames
        self.position = pygame.Vector2(position)
        self.age = 0.0

    @property
    def finished(self):
        """Проверить, закончилась ли анимация."""
        return self.age >= len(self.frames) * cfg.EXPLOSION_FRAME_TIME

    def update(self, dt):
        """Продвинуть время анимации."""
        self.age += dt

    def draw(self, screen):
        """Нарисовать кадр, соответствующий текущему времени."""
        if not self.finished:
            index = int(self.age / cfg.EXPLOSION_FRAME_TIME)
            draw_wrapped(screen, self.frames[index], self.position, 0)

class Supply:
    """Дрейфующая капсула или выпавший из неё бонус."""

    def __init__(self, image, position, velocity, lifetime=None):
        """Запомнить спрайт, движение и время до исчезновения."""
        self.image = image
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.remaining = lifetime

    def update(self, dt):
        """Сдвинуть объект и обновить его таймер."""
        self.position += self.velocity * dt
        self.position.x %= cfg.WIDTH
        self.position.y %= cfg.HEIGHT
        if self.remaining is not None:
            self.remaining -= dt

    def draw(self, screen):
        """Нарисовать объект, мигая перед исчезновением бонуса."""
        if self.remaining is not None and self.remaining <= cfg.BONUS_BLINK_TIME:
            phase = int(self.remaining / cfg.BONUS_BLINK_INTERVAL)
            if phase % 2:
                return
        draw_wrapped(screen, self.image, self.position, 0)
        