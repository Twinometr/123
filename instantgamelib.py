class GameObject:
    """Базовый класс для игровых объектов"""
    def __init__(self, x=0, y=0, char='#'):
        self.x = x          # Позиция по горизонтали
        self.y = y          # Позиция по вертикали
        self.char = char    # Символ для отображения
        self.active = True # Активен ли объект
    
    def update(self):
        """Логика обновления объекта (переопределите в дочерних классах)"""
        pass
    
    def draw(self, grid):
        """Отрисовка объекта в игровой сетке"""
        if self.active and 0 <= self.y < len(grid) and 0 <= self.x < len(grid[0]):
            grid[self.y][self.x] = self.char


class GameEngine:
    """Основной игровой движок"""
    def __init__(self, width=20, height=10):
        self.width = width    # Ширина игрового поля
        self.height = height  # Высота игрового поля
        self.grid = []        # Игровая сетка
        self.objects = []     # Список игровых объектов
        self.running = False  # Флаг работы игры
        self.last_key = None  # Последняя нажатая клавиша
        self._init_grid()     # Инициализация сетки
    
    def _init_grid(self):
        """Создаю пустую игровую сетку"""
        self.grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
    
    def add_object(self, obj):
        """Добавляет объект в игру"""
        obj.game = self  # Даем объекту ссылку на игру
        self.objects.append(obj)
        return 
        if obj in self.objects:
            self.objects.remove(obj)
    
    def clear(self):
        """Очищаю игровую сетку"""
        self._init_grid()
    
    def _get_input(self):
        """Получаю ввод с клавиатуры (только для Windows)"""
        import msvcrt
        if msvcrt.kbhit():
            try:
                return msvcrt.getch().decode().lower()
            except:
                return None
        return None
    
    def update(self):
        """Обновляю состояние игры"""
        key = self._get_input()
        if key:
            self.last_key = key
            if key == 'q':
                self.running = False
        
        # Обновляем все активные объекты
        for obj in self.objects[:]:
            if obj.active:
                obj.update()
            else:
                self.remove_object(obj)
    
    def render(self):
        """Отрисовываю игровое поле"""
        self.clear()
        
        # Рисуем все объекты
        for obj in self.objects:
            obj.draw(self.grid)
        
        # Очищаем консоль (имитация)
        print("\n" * 30)
        
        # Рисую сетку
        for row in self.grid:
            print(' '.join(row))
    
    def run(self):
        """Запускает игровой цикл"""
        self.running = True
        while self.running:
            self.update()
            self.render()


# Пример использования библиотеки

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, '@')  
        self.speed = 1
    
    def update(self):
        if hasattr(self, 'game') and self.game.last_key:
            key = self.game.last_key
            if key == 'w': self.y -= self.speed
            elif key == 's': self.y += self.speed
            elif key == 'a': self.x -= self.speed
            elif key == 'd': self.x += self.speed
            # Границы
            if self.x < 0: self.x = 0
            elif self.x >= self.game.width: self.x = self.game.width - 1
            if self.y < 0: self.y = 0
            elif self.y >= self.game.height: self.y = self.game.height - 1


class Wall(GameObject):
    "Стена"
    def __init__(self, x, y):
        super().__init__(x, y, '█')


if __name__ == "__main__":
    game = GameEngine(30, 15)
    
    player = Player(5, 5)
    game.add_object(player)
    
    # Создаем стены
    for x in range(30):
        game.add_object(Wall(x, 0))         # Верхняя стена
        game.add_object(Wall(x, 14))        # Нижняя стена
    for y in range(1, 14):
        game.add_object(Wall(0, y))         # Левая стена
        game.add_object(Wall(29, y))        # Правая стена
    
    # Добавляем несколько стен внутри
    game.add_object(Wall(10, 5))
    game.add_object(Wall(15, 10))
    game.add_object(Wall(20, 7))
    
    print("Простая игра с управлением WASD")
    print("Игрок - @, Стены - █")
    print("Нажмите Q для выхода")
    
    # Запускаем игру
    game.run()
