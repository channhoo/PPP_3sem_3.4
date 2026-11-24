"""Игровые объекты и их движение."""

import pygame

import settings as cfg


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
        """Нарисовать корабль и его видимые части за краями поля."""
        source = self.thrust_image if self.thrusting else self.idle_image
        image = pygame.transform.rotate(source, -self.angle)
        rect = image.get_rect(center=(round(self.position.x),
                                      round(self.position.y)))
        field = screen.get_rect()

        for dx in (-cfg.WIDTH, 0, cfg.WIDTH):
            for dy in (-cfg.HEIGHT, 0, cfg.HEIGHT):
                copy_rect = rect.move(dx, dy)
                if field.colliderect(copy_rect):
                    screen.blit(image, copy_rect)
