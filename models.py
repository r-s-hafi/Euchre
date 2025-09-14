
class Player():
    def __init__(self, name):
        self.order: int
        self.team: int
        self.name = name
        self.points = int
        self.is_maker = False
        self.hand = []

class User(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = 'User'

class Bot(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = 'Bot'

