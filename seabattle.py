import gamepole as gp
import pygame
import random


player = gp.GamePole(10)
player.init()
computer = gp.GamePole(10)
computer.init()

pole_size = player._size
indent = pole_size / 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

block_sz, left_mn, upper_mn = 50, 200, 100
window_size = left_mn + (3 * pole_size) * block_sz, upper_mn + (pole_size + pole_size / 2) * block_sz
font_size = int(block_sz / 1.5)

pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Sea Battle")

pygame.display.flip()
font = pygame.font.SysFont('arial', font_size)


def naming():
    computer = font.render("Computer", True, BLACK)
    player = font.render("Player", True, BLACK)
    sign1_width = computer.get_width()
    sign2_width = player.get_width()
    screen.blit(computer, (left_mn + indent * block_sz - sign1_width // 2, upper_mn - block_sz//2 - font_size))
    screen.blit(player, (left_mn + 2 * pole_size * block_sz - sign2_width // 2, upper_mn - block_sz//2 - font_size))


def draw_numbers_and_letters(step):
    letters = [chr(i).upper() for i in range(97, 97 + pole_size)]

    if step < pole_size:
        num_ver = font.render(str(step + 1), True, BLACK)
        letters_hor = font.render(letters[step], True, BLACK)

        num_ver_width, num_ver_height = num_ver.get_width(), num_ver.get_height()
        letters_hor_width = letters_hor.get_width()

        # Vertical numbers of player pole
        screen.blit(num_ver, (left_mn - (block_sz // 2 + num_ver_width // 2) + (pole_size + indent) * block_sz,
                              upper_mn + step * block_sz + (block_sz // 2 - num_ver_height // 2)))
        # Horizontal letters of player pole
        screen.blit(letters_hor, (left_mn + step * block_sz + (block_sz // 2 - letters_hor_width // 2) +
                                  (pole_size + indent) * block_sz, upper_mn + pole_size * block_sz))
        # Vertical numbers of computer pole
        screen.blit(num_ver, (left_mn - (block_sz // 2 + num_ver_width // 2),
                              upper_mn + step * block_sz + (block_sz // 2 - num_ver_height // 2)))
        # Horizontal letters of computer pole
        screen.blit(letters_hor, (left_mn + step * block_sz + (block_sz // 2 - letters_hor_width // 2),
                                  upper_mn + pole_size * block_sz))


def draw_pole():
    naming()

    for column in range(pole_size + 1):

        # Horizontal lines of computer pole
        pygame.draw.line(screen, BLACK, (left_mn, upper_mn + column * block_sz),
                         (left_mn + pole_size * block_sz, upper_mn + column * block_sz), 1)
        # Vertical lines of computer pole
        pygame.draw.line(screen, BLACK, (left_mn + column * block_sz, upper_mn),
                         (left_mn + column * block_sz, upper_mn + pole_size * block_sz), 1)
        draw_numbers_and_letters(column)
        # Horizontal lines of player pole
        pygame.draw.line(screen, BLACK, (left_mn + (pole_size + indent) * block_sz, upper_mn + column * block_sz),
                         (left_mn + (indent + 2 * pole_size) * block_sz, upper_mn + column * block_sz), 1)
        # Vertical lines of player pole
        pygame.draw.line(screen, BLACK, (left_mn + column * block_sz + (indent + pole_size) * block_sz, upper_mn),
                         (left_mn + column * block_sz + (indent + pole_size) * block_sz, upper_mn +
                          pole_size * block_sz), 1)


def draw_ships(ships):
    for ship in ships:
        x_start, y_start = ship._x, ship._y
        # Vertical ships
        if ship._tp == 2 and ship._length > 1:
            ship_width = block_sz
            ship_height = block_sz * ship._length
        # Horizontal and single-deck ships
        else:
            ship_width = block_sz * ship._length
            ship_height = block_sz
        x = block_sz * x_start + left_mn
        y = block_sz * y_start + upper_mn
        if ships == player._ships:
            x += (pole_size + indent) * block_sz
        pygame.draw.rect(screen, BLACK, ((x, y), (ship_width, ship_height)), width=block_sz//pole_size)


def main():
    game_over = False
    screen.fill(WHITE)
    draw_pole()
    draw_ships(computer.get_ships())
    draw_ships(player.get_ships())
    pygame.display.update()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True


main()
pygame.quit()

