class Entity:
    def __init__(self, name, hp, mp, armor, damage, x=0, y=0):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.armor = armor
        self.damage = damage
        self.x = x
        self.y = y
        self.inventory = []
        self.seed = (x + y) * 12345  # Простое начальное значение для генерации
    
    def move(self, dx, dy, game_map):
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map):
            if game_map[new_y][new_x] != '#':
                self.x, self.y = new_x, new_y
                return True
        return False
    
    def attack(self, target):
        damage_dealt = max(1, self.damage - target.armor // 2)
        target.hp -= damage_dealt
        return damage_dealt
    
    def is_alive(self):
        return self.hp > 0
    
    def add_to_inventory(self, item):
        self.inventory.append(item)
    
    def use_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if item.type == "heal":
                self.hp = min(self.max_hp, self.hp + item.value)
                print(f"{self.name} использовал {item.name} и восстановил {item.value} HP!")
            elif item.type == "mana":
                self.mp = min(self.max_mp, self.mp + item.value)
                print(f"{self.name} использовал {item.name} и восстановил {item.value} MP!")
            self.inventory.pop(item_index)
            return True
        return False
    
    def simple_random(self):
        # Простейший генератор псевдослучайных чисел
        self.seed = (self.seed * 1103515245 + 12345) & 0x7fffffff
        return self.seed / 2147483647

class Item:
    def __init__(self, name, item_type, value, x=None, y=None):
        self.name = name
        self.type = item_type
        self.value = value
        self.x = x
        self.y = y

class Quest:
    def __init__(self, name, description, target, reward, completed=False):
        self.name = name
        self.description = description
        self.target = target
        self.reward = reward
        self.completed = completed
        self.progress = {k: 0 for k in self.target.keys()}

class Game:
    def __init__(self):
        self.player = None
        self.enemies = []
        self.items = []
        self.quests = []
        self.current_location = "village"
        self.locations = {}
        self.load_locations()
        self.game_map = self.locations[self.current_location]["map"]
        self.debug_mode = False
        self.setup_game()
    
    def load_locations(self):
        village_map = [
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", "H", ".", "#", "#", "#", ".", ".", "#"],
            ["#", ".", ".", ".", "#", "W", "#", ".", ".", "#"],
            ["#", ".", "#", "#", "#", ".", "#", "#", ".", "#"],
            ["#", ".", "#", "L", ".", ".", ".", "#", ".", "#"],
            ["#", ".", "#", "#", "#", ".", "#", "#", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", "F", ".", "C", ".", ".", ".", "G", ".", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
        ]
        
        forest_map = [
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", ".", ".", ".", "T", ".", "#"],
            ["#", ".", "T", ".", "#", "#", "#", ".", ".", "#"],
            ["#", ".", ".", ".", "#", "T", "#", ".", "T", "#"],
            ["#", ".", "#", "#", "#", ".", "#", "#", ".", "#"],
            ["#", ".", "#", "T", ".", ".", "T", "#", ".", "#"],
            ["#", ".", "#", "#", "#", ".", "#", "#", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", "T", ".", ".", ".", "T", ".", ".", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
        ]
        
        lake_map = [
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "~", "~", "~", "~", "~", "~", "~", "~", "#"],
            ["#", "~", "H", "~", "~", "~", "~", "~", "~", "#"],
            ["#", "~", "~", "~", "~", "~", "~", "~", "~", "#"],
            ["#", "~", "~", "~", "~", "~", "~", "~", "~", "#"],
            ["#", "~", "~", "~", "~", "~", "~", "~", "~", "#"],
            ["#", "~", "~", "~", "~", "~", "~", "~", "~", "#"],
            ["#", "~", "~", "~", "~", "~", "~", "~", "~", "#"],
            ["#", "~", "~", "~", "~", "~", "~", "~", "~", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
        ]
        
        basement_map = [
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", "R", ".", "R", ".", "R", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", "R", ".", "R", ".", "R", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", "R", ".", "R", ".", "R", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
        ]
        
        self.locations = {
            "village": {
                "map": village_map,
                "name": "Деревня",
                "exits": {"forest": (5, 8), "lake": (1, 8), "basement": (3, 5)},
                "description": "Тихая деревня, где вы начали своё приключение."
            },
            "forest": {
                "map": forest_map,
                "name": "Лес",
                "exits": {"village": (5, 1)},
                "description": "Густой лес, полный опасностей и ценных ресурсов."
            },
            "lake": {
                "map": lake_map,
                "name": "Озеро",
                "exits": {"village": (1, 1)},
                "description": "Спокойное озеро с целебными травами по берегам."
            },
            "basement": {
                "map": basement_map,
                "name": "Подвал",
                "exits": {"village": (3, 5)},
                "description": "Тёмный и сырой подвал, кишащий крысами."
            }
        }
    
    def setup_game(self):
        self.player = Entity("Герой", 100, 50, 10, 20, 1, 1)
        
        health_potion = Item("Зелье здоровья", "heal", 30)
        mana_potion = Item("Зелье маны", "mana", 20)
        self.player.add_to_inventory(health_potion)
        self.player.add_to_inventory(mana_potion)
        
        self.quests = [
            Quest("Сбор трав", "Соберите 5 целебных трав у озера", {"herb": 5}, {"Зелье здоровья": 2}),
            Quest("Крысы в подвале", "Убейте 10 крыс в подвале", {"rat": 10}, {"Меч": 1}),
            Quest("Сбор шкур", "Соберите 3 волчьи шкуры в лесу", {"pelt": 3}, {"Кожаный доспех": 1}),
            Quest("Секретный цветок", "Найдите редкий синий цветок в лесу", {"blue_flower": 1}, {"Синее зелье": 1})
        ]
        
        self.generate_map_items()
    
    def generate_map_items(self):
        self.items = []
        
        if self.current_location == "lake":
            for y in range(len(self.game_map)):
                for x in range(len(self.game_map[y])):
                    if self.game_map[y][x] == "H":
                        # Используем простой детерминированный "случайный" выбор
                        val = (x * y + x + y) % 3
                        if val == 0:  # ~33% chance
                            self.items.append(Item("Целебная трава", "herb", 1, x, y))
        
        elif self.current_location == "forest":
            for y in range(len(self.game_map)):
                for x in range(len(self.game_map[y])):
                    if self.game_map[y][x] == "T":
                        val = (x * y + x + y) % 5
                        if val == 0:  # ~20% chance
                            rare_val = (x + y) % 10
                            if rare_val == 0:  # 10% chance from previous 20%
                                self.items.append(Item("Синий цветок", "blue_flower", 1, x, y))
                            else:
                                self.items.append(Item("Волчья шкура", "pelt", 1, x, y))
        
        self.enemies = []
        if self.current_location == "basement":
            for y in range(len(self.game_map)):
                for x in range(len(self.game_map[y])):
                    if self.game_map[y][x] == "R":
                        val = (x * y + x + y) % 2
                        if val == 0:  # 50% chance
                            self.enemies.append(Entity("Крыса", 15, 0, 2, 5, x, y))
        elif self.current_location == "forest":
            for y in range(len(self.game_map)):
                for x in range(len(self.game_map[y])):
                    if self.game_map[y][x] == "T":
                        val = (x * y + x + y) % 4
                        if val == 0:  # ~25% chance
                            self.enemies.append(Entity("Волк", 30, 0, 5, 10, x, y))
    
    def change_location(self, new_location):
        if new_location in self.locations:
            exit_pos = self.locations[self.current_location]["exits"].get(new_location)
            if exit_pos and (self.player.x, self.player.y) == exit_pos:
                self.current_location = new_location
                self.game_map = self.locations[new_location]["map"]
                self.player.x, self.player.y = self.locations[new_location]["exits"].get(self.current_location, (1, 1))
                self.generate_map_items()
                print(f"Вы перешли в локацию: {self.locations[new_location]['name']}")
                print(self.locations[new_location]["description"])
                return True
        return False
    
    def clear_screen(self):
        print("\n" * 50)
    
    def render_map(self):
        self.clear_screen()
        
        print(f"Локация: {self.locations[self.current_location]['name']}")
        print(f"HP: {self.player.hp}/{self.player.max_hp} | MP: {self.player.mp}/{self.player.max_mp}")
        print(f"Броня: {self.player.armor} | Урон: {self.player.damage}")
        print("Управление: WASD - движение, I - инвентарь, Q - квесты, F - взаимодействие")
        print()
        
        for y in range(len(self.game_map)):
            for x in range(len(self.game_map[y])):
                if self.player.x == x and self.player.y == y:
                    print("@", end=" ")
                else:
                    enemy_here = None
                    for enemy in self.enemies:
                        if enemy.x == x and enemy.y == y:
                            enemy_here = enemy
                            break
                    
                    item_here = None
                    for item in self.items:
                        if hasattr(item, 'x') and item.x == x and item.y == y:
                            item_here = item
                            break
                    
                    if enemy_here:
                        print("E", end=" ")
                    elif item_here:
                        print("*", end=" ")
                    else:
                        print(self.game_map[y][x], end=" ")
            print()
        
        if hasattr(self, 'message'):
            print(self.message)
            delattr(self, 'message')
    
    def process_input(self, command):
        moved = False
        
        if command.lower() == 'w':
            moved = self.player.move(0, -1, self.game_map)
        elif command.lower() == 's':
            moved = self.player.move(0, 1, self.game_map)
        elif command.lower() == 'a':
            moved = self.player.move(-1, 0, self.game_map)
        elif command.lower() == 'd':
            moved = self.player.move(1, 0, self.game_map)
        elif command.lower() == 'i':
            self.show_inventory()
            return False
        elif command.lower() == 'q':
            self.show_quests()
            return False
        elif command.lower() == 'f':
            self.interact()
            return False
        
        if moved:
            self.check_for_combat()
            self.check_for_items()
            self.check_location_change()
        
        return True
    
    def check_for_combat(self):
        for enemy in self.enemies[:]:
            if self.player.x == enemy.x and self.player.y == enemy.y:
                self.start_combat(enemy)
                break
    
    def start_combat(self, enemy):
        print(f"Бой с {enemy.name}!")
        while self.player.is_alive() and enemy.is_alive():
            print(f"Ваше HP: {self.player.hp}/{self.player.max_hp} | HP {enemy.name}: {enemy.hp}/{enemy.max_hp}")
            action = input("Атаковать (A) или Использовать предмет (I)? ").lower()
            
            if action == 'a':
                damage = self.player.attack(enemy)
                print(f"Вы нанесли {damage} урона {enemy.name}!")
            elif action == 'i':
                self.show_inventory(combat=True)
                item_choice = input("Выберите предмет для использования (номер или 'отмена'): ")
                if item_choice.lower() != 'отмена':
                    try:
                        item_index = int(item_choice) - 1
                        if not self.player.use_item(item_index):
                            print("Неверный выбор предмета!")
                            continue
                    except ValueError:
                        print("Неверный ввод!")
                        continue
            
            if not enemy.is_alive():
                print(f"Вы победили {enemy.name}!")
                if enemy.name == "Крыса":
                    self.update_quest_progress("rat")
                elif enemy.name == "Волк":
                    self.update_quest_progress("pelt")
                self.enemies.remove(enemy)
                break
            
            damage = enemy.attack(self.player)
            print(f"{enemy.name} нанес вам {damage} урона!")
            
            if not self.player.is_alive():
                print("Вы погибли...")
                input("Нажмите Enter, чтобы продолжить...")
                self.setup_game()
                return
    
    def check_for_items(self):
        for item in self.items[:]:
            if hasattr(item, 'x') and item.x == self.player.x and item.y == self.player.y:
                self.player.add_to_inventory(item)
                self.items.remove(item)
                self.message = f"Вы подобрали: {item.name}"
                if item.type == "herb":
                    self.update_quest_progress("herb")
                elif item.type == "blue_flower":
                    self.update_quest_progress("blue_flower")
                break
    
    def check_location_change(self):
        for location, pos in self.locations[self.current_location]["exits"].items():
            if (self.player.x, self.player.y) == pos:
                self.change_location(location)
                break
    
    def interact(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        interacted = False
        
        for dx, dy in directions:
            nx, ny = self.player.x + dx, self.player.y + dy
            if 0 <= nx < len(self.game_map[0]) and 0 <= ny < len(self.game_map):
                if self.game_map[ny][nx] == "C":
                    self.open_chest()
                    interacted = True
                    break
                elif self.game_map[ny][nx] == "G":
                    self.talk_to_elder()
                    interacted = True
                    break
        
        if not interacted:
            self.message = "Здесь не с чем взаимодействовать"
    
    def open_chest(self):
        # Детерминированный выбор награды
        val = (self.player.x + self.player.y) % 2
        if val == 0:
            reward = Item("Зелье здоровья", "heal", 30)
        else:
            reward = Item("Зелье маны", "mana", 20)
        
        self.player.add_to_inventory(reward)
        self.message = f"Вы нашли в сундуке: {reward.name}!"
    
    def talk_to_elder(self):
        print("Старейшина: 'Приветствую тебя, герой! Как продвигаются твои задания?'")
        self.show_quests()
    
    def show_inventory(self, combat=False):
        print("\n--- ИНВЕНТАРЬ ---")
        if not self.player.inventory:
            print("Инвентарь пуст")
        else:
            for i, item in enumerate(self.player.inventory, 1):
                print(f"{i}. {item.name} ({item.type})")
        
        if not combat:
            input("\nНажмите Enter, чтобы продолжить...")
    
    def show_quests(self):
        print("\n--- КВЕСТЫ ---")
        for quest in self.quests:
            print(f"\n{quest.name}: {quest.description}")
            print("Прогресс:")
            for target, count in quest.target.items():
                print(f"- {target}: {quest.progress[target]}/{count}")
            if quest.completed:
                print("(Завершено)")
        
        input("\nНажмите Enter, чтобы продолжить...")
    
    def update_quest_progress(self, target_type):
        for quest in self.quests:
            if not quest.completed and target_type in quest.target:
                quest.progress[target_type] += 1
                if quest.progress[target_type] >= quest.target[target_type]:
                    quest.completed = True
                    self.message = f"Квест '{quest.name}' завершен! Получена награда."
                    for reward, count in quest.reward.items():
                        for _ in range(count):
                            if reward == "Зелье здоровья":
                                self.player.add_to_inventory(Item(reward, "heal", 30))
                            elif reward == "Меч":
                                self.player.damage += 10
                                self.message += f"\nВаш урон увеличен на 10!"
                            elif reward == "Кожаный доспех":
                                self.player.armor += 5
                                self.message += f"\nВаша броня увеличена на 5!"
                            elif reward == "Синее зелье":
                                self.player.add_to_inventory(Item(reward, "heal", 50))
    
    def run(self):
        running = True
        while running:
            self.render_map()
            command = input("Ваше действие: ")
            running = self.process_input(command)

if __name__ == "__main__":
    game = Game()
    game.run()