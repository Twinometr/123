class Character:
    def __init__(self, hp, mp, arm, dmg):
        self.hp = hp
        self.mp = mp
        self.arm = arm
        self.dmg = dmg

class Player(Character):
    def __init__(self, hp, mp, arm, dmg):
        super().__init__(hp, mp, arm, dmg)
        self.inventory = []

    def pickup(self, item):
        self.inventory.append(item)
        print(f"Подобран предмет: {item}")

class Enemy(Character):
    pass

def generate_map(size):
    # Deterministic map generation without random module
    game_map = []
    for y in range(size):
        row = []
        for x in range(size):
            if x == 0 or y == 0 or x == size-1 or y == size-1:
                row.append('#')  # Border walls
            else:
                row.append('.')
        game_map.append(row)
    return game_map

def place_entities(game_map, size):
    # Fixed positions for 5x5 map
    if size == 5:
        return (1, 1), (3, 3)
    # Default placement for other sizes
    return (1, 1), (size-2, size-2)

def generate_items(game_map, size):
    # Fixed item position in center
    center = size // 2
    game_map[center][center] = '!'
    return [(center, center)]

def render_map(game_map, pc_pos, npc_pos, items):
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            if (x, y) == pc_pos:
                print('@', end=' ')
            elif (x, y) == npc_pos:
                print('E', end=' ')
            elif (x, y) in items:
                print('!', end=' ')
            else:
                print(game_map[y][x], end=' ')
        print()

def move(direction, position, game_map):
    x, y = position
    new_x, new_y = x, y
    if direction == 'w': new_y -= 1
    elif direction == 's': new_y += 1
    elif direction == 'a': new_x -= 1
    elif direction == 'd': new_x += 1

    if 0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map):
        if game_map[new_y][new_x] != '#':
            return (new_x, new_y)
    return (x, y)

def attack(attacker, defender):
    damage = max(1, attacker.dmg - defender.arm)
    defender.hp -= damage
    print(f"{type(attacker).__name__} наносит {damage} урона! "
          f"Осталось HP: {defender.hp}")

def npc_ai(npc_pos, game_map):
    directions = ['d', 's', 'a', 'w']
    for direction in directions:
        new_pos = move(direction, npc_pos, game_map)
        if new_pos != npc_pos:
            return new_pos
    return npc_pos

def show_debug(pc, npc, items_collected):
    print("\n--- Debug информация ---")
    print(f"PC: HP {pc.hp}, MP {pc.mp}, ARM {pc.arm}, DMG {pc.dmg}")
    print(f"NPC: HP {npc.hp}, MP {npc.mp}, ARM {npc.arm}, DMG {npc.dmg}")
    print(f"Инвентарь: {', '.join(pc.inventory)}")
    print(f"Собрано предметов: {items_collected}")

def main():
    print("Выберите тип карты:")
    print("1. Стандартная карта (5x5)")
    print("2. Сгенерированная карта")
    choice = input("> ")

    if choice == '1':
        game_map = [
            ['#', '#', '#', '#', '#'],
            ['#', '.', '.', '.', '#'],
            ['#', '.', '.', '.', '#'],
            ['#', '.', '.', '.', '#'],
            ['#', '#', '#', '#', '#']
        ]
        size = 5
    else:
        size = int(input("Введите размер карты: "))
        game_map = generate_map(size)

    pc_pos, npc_pos = place_entities(game_map, size)
    items = generate_items(game_map, size)
    items_collected = 0

    player = Player(hp=100, mp=50, arm=10, dmg=15)
    enemy = Enemy(hp=80, mp=30, arm=5, dmg=10)

    while player.hp > 0 and enemy.hp > 0:
        render_map(game_map, pc_pos, npc_pos, items)
        show_debug(player, enemy, items_collected)
        
        action = input("\nДействие (wasd/attack): ").lower()

        if action in ['w', 'a', 's', 'd']:
            new_pos = move(action, pc_pos, game_map)
            if new_pos in items:
                player.pickup("предмет")
                items.remove(new_pos)
                game_map[new_pos[1]][new_pos[0]] = '.'
                items_collected += 1
            pc_pos = new_pos

        elif action == 'attack':
            if pc_pos == npc_pos:
                attack(player, enemy)
            else:
                print("Слишком далеко для атаки!")

        # NPC movement
        npc_pos = npc_ai(npc_pos, game_map)
        if pc_pos == npc_pos:
            attack(enemy, player)

        # Check game over
        if player.hp <= 0:
            print("Вы проиграли!")
            break
        if enemy.hp <= 0:
            print("Вы победили!")
            break

if __name__ == "__main__":
    main()