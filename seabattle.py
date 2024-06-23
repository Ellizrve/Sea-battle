import math

import gamepole as gp
import pygame
import random


player = gp.GamePole(10)
player.init()
computer = gp.GamePole(10)
computer.init()


def human_ships_working():
    return player._ships


def computer_ships_working():
    return computer._ships


pole_size = player._size
indent = pole_size / 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (230, 50, 230)
RED = (255, 0, 0)

block_sz, left_mn, upper_mn = 50, 200, 100
window_size = left_mn + (3 * pole_size) * block_sz, upper_mn + (pole_size + pole_size / 2) * block_sz
font_size = int(block_sz / 1.5)

pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Sea Battle")

pygame.display.flip()
font = pygame.font.SysFont('arial', font_size)

game_over_font_size = 3 * block_sz
game_over_font = pygame.font.SysFont('notosans', game_over_font_size)

computer_available_to_fire_set = set((x, y) for x in range(0, pole_size) for y in range(0, pole_size))
around_last_computer_hit_set = set()
ruined_decks_of_computer_ships = []
ruined_decks_of_player_ships = []
exceptions = set()
computer_win, player_win = False, False


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


def computer_shoots(set_to_shoot_from):
    computer_fired_block = random.choice(tuple(set_to_shoot_from))
    computer_available_to_fire_set.discard(computer_fired_block)
    return check_hit_or_miss(computer_fired_block, human_ships_working(), True)


def calculation_coords(fired_block):
    global around_last_computer_hit_set
    xhit, yhit = fired_block
    if 0 < xhit:
        around_last_computer_hit_set.add((xhit-1, yhit))
    if xhit < pole_size:
        around_last_computer_hit_set.add((xhit+1, yhit))
    if 0 < yhit:
        around_last_computer_hit_set.add((xhit, yhit-1))
    if yhit < pole_size:
        around_last_computer_hit_set.add((xhit, yhit+1))


def check_hit_or_miss(fired_block, opponents_ships, computer_queue):
    global around_last_computer_hit_set

    for opponents_ship in opponents_ships:
        if fired_block in opponents_ship.get_coords():
            opponents_ship.hit_the_ship(fired_block)

            if computer_queue:
                add_exceptions(fired_block, player)
                if not around_last_computer_hit_set:
                    calculation_coords(fired_block)
                else:
                    computer_available_to_fire_set.discard(fired_block)
                ruined_decks_of_player_ships.append(fired_block)
            else:
                ruined_decks_of_computer_ships.append(fired_block)
            return True

    return False


def add_exceptions(fired_block, player):
    global exceptions, computer_available_to_fire_set
    x, y = fired_block
    if 0 < x and 0 < y:
        computer_available_to_fire_set.discard((x-1, y-1))
    if x < pole_size and y < pole_size:
        computer_available_to_fire_set.discard((x+1, y+1))
    if x < pole_size and 0 < y:
        computer_available_to_fire_set.discard((x+1, y-1))
    if 0 < x and y < pole_size:
        computer_available_to_fire_set.discard((x-1, y+1))
    for ship in player._ships:
        assay = [2 for x in range(ship._length)]
        if assay == ship._cells:
            for deck in ship.get_coords():
                x, y = deck
                if (x, y) == (ship._x, ship._y):
                    if 0 < x:
                        computer_available_to_fire_set.discard((x - 1, y))
                    if x < pole_size:
                        computer_available_to_fire_set.discard((x + 1, y))
                    if 0 < y:
                        computer_available_to_fire_set.discard((x, y - 1))
                    if y < pole_size:
                        computer_available_to_fire_set.discard((x, y + 1))


def draw_ruined_players_deck(ruined_decks_of_players_ships):
    for deck in ruined_decks_of_players_ships:
        x_start, y_start = deck
        x = block_sz * x_start + left_mn
        x += (pole_size + indent) * block_sz
        y = block_sz * y_start + upper_mn
        pygame.draw.rect(screen, PINK, ((x, y), (block_sz, block_sz)))


def draw_ruined_computers_deck(ruined_decks_of_computers_ships):
    for deck in ruined_decks_of_computers_ships:
        x_start, y_start = deck
        x = block_sz * x_start + left_mn
        y = block_sz * y_start + upper_mn
        pygame.draw.rect(screen, PINK, ((x, y), (block_sz, block_sz)))


def draw_ruined_ships(participant):
    global computer_win, player_win
    ruined_ships = 0
    for ship in participant._ships:
        assay = [2 for x in range(ship._length)]
        if assay == ship._cells:
            ruined_ships += 1
            for deck in ship.get_coords():
                x_start, y_start = deck
                x = block_sz * x_start + left_mn
                if participant == player:
                    x += (pole_size + indent) * block_sz
                y = block_sz * y_start + upper_mn
                pygame.draw.rect(screen, RED, ((x, y), (block_sz, block_sz)))
            if ruined_ships == 10 and participant == player:
                computer_win = True
            if ruined_ships == 10 and participant == computer:
                player_win = True


def show_message_at_rect_center(message, rect, which_font=font, color=RED):
    message_width, message_height = which_font.size(message)
    message_rect = pygame.Rect(rect)
    x_start = message_rect.centerx - message_width / 2
    y_start = message_rect.centery - message_height / 2
    background_rect = pygame.Rect(
        x_start - block_sz / 2, y_start, message_width + block_sz, message_height)
    message_to_blit = which_font.render(message, True, color)
    screen.fill(WHITE, background_rect)
    screen.blit(message_to_blit, (x_start, y_start))


def draw_field():
    screen.fill(WHITE)
    draw_pole()
    # draw_ships(computer.get_ships())
    draw_ships(player.get_ships())
    draw_ruined_players_deck(ruined_decks_of_player_ships)
    draw_ruined_computers_deck(ruined_decks_of_computer_ships)
    draw_ruined_ships(computer)
    draw_ruined_ships(player)
    if player_win:
        show_message_at_rect_center("ВЫ ВЫИГРАЛИ!", (0, 0, window_size[0], window_size[1]), game_over_font)
    if computer_win:
        show_message_at_rect_center("ВЫ ПРОИГРАЛИ!", (0, 0, window_size[0], window_size[1]), game_over_font)
    pygame.display.update()


def main():
    game_over = False
    computer_queue = False
    draw_field()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif not computer_queue and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (left_mn <= math.floor(x) <= left_mn + pole_size * block_sz and
                        upper_mn <= math.floor(y) <= upper_mn + pole_size * block_sz):
                    fired_block = (math.floor(x) - left_mn) // block_sz, (math.floor(y) - upper_mn) // block_sz
                computer_queue = not check_hit_or_miss(fired_block, computer_ships_working(), computer_queue)
                draw_ruined_computers_deck(ruined_decks_of_computer_ships)
                computer.move_ships()

            elif computer_queue:
                if around_last_computer_hit_set:
                    computer_queue = computer_shoots(around_last_computer_hit_set)
                    if computer_queue:
                        around_last_computer_hit_set.clear()
                else:
                    computer_queue = computer_shoots(computer_available_to_fire_set)
                draw_ruined_players_deck(ruined_decks_of_player_ships)
                player.move_ships()

        draw_field()


main()
pygame.quit()

