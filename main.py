import pygame

from jeu.main_menu import main_menu

pygame.init()

screen: pygame.surface.Surface = pygame.display.set_mode(
    (1280, 720), pygame.RESIZABLE | pygame.SCALED
)

main_menu(screen)
