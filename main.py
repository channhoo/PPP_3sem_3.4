"""Заставка и основной цикл игры «Астероиды»."""

from pathlib import Path
from random import Random

import pygame

import settings as cfg


ASSETS = Path(__file__).with_name("assets")


def load_sprite(name, scale):
    """Загрузить PNG и увеличить его целым множителем."""
    image = pygame.image.load(ASSETS / f"{name}.png").convert_alpha()
    size = (image.get_width() * scale, image.get_height() * scale)
    return pygame.transform.scale(image, size)


class App:
    """Управляет окном, заставкой и переходом к партии."""

    def __init__(self):
        """Создать окно и подготовить изображения."""
        self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        pygame.display.set_caption("Астероиды")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("consolas,dejavusansmono", 52, True)
        self.font = pygame.font.SysFont("consolas,dejavusansmono", 23, True)

        self.ship = load_sprite("ship", 2)
        self.flame = load_sprite("flame", 2)
        self.life_icon = load_sprite("life", 2)
        self.rocks = [load_sprite(f"asteroid_{index}", 2) for index in (1, 2, 3)]
        self.distant_rocks = [rock.copy() for rock in self.rocks]
        for rock in self.distant_rocks:
            rock.set_alpha(cfg.BACKGROUND_ALPHA)

        rng = Random(25)
        self.stars = [
            (rng.randrange(cfg.WIDTH), rng.randrange(cfg.HEIGHT))
            for _ in range(cfg.STAR_COUNT)
        ]
        self.distant_positions = [
            (140, 160), (610, 120), (830, 380), (280, 520), (700, 570)
        ]
        self.scroll = 0.0
        self.card = pygame.Rect(0, 0, 580, 248)
        self.card.center = self.screen.get_rect().center
        self.playing = False
        self.lives = cfg.START_LIVES
        self.score = 0

    def _draw_text(self, text, center, font):
        image = font.render(text, False, cfg.CREAM)
        self.screen.blit(image, image.get_rect(center=center))

    def _draw_background(self):
        self.screen.fill(cfg.SPACE_COLOR)
        for x, y in self.stars:
            pygame.draw.rect(self.screen, "#68648f", (x, y, 2, 2))

        for index, (x, y) in enumerate(self.distant_positions):
            rock = self.distant_rocks[index % len(self.distant_rocks)]
            left = int((x - self.scroll) % cfg.WIDTH)
            self.screen.blit(rock, (left, y))
            self.screen.blit(rock, (left - cfg.WIDTH, y))

    def _draw_hud(self):
        for index in range(self.lives):
            self.screen.blit(self.life_icon, (24 + index * 28, 20))
        self._draw_text(f"ЗАПАС {self.lives}", (174, 31), self.font)
        self._draw_text(f"ОЧКИ {self.score}", (863, 31), self.font)

    def _draw_splash(self):
        hovered = self.card.collidepoint(pygame.mouse.get_pos())
        border = cfg.CREAM if hovered else cfg.LILAC
        pygame.draw.rect(self.screen, cfg.PANEL_COLOR, self.card)
        pygame.draw.rect(self.screen, border, self.card, 3)

        center_x = self.card.centerx
        self._draw_text(
            "АСТЕРОИДЫ", (center_x, self.card.top + 54), self.title_font
        )

        icon_y = self.card.centery + 10
        ship_rect = self.ship.get_rect(center=(center_x, icon_y))
        self.screen.blit(self.ship, ship_rect)
        flame_rect = self.flame.get_rect(
            midright=(ship_rect.left + 11, icon_y)
        )
        self.screen.blit(self.flame, flame_rect)
        for rock, offset in ((self.rocks[0], -135), (self.rocks[2], 135)):
            self.screen.blit(rock, rock.get_rect(center=(center_x + offset, icon_y)))

        self._draw_text(
            "НАЖМИ, ЧТОБЫ НАЧАТЬ",
            (center_x, self.card.bottom - 38),
            self.font,
        )

    def run(self):
        """Обрабатывать события и рисовать кадры до закрытия окна."""
        while True:
            dt = self.clock.tick(cfg.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and not self.playing
                    and self.card.collidepoint(event.pos)
                ):
                    self.playing = True

            self.scroll = (self.scroll + cfg.BACKGROUND_SPEED * dt) % cfg.WIDTH
            self._draw_background()
            if self.playing:
                center = self.screen.get_rect().center
                self.screen.blit(self.ship, self.ship.get_rect(center=center))
            else:
                self._draw_splash()
            self._draw_hud()
            pygame.display.flip()


def main():
    """Запустить приложение."""
    pygame.display.init()
    pygame.font.init()
    try:
        App().run()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
