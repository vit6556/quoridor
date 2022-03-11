import play, random

user_put = 0
bot_put = 0

def bot(pole):
    global bot_put
    user_way = find_way(pole, 1)[::-1]
    bot_way = find_way(pole, 2)[::-1]
    if len(user_way) < len(bot_way) and bot_put < 11:
        x, y = play.find_player(1, pole)
        for i in range(len(user_way)):
            if user_way[i] == 'r':
                user_way[i] = 'l'
            elif user_way[i] == 'l':
                user_way[i] = 'r'
            elif user_way[i] == 'u':
                user_way[i] = 'd'
            elif user_way[i] == 'd':
                user_way[i] = 'u'
        global found
        found = False
        if place_wall(pole, user_way, x - 1, y) != -1:
            bot_put += 1
            return 0
        else:
            go(pole, bot_way[0])
    else:
        go(pole, bot_way[0])

found = False

def place_wall(pole, user_way, x, y):
    global found
    if found:
        return 0
    for direction in user_way:
        if x > 0:
            if direction == 'u':
                if put(pole, x, y + 1, 'h') != -1:
                    found = True
                    return 0
                elif y > 0:
                    if put(pole, x, y - 1, 'h') != -1:
                        found = True
                        return 0
                elif put(pole, x, y + 1, 'v') != -1:
                    found = True
                    return 0
                elif put(pole, x, y - 1, 'v') != -1:
                    found = True
                    return 0
                else:
                    user_way = user_way[1:]
                    go(pole, 'u')
                    place_wall(pole, user_way, x - 1, y)
        if y > 0:
            if direction == 'r':
                if put(pole, x, y + 1, 'h') != -1:
                    found = True
                    return 0
                elif put(pole, x, y - 1, 'h') != -1:
                    found = True
                    return 0
                elif put(pole, x, y + 1, 'v') != -1:
                    found = True
                    return 0
                elif put(pole, x, y - 1, 'v') != -1:
                    found = True
                    return 0
                else:
                    user_way = user_way[1:]
                    go(pole, 'r')
                    place_wall(pole, user_way, x, y - 1)
        if x < 17:
            if direction == 'd':
                if put(pole, x, y + 1, 'h') != -1:
                    found = True
                    return 0
                elif put(pole, x, y - 1, 'h') != -1:
                    found = True
                    return 0
                elif put(pole, x, y + 1, 'v') != -1:
                    found = True
                    return 0
                elif put(pole, x, y - 1, 'v') != -1:
                    found = True
                    return 0
                else:
                    user_way = user_way[1:]
                    go(pole, 'd')
                    place_wall(pole, user_way, x + 1, y)
        if y < 17:
            if direction == 'l':
                if put(pole, x, y + 1, 'h') != -1:
                    found = True
                    return 0
                elif put(pole, x, y - 1, 'h') != -1:
                    found = True
                    return 0
                elif put(pole, x, y + 1, 'v') != -1:
                    found = True
                    return 0
                elif put(pole, x, y - 1, 'v') != -1:
                    found = True
                    return 0
                else:
                    user_way = user_way[1:]
                    go(pole, 'l')
                    place_wall(pole, user_way, x, y + 1)
    return -1


def find_way(pole, player):
    ways = []
    for i in range(9):
        for_ways = []
        for j in range(9):
            for_ways.append(999999)
        ways.append(for_ways)
    m, n = play.find_player(player, pole)
    ways[m // 2][n // 2] = 0
    way_exist(ways, pole.pole, m, n)
    min_way = 9999
    min_index = 0
    if player == 2:
        for i in range(len(ways)):
            if min_way > ways[8][i]:
                min_way = ways[8][i]
                min_index = i
        way = []
        way = get_way(ways, 8, min_index, way, pole.pole, player)
    else:
        for i in range(len(ways)):
            if min_way > ways[0][i]:
                min_way = ways[0][i]
                min_index = i
        way = []
        way = get_way(ways, 0, min_index, way, pole.pole, player)
    return way

def get_way(ways, x, y, way, pole, player):
    find = False
    if y > 0 and not find:
        if pole[x * 2][y * 2] != str(player % 2 + 1):
            if ways[x][y - 1] + 1 == ways[x][y] and pole[x * 2][y * 2 - 1] != '#':
                way.append('l')
                find = True
                return get_way(ways, x, y - 1, way, pole, player)
            elif pole[x * 2][(y - 1) * 2] == str(player):
                way.append('l')
                find = True
        else:
            way.append('l')
            find = True
            return get_way(ways, x, y - 1, way, pole, player)
    if y < 8 and not find:
        if pole[x * 2][y * 2] != str(player % 2 + 1):
            if ways[x][y + 1] + 1 == ways[x][y] and pole[x * 2][y * 2 + 1] != '#':
                way.append('r')
                find = True
                return get_way(ways, x, y + 1, way, pole, player)
            elif pole[x * 2][(y + 1) * 2] == str(player):
                way.append('r')
                find = True
        else:
            way.append('r')
            find = True
            return get_way(ways, x, y + 1, way, pole, player)
    if x > 0 and not find:
        if pole[x * 2][y * 2] != str(player % 2 + 1):
            if ways[x - 1][y] + 1 == ways[x][y] and pole[x * 2 -1][y * 2] != '#':
                way.append('u')
                find = True
                return get_way(ways, x-1, y, way, pole, player)
            elif pole[(x - 1) * 2][y * 2] == str(player):
                way.append('u')
                find = True
        else:
            way.append('u')
            find = True
            return get_way(ways, x - 1, y, way, pole, player)
    if x < 8 and not find:
        if pole[x * 2][y * 2] != str(player % 2 + 1):
            if ways[x + 1][y] + 1 == ways[x][y] and pole[x * 2 + 1][y * 2] != '#':
                way.append('d')
                find = True
                return get_way(ways, x+1, y, way, pole, player)
            elif pole[(x + 1) * 2][y * 2] == str(player):
                way.append('d')
                find = True
        else:
            way.append('d')
            find = True
            return get_way(ways, x + 1, y, way, pole, player)
    return way



def put(pole, a, b, orintation):
    if pole.pole[a][b] != ' ':
        return -1
    else:
        if orintation == 'h':
            try:
                if pole.pole[a][b + 1] == '#' or pole.pole[a][b - 1] == '#':
                    return -1
            except:
                return -1
            if not play.check_put(pole, a, b, orintation):
                return -1
            pole.pole[a][b + 1] = '#'
            pole.pole[a][b - 1] = '#'
            pole.pole[a][b] = '#'
            return 1
        elif orintation == 'v':
            try:
                if pole.pole[a + 1][b] == '#' or pole.pole[a - 1][b] == '#':
                    return -1
            except:
                return -1
            if not play.check_put(pole, a, b, orintation):
                return -1
            pole.pole[a + 1][b] = '#'
            pole.pole[a - 1][b] = '#'
            pole.pole[a][b] = '#'
            return 1
    return -1

def go(pole, where):
    x, y = play.find_player(2, pole)
    where = where[:1]
    if where == 'd':
        if x <= 1:
            return -1
        elif pole.pole[x - 2][y] == '*' and pole.pole[x - 1][y] != '#':
            pole.pole[x][y] = '*'
            pole.pole[x - 2][y] = '2'
            return 1
        else:
            return -1
    elif where == 'u':
        if x >= len(pole.pole[0]) - 2:
            return -1
        elif pole.pole[x + 2][y] == '*'  and pole.pole[x + 1][y] != '#':
            pole.pole[x][y] = '*'
            pole.pole[x + 2][y] = '2'
            return 1
        else:
            return -1
    elif where == 'r':
        if y <= 1:
            return -1
        elif pole.pole[x][y - 2] == '*' and pole.pole[x][y - 1] != '#':
            pole.pole[x][y] = '*'
            pole.pole[x][y - 2] = '2'
            return 1
        else:
            return -1
    elif where == 'l':
        if y >= len(pole.pole[0]) - 2:
            return -1
        elif pole.pole[x][y + 2] == '*' and pole.pole[x][y + 1] != '#':
            pole.pole[x][y] = '*'
            pole.pole[x][y + 2] = '2'
            return 1
        else:
            return -1
    return -1

def way_exist(ways, pole, x, y):
    if x >= 2:
        if pole[x - 1][y] != '#'and pole[x - 2][y] == '*':
            if ways[(x - 2) // 2][y // 2] > ways[x // 2][y // 2] + 1:
                ways[(x - 2) // 2][y // 2] = ways[x // 2][y // 2] + 1
                way_exist(ways, pole, x - 2, y)
    if x <= 14:
        if pole[x + 1][y] != '#'and pole[x + 2][y] == '*':
            if ways[(x + 2) // 2][y // 2] > ways[x // 2][y // 2] + 1:
                ways[(x + 2) // 2][y // 2] = ways[x // 2][y // 2] + 1
                way_exist(ways, pole, x + 2, y)
    if y <= 14:
        if pole[x][y + 1] != '#'and pole[x][y + 2] == '*':
            if ways[x // 2][(y + 2) // 2] > ways[x // 2][y // 2] + 1:
                ways[x // 2][(y + 2) // 2] = ways[x // 2][y // 2] + 1
                way_exist(ways, pole, x, y + 2)
    if y >= 2:
        if pole[x][y - 1] != '#'and pole[x][y - 2] == '*':
            if ways[x // 2][(y - 2) // 2] > ways[x // 2][y // 2] + 1:
                ways[x // 2][(y - 2) // 2] = ways[x // 2][y // 2] + 1
                way_exist(ways, pole, x, y - 2)
    return