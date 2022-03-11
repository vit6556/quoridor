import bot, pygame, sys
from copy import deepcopy

screen_width = 630
screen_height = 550
putted = []


def user_go(pole, screen, first_put, second_put, player):
    global putted
    gone = False
    if player == 1:
        amount_of_putted = first_put
    else:
        amount_of_putted = second_put
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                pygame.draw.rect(screen, (255, 255, 255), (220, 150, 200, 250), 0)
                pygame.draw.rect(screen, (255, 0, 0), (245, 200, 150, 50), 0)
                pygame.draw.rect(screen, (255, 0, 0), (245, 300, 150, 50), 0)
                f1 = pygame.font.Font(None, 25)
                text1 = f1.render("Заново", 1, (255, 255, 255))
                text2 = f1.render("Выйти", 1, (255, 255, 255))
                screen.blit(text1, (295, 215))
                screen.blit(text2, (297, 315))
                pygame.display.flip()
                exit = False
                while not exit:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            x, y = event.pos
                            if x >= 245 and x <= 395 and y >= 200 and y <= 250:
                                return -2, gone, first_put, second_put
                            elif x >= 245 and x <= 395 and y >= 300 and y <= 350:
                                return -3, gone, first_put, second_put
                        if event.type == pygame.QUIT:
                            sys.exit(0)
                        if event.type == pygame.KEYDOWN:
                            if event.key == 27:
                                exit = True
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = find_cords_from_pos(pygame.mouse.get_pos())
            if x < 0 or y < 0:
                if amount_of_putted >= 10:
                    return player, gone, first_put, second_put
                x, y = find_wall_cords_from_pos(pygame.mouse.get_pos(), 'h')
                if x < 0 or y < 0:
                    x, y = find_wall_cords_from_pos(pygame.mouse.get_pos(), 'v')
                    if x >= 0 and y >= 0:
                        if len(putted) == 0:
                            if pole.pole[x][y] != '#':
                                putted.append([x, y])
                        elif putted[0][0] == x and putted[0][1] == y:
                            putted = []
                        else:
                            if check_v(putted[0]) == False and abs(putted[0][0] - x) == 2 and abs(
                                    putted[0][1] - y) == 0 and pole.pole[(putted[0][0] + x) // 2][
                                (putted[0][1] + y) // 2] != '#' and check_put(pole, (putted[0][0] + x) // 2,
                                                                              (putted[0][1] + y) // 2, 'v') and \
                                    pole.pole[x][y] != '#':
                                pole.pole[x][y] = '#'
                                pole.pole[putted[0][0]][putted[0][1]] = '#'
                                pole.pole[(putted[0][0] + x) // 2][(putted[0][1] + y) // 2] = '#'
                                putted = []
                                if player == 1:
                                    first_put += 1
                                else:
                                    second_put += 1
                                gone = True
                            else:
                                if pole.pole[x][y] != '#':
                                    putted = [[x, y]]
                else:
                    if len(putted) == 0:
                        if pole.pole[x][y] != '#':
                            putted.append([x, y])
                    elif putted[0][0] == x and putted[0][1] == y:
                        putted = []
                    else:
                        if check_v(putted[0]) == False and abs(putted[0][0] - x) == 0 and abs(
                                putted[0][1] - y) == 2 and pole.pole[(putted[0][0] + x) // 2][
                            (putted[0][1] + y) // 2] != '#' and check_put(pole, (putted[0][0] + x) // 2,
                                                                          (putted[0][1] + y) // 2, 'h') and \
                                pole.pole[x][y] != '#':
                            pole.pole[x][y] = '#'
                            pole.pole[putted[0][0]][putted[0][1]] = '#'
                            pole.pole[(putted[0][0] + x) // 2][(putted[0][1] + y) // 2] = '#'
                            putted = []
                            gone = True
                            if player == 1:
                                first_put += 1
                            else:
                                second_put += 1
                        else:
                            if pole.pole[x][y] != '#':
                                putted = [[x, y]]

            else:
                x1, y1 = find_player(player, pole)
                if x1 - x == 2 and y == y1:
                    if go(pole, 'u', player) != -1:
                        putted = []
                        gone = True
                elif x - x1 == 2 and y == y1:
                    if go(pole, 'd', player) != -1:
                        putted = []
                        gone = True
                elif y - y1 == 2 and x == x1:
                    if go(pole, 'r', player) != -1:
                        putted = []
                        gone = True
                elif y1 - y == 2 and x == x1:
                    if go(pole, 'l', player) != -1:
                        putted = []
                        gone = True
                elif y1 - y == 4 and x == x1 and pole.pole[x][y + 2] == str(player % 2 + 1) and pole.pole[x][
                    y + 1] != '#' and pole.pole[x][y + 3] != '#':
                    pole.pole[x][y] = str(player)
                    pole.pole[x][y1] = '*'
                    putted = []
                    gone = True
                elif y - y1 == 4 and x == x1 and pole.pole[x][y - 2] == str(player % 2 + 1) and pole.pole[x][
                    y - 1] != '#' and pole.pole[x][y - 3] != '#':
                    pole.pole[x][y] = str(player)
                    pole.pole[x][y1] = '*'
                    putted = []
                    gone = True
                elif x1 - x == 4 and y == y1 and pole.pole[x + 2][y] == str(player % 2 + 1) and pole.pole[x + 1][
                    y] != '#' and pole.pole[x + 3][y] != '#':
                    pole.pole[x][y] = str(player)
                    pole.pole[x1][y] = '*'
                    putted = []
                    gone = True
                elif x - x1 == 4 and y == y1 and pole.pole[x - 2][y] == str(player % 2 + 1) and pole.pole[x - 1][
                    y] != '#' and pole.pole[x - 3][
                    y] != '#':
                    pole.pole[x][y] = str(player)
                    pole.pole[x1][y] = '*'
                    putted = []
                    gone = True
                elif x1 - x == 2 and y1 - y == 2:
                    if pole.pole[x1 - 2][y1] != '*' and pole.pole[x1 - 1][y1] != '#' and pole.pole[x1 - 3][y1] == '#' \
                            and pole.pole[x1 - 2][y1 - 1] != '#':
                        pole.pole[x][y] = str(player)
                        pole.pole[x1][y1] = '*'
                        putted = []
                        gone = True
                    if pole.pole[x1][y1 - 2] != '*' and pole.pole[x1][y1 - 1] != '#' and pole.pole[x1][y1 - 3] == '#' \
                            and pole.pole[x1 - 1][y1 - 2] != '#':
                        pole.pole[x][y] = str(player)
                        pole.pole[x1][y1] = '*'
                        putted = []
                        gone = True
                elif x1 - x == 2 and y - y1 == 2:
                    if pole.pole[x1 - 2][y1] != '*' and pole.pole[x1 - 1][y1] != '#' and pole.pole[x1 - 3][y1] == '#'\
                            and pole.pole[x1 - 2][y1 + 1] != '#':
                        pole.pole[x][y] = str(player)
                        pole.pole[x1][y1] = '*'
                        putted = []
                        gone = True
                    if pole.pole[x1][y1 + 2] != '*' and pole.pole[x1][y1 + 1] != '#' and pole.pole[x1][y1 + 3] == '#'\
                            and pole.pole[x1 - 1][y1 + 2] != '#':
                        pole.pole[x][y] = str(player)
                        pole.pole[x1][y1] = '*'
                        putted = []
                        gone = True
                elif x - x1 == 2 and y1 - y == 2:
                    if pole.pole[x1 + 2][y1] != '*' and pole.pole[x1 + 1][y1] != '#' and pole.pole[x1 + 3][y1] == '#'\
                            and pole.pole[x1 + 2][y1 - 1] != '#':
                        pole.pole[x][y] = str(player)
                        pole.pole[x1][y1] = '*'
                        putted = []
                        gone = True
                    if pole.pole[x1][y1 - 2] != '*' and pole.pole[x1][y1 - 1] != '#' and pole.pole[x1][y1 - 3] == '#'\
                            and pole.pole[x1 + 1][y1 - 2] != '#':
                        pole.pole[x][y] = str(player)
                        pole.pole[x1][y1] = '*'
                        putted = []
                        gone = True
                elif x - x1 == 2 and y - y1 == 2:
                    if pole.pole[x1 + 2][y1] != '*' and pole.pole[x1 + 1][y1] != '#' and pole.pole[x1 + 3][y1] == '#'\
                            and pole.pole[x1 + 2][y1 + 1] != '#':
                        pole.pole[x][y] = str(player)
                        pole.pole[x1][y1] = '*'
                        putted = []
                        gone = True
                    if pole.pole[x1][y1 + 2] != '*' and pole.pole[x1][y1 + 1] != '#' and pole.pole[x1][y1 + 3] == '#'\
                            and pole.pole[x1 + 1][y1 + 2] != '#':
                        pole.pole[x][y] = str(player)
                        pole.pole[x1][y1] = '*'
                        putted = []
                        gone = True
            if check_win(pole, screen):
                return -1, gone, first_put, second_put
    draw(pole, screen, first_put, second_put, player)
    if gone:
        if player == 2:
            player = 1
        else:
            player = 2
    return player, gone, first_put, second_put


def main():
    global putted
    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])  # , pygame.FULLSCREEN)
    while True:
        pole = Pole()
        pole.generate_pole(9)
        res = draw_buttons(screen)
        while res == -1:
            res = draw_buttons(screen)
        if res == 2:
            again = False
            while not again:
                draw(pole, screen, 0, 0, 1)
                player = 1
                first_put = 0
                second_put = 0
                while True:
                    player, gone, first_put, second_put = user_go(pole, screen, first_put, second_put, player)
                    if player == -1 or player == -3:
                        putted = []
                        again = True
                        break
                    elif player == -2:
                        pole = Pole()
                        pole.generate_pole(9)
                        putted = []
                        break
        else:
            again = False
            while not again:
                bot.bot_put = 0
                bot.user_put = 0
                draw(pole, screen, 0, 0, 1)
                while True:
                    player, gone, first_put, second_put = user_go(pole, screen, bot.user_put, bot.bot_put, 1)
                    if player == -1 or player == -3:
                        again = True
                        putted = []
                        break
                    elif player == -2:
                        pole = Pole()
                        pole.generate_pole(9)
                        putted = []
                        break
                    bot.bot_put = second_put
                    bot.user_put = first_put
                    if gone:
                        bot.bot(pole)
                        if check_win(pole, screen):
                            break


def go(pole, where, player):
    x, y = find_player(player, pole)
    where = where[:1]
    if where == 'u':
        if x <= 1:
            return -1
        elif pole.pole[x - 2][y] == '*' and pole.pole[x - 1][y] != '#':
            pole.pole[x][y] = '*'
            pole.pole[x - 2][y] = str(player)
            return 1
        else:
            return -1
    elif where == 'd':
        if x >= len(pole.pole[0]) - 2:
            return -1
        elif pole.pole[x + 2][y] == '*' and pole.pole[x + 1][y] != '#':
            pole.pole[x][y] = '*'
            pole.pole[x + 2][y] = str(player)
            return 1
        else:
            return -1
    elif where == 'l':
        if y <= 1:
            return -1
        elif pole.pole[x][y - 2] == '*' and pole.pole[x][y - 1] != '#':
            pole.pole[x][y] = '*'
            pole.pole[x][y - 2] = str(player)
            return 1
        else:
            return -1
    elif where == 'r':
        if y >= len(pole.pole[0]) - 2:
            return -1
        elif pole.pole[x][y + 2] == '*' and pole.pole[x][y + 1] != '#':
            pole.pole[x][y] = '*'
            pole.pole[x][y + 2] = str(player)
            return 1
        else:
            return -1
    return -1


def check_v(pos):
    answer_x = -1
    answer_y = -1
    for i in range(8):
        if pos[0] >= 60 + 60 * i and pos[0] <= 70 + 60 * i:
            answer_x = i
    for i in range(9):
        if pos[1] >= 10 + 60 * i and pos[1] <= 60 + 60 * i:
            answer_y = i
    if answer_y < 0 or answer_x < 0:
        return False
    else:
        return True


def find_cords_from_pos(pos):
    answer_x = -1
    answer_y = -1
    for i in range(9):
        if pos[0] >= 10 + 60 * i and pos[0] <= 60 + 60 * i:
            answer_x = i
    for i in range(9):
        if pos[1] >= 10 + 60 * i and pos[1] <= 60 + 60 * i:
            answer_y = i
    return answer_y * 2, answer_x * 2


def find_wall_cords_from_pos(pos, orintation):
    answer_x = -1
    answer_y = -1
    if orintation == 'v':
        for i in range(8):
            if pos[0] >= 60 + 60 * i and pos[0] <= 70 + 60 * i:
                answer_x = i
        for i in range(9):
            if pos[1] >= 10 + 60 * i and pos[1] <= 60 + 60 * i:
                answer_y = i
        return answer_y * 2, answer_x * 2 + 1
    else:
        for i in range(8):
            if pos[1] >= 60 + 60 * i and pos[1] <= 70 + 60 * i:
                answer_y = i
        for i in range(9):
            if pos[0] >= 10 + 60 * i and pos[0] <= 60 + 60 * i:
                answer_x = i
        return answer_y * 2 + 1, answer_x * 2


def find_player(player, pole):
    for i in range(len(pole.pole)):
        for j in range(len(pole.pole)):
            if pole.pole[i][j] == str(player):
                return i, j


def check_put(pole, x, y, orintation):
    current_pole = deepcopy(pole.pole)
    current_pole[x][y] = '#'
    if orintation == 'h':
        current_pole[x][y + 1] = '#'
        current_pole[x][y - 1] = '#'
    elif orintation == 'v':
        current_pole[x + 1][y] = '#'
        current_pole[x - 1][y] = '#'
    way = False
    ways = []
    for i in range(9):
        for_ways = []
        for j in range(9):
            for_ways.append(999999)
        ways.append(for_ways)
    m, n = find_player(1, pole)
    ways[m // 2][n // 2] = 0
    way_exist(ways, current_pole, m, n)
    for i in range(9):
        if ways[0][i] != 999999:
            way = True
            break
    if not way:
        return False
    ways = []
    for i in range(9):
        for_ways = []
        for j in range(9):
            for_ways.append(999999)
        ways.append(for_ways)
    m, n = find_player(2, pole)
    ways[m // 2][n // 2] = 0
    way_exist(ways, current_pole, m, n)
    way = False
    for i in range(9):
        if ways[8][i] != 999999:
            way = True
            break
    if not way:
        return False
    else:
        return True


def way_exist(ways, pole, x, y):
    if x >= 2:
        if pole[x - 1][y] != '#':
            if ways[(x - 2) // 2][y // 2] > ways[x // 2][y // 2] + 1:
                ways[(x - 2) // 2][y // 2] = ways[x // 2][y // 2] + 1
                way_exist(ways, pole, x - 2, y)
    if x <= 14:
        if pole[x + 1][y] != '#':
            if ways[(x + 2) // 2][y // 2] > ways[x // 2][y // 2] + 1:
                ways[(x + 2) // 2][y // 2] = ways[x // 2][y // 2] + 1
                way_exist(ways, pole, x + 2, y)
    if y <= 14:
        if pole[x][y + 1] != '#':
            if ways[x // 2][(y + 2) // 2] > ways[x // 2][y // 2] + 1:
                ways[x // 2][(y + 2) // 2] = ways[x // 2][y // 2] + 1
                way_exist(ways, pole, x, y + 2)
    if y >= 2:
        if pole[x][y - 1] != '#':
            if ways[x // 2][(y - 2) // 2] > ways[x // 2][y // 2] + 1:
                ways[x // 2][(y - 2) // 2] = ways[x // 2][y // 2] + 1
                way_exist(ways, pole, x, y - 2)
    return


def draw(pole, screen, first_put, second_put, player):
    global putted
    screen.fill((10, 10, 10))
    for i in range(9):
        y1 = 60 * i + 10
        for j in range(9):
            x1 = 60 * j + 10
            pygame.draw.rect(screen, (112, 84, 62), (y1, x1, 50, 50), 0)
    for i in range(len(pole.pole)):
        for j in range(len(pole.pole)):
            if pole.pole[i][j] == '#':
                if i % 2 != 0 and j % 2 != 0:
                    pygame.draw.rect(screen, (141, 104, 21), (j * 30 + 30, i * 30 + 30, 10, 10), 0)
                elif i % 2 == 0:
                    pygame.draw.rect(screen, (141, 104, 21), (j * 30 + 30, i * 30 + 10, 10, 50), 0)
                else:
                    pygame.draw.rect(screen, (141, 104, 21), (j * 30 + 10, i * 30 + 30, 50, 10), 0)
            elif pole.pole[i][j] == '1':
                pygame.draw.circle(screen, (0, 0, 255), (j * 30 + 35, i * 30 + 35,), 20, 0)
            elif pole.pole[i][j] == '2':
                pygame.draw.circle(screen, (255, 0, 0), (j * 30 + 35, i * 30 + 35,), 20, 0)
    for i in putted:
        if i[0] % 2 == 0:
            pygame.draw.rect(screen, (0, 255, 0), (i[1] * 30 + 30, i[0] * 30 + 10, 10, 50), 0)
        else:
            pygame.draw.rect(screen, (0, 255, 0), (i[1] * 30 + 10, i[0] * 30 + 30, 50, 10), 0)
    pygame.draw.rect(screen, (255, 0, 0), (550, 20, 30, 10), 0)
    pygame.draw.rect(screen, (0, 0, 255), (550, 60, 30, 10), 0)
    f1 = pygame.font.Font(None, 20)
    text1 = f1.render(str(10 - second_put), 1, (255, 255, 255))
    text2 = f1.render(str(10 - first_put), 1, (255, 255, 255))
    if player == 1:
        text3 = f1.render('Ход', 1, (0, 0, 255))
        screen.blit(text3, (572, 100))
        text4 = f1.render('cиних', 1, (0, 0, 255))
        screen.blit(text4, (566, 120))
    else:
        text3 = f1.render('Ход', 1, (255, 0, 0))
        screen.blit(text3, (572, 100))
        text4 = f1.render('красных', 1, (255, 0, 0))
        screen.blit(text4, (560, 120))
    screen.blit(text1, (590, 20))
    screen.blit(text2, (590, 60))
    pygame.display.flip()


def buttons(screen):
    pygame.draw.rect(screen, (50, 50, 50), (230, 230, 150, 40), 0)
    pygame.draw.rect(screen, (220, 0, 0), (230, 320, 150, 40), 0)
    pygame.draw.circle(screen, (220, 0, 0), (615, 535), 10, 0)
    f1 = pygame.font.Font(None, 30)
    f2 = pygame.font.Font(None, 70)
    f3 = pygame.font.Font(None, 20)
    text1 = f1.render('1 player', 1, (255, 255, 255))
    text2 = f1.render('2 players', 1, (255, 255, 255))
    text3 = f2.render('QUORIDOR', 1, (255, 255, 255))
    text4 = f3.render('?', 1, (255, 255, 255))
    screen.blit(text1, (267, 240))
    screen.blit(text2, (263, 330))
    screen.blit(text3, (176, 100))
    screen.blit(text4, (611, 529))


def draw_buttons(screen):
    screen.fill((20, 20, 20))
    buttons(screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x <= 370 and x >= 230 and y <= 360 and y >= 320:
                    return 2
                # elif x <= 370 and x >= 230 and y <= 270 and y >= 230:
                #    screen.fill((20, 20, 20))
                #    f1 = pygame.font.Font(None, 25)
                #    text1 = f1.render("Этот режим находится в разработке, поэтому может работать нестабильно", 1,
                #                      (255, 255, 255))
                #    text2 = f1.render("Вы уверены, что хотите продолжить?", 1, (255, 255, 255))
                #    text3 = f1.render("Да", 1, (255, 255, 255))
                #    text4 = f1.render("Нет", 1, (255, 255, 255))
                #    screen.blit(text1, (10, 275))
                #    screen.blit(text2, (155, 295))
                #    pygame.draw.rect(screen, (220, 0, 0), (200, 335, 70, 30), 0)
                #    pygame.draw.rect(screen, (220, 0, 0), (350, 335, 70, 30), 0)
                #    screen.blit(text3, (220, 343))
                #    screen.blit(text4, (372, 343))
                #    pygame.display.flip()
                #    pressed = False
                #    while not pressed:
                #        for event in pygame.event.get():
                #            if event.type == pygame.QUIT:
                #                sys.exit(0)
                #            if event.type == pygame.MOUSEBUTTONDOWN:
                #                x, y = event.pos
                #                if x <= 270 and x >= 200 and y >= 335 and y <= 365:
                #                    pressed = True
                #                elif x <= 420 and x >= 350 and y >= 335 and y <= 365:
                #                    return -1
                #    return 1
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if x >= 605 and x <= 625 and y >= 525 and y <= 545:
                    screen.fill((20, 20, 20))
                    pygame.draw.rect(screen, (255, 255, 255), (410, 475, 200, 50), 0)
                    f1 = pygame.font.Font(None, 25)
                    text1 = f1.render('Компьютерная версия', 1, (0, 0, 0))
                    text2 = f1.render('настольной игры', 1, (0, 0, 0))
                    text3 = f1.render('Коридор', 1, (0, 0, 0))
                    screen.blit(text1, (415, 475))
                    screen.blit(text2, (415, 490))
                    screen.blit(text3, (415, 505))
                    buttons(screen)
                    pygame.display.flip()
                elif x >= 230 and x <= 380 and y >= 230 and y <= 270:
                    screen.fill((20, 20, 20))
                    buttons(screen)
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, 130, 25), 0)
                    f1 = pygame.font.Font(None, 25)
                    text1 = f1.render('Coming soon...', 1, (0, 0, 0))
                    screen.blit(text1, (x + 5, y + 5))
                    pygame.display.flip()
                else:
                    screen.fill((20, 20, 20))
                    buttons(screen)
                    pygame.display.flip()



class Pole:
    def __init__(self):
        self.pole = []

    def generate_pole(self, size_of_pole):
        for i in range(size_of_pole * 2):
            line = []
            if i % 2 == 0:
                for j in range(size_of_pole * 2):
                    if j % 2 == 0:
                        line.append('*')
                    else:
                        line.append(' ')
                self.pole.append(line)
            else:
                for j in range(size_of_pole * 2):
                    line.append(' ')
                self.pole.append(line)
        self.pole[0][8] = '2'
        self.pole[16][8] = '1'


def check_win(pole, screen):
    x, y = find_player(1, pole)
    if x == 0:
        screen.fill((20, 20, 20))
        f1 = pygame.font.Font(None, 35)
        f2 = pygame.font.Font(None, 25)
        text1 = f1.render("Синий победил", 1, (0, 0, 255))
        text2 = f2.render("Выйти в меню", 1, (255, 255, 255))
        pygame.draw.rect(screen, (220, 0, 0), (253, 250, 130, 30), 0)
        screen.blit(text1, (225, 200))
        screen.blit(text2, (264, 255))
        pygame.display.flip()
        pressed = False
        while not pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x <= 383 and x >= 253 and y >= 250 and y <= 280:
                        return True
    x, y = find_player(2, pole)
    if x == 16:
        screen.fill((20, 20, 20))
        f1 = pygame.font.Font(None, 35)
        f2 = pygame.font.Font(None, 25)
        text1 = f1.render("Красный победил", 1, (255, 0, 0))
        text2 = f2.render("Выйти в меню", 1, (255, 255, 255))
        pygame.draw.rect(screen, (220, 0, 0), (253, 250, 130, 30), 0)
        screen.blit(text1, (210, 200))
        screen.blit(text2, (262, 255))
        pygame.display.flip()
        pressed = False
        while not pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x <= 383 and x >= 253 and y >= 250 and y <= 280:
                        return True


if __name__ == '__main__':
    main()
