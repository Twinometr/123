class GameObject:
    """
    Базовый класс для игровых объектов
    Использование:
    class Player(GameObject):
        def __init__(self, x, y):
            super().__init__(x, y, '@')  # Символ '@' будет отображаться
    """
    def __init__(self, x=0, y=0, char='#'):
        self.x = x
        self.y = y
        self.char = char
        self.active = True
    
    def update(self):
        """Переопределите этот метод для логики объекта"""
        pass
    
    def draw(self, grid):
        """Отрисовывает объект в игровой сетке"""
        if self.active and 0 <= self.y < len(grid) and 0 <= self.x < len(grid[0]):
            grid[self.y][self.x] = self.char


class InstantGame:
    """
    Основной класс игры
    Использование:
    game = InstantGame(20, 10)  # Ширина, высота
    player = Player(5, 5)
    game.add_object(player)
    game.run()
    """
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.grid = []
        self.objects = []
        self.running = False
        self.last_key = None
        self._init_grid()
        self._setup_input()
    
    def _init_grid(self):
        """Инициализирует пустую игровую сетку"""
        self.grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
    
    def _setup_input(self):
        """Настраивает обработку ввода для разных ОС"""
        try:
            # Windows
            import msvcrt
            self._get_key = lambda: msvcrt.getch().decode() if msvcrt.kbhit() else None
        except:
            # Unix-системы
            import sys, tty, termios
            self._fd = sys.stdin.fileno()
            self._old_settings = termios.tcgetattr(self._fd)
            tty.setraw(self._fd)
            import select
            self._get_key = lambda: sys.stdin.read(1) if select.select([sys.stdin], [], [], 0)[0] else None
    
    def add_object(self, obj):
        """
        Добавляет объект в игру
        Возвращает добавленный объект
        """
        obj.game = self  # Даем объекту доступ к игре
        self.objects.append(obj)
        return obj
    
    def remove_object(self, obj):
        """Удаляет объект из игры"""
        if obj in self.objects:
            self.objects.remove(obj)
    
    def clear(self):
        """Очищает игровую сетку"""
        self._init_grid()
    
    def update(self):
        """Обновляет состояние игры"""
        key = self._get_key()
        if key:
            key = key.lower()
            if key == 'q':
                self.running = False
            self.last_key = key
        
        for obj in self.objects[:]:
            if obj.active:
                obj.update()
            else:
                self.remove_object(obj)
    
    def render(self):
        """Отрисовывает игровое поле"""
        self.clear()
        for obj in self.objects:
            obj.draw(self.grid)
        
        # Очистка экрана (имитация)
        print("\n" * 30)
        # Отрисовка сетки
        for row in self.grid:
            print(' '.join(row))
    
    def run(self):
        """
        Запускает игровой цикл
        Автоматически восстанавливает настройки терминала после завершения
        """
        self.running = True
        while self.running:
            self.update()
            self.render()
        
        # Восстановление настроек терминала для Unix
        if hasattr(self, '_old_settings'):
            import termios
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)


# Вспомогательные классы

class WASDController:
    """
    Контроллер для управления объектом через WASD
    Использование:
    player = Player(5, 5)
    controller = WASDController(player)
    game.on_key_press = controller.handle_input
    """
    def __init__(self, target, speed=1):
        self.target = target
        self.speed = speed
    
    def handle_input(self, key):
        if key == 'w':
            self.target.y -= self.speed
        elif key == 's':
            self.target.y += self.speed
        elif key == 'a':
            self.target.x -= self.speed
        elif key == 'd':
            self.target.x += self.speed


class BoundaryChecker:
    """
    Проверяет границы для объекта
    Использование:
    player = Player(5, 5)
    checker = BoundaryChecker(player, game.width, game.height)
    """
    def __init__(self, target, max_x, max_y):
        self.target = target
        self.max_x = max_x
        self.max_y = max_y
    
    def check(self):
        if self.target.x < 0:
            self.target.x = 0
        elif self.target.x >= self.max_x:
            self.target.x = self.max_x - 1
        if self.target.y < 0:
            self.target.y = 0
        elif self.target.y >= self.max_y:
            self.target.y = self.max_y - 1