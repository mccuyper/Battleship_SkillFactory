from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, ship, length, orientation):
        self.ship = ship
        self.length = length
        self.orientation = orientation

    @property
    def dots(self):
        ship_dots = []

        for i in range(self.length):  # start loop with a ship length

            cur_x = self.ship.x
            cur_y = self.ship.y

            if self.orientation == 0:  # horizontal position of ship
                cur_x += i

            elif self.orientation == 1:  # vertical position
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0
        self.field = [["O"]*size for _ in range(size)]  # 6*6 field

        self.busy = []
        self.ships = []


    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for i in ship.dots:
            self.field[i.x][i.y] = "■"
            self.busy.append(i)

        self.ship_shape(ship)


    def ship_shape(self, ship): 
        near = [
          (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    
                    self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
        

    def out(self, d):
        return not((0<=d.x < self.size) and (0<= d.y < self.size))
 


    def __str__(self):
        res = ""
        res += "■ | 1 | 2 | 3 | 4 | 5 | 6 | \n---------------------------"
        for i, row in  enumerate(self.field):
            res +=f"\n{i+1} | " + " | ".join(row) + " |"
        
        if self.hid:
            res = res.replace("■", 'O')

        return res



def random_place(size=6):
    lens = [3, 2, 2, 1, 1, 1, 1]
    board = Board()
    attempts = 0
    for l in lens:
        # while True:
        #     attempts += 1
        #     if attempts > 2000:
        #         return None
        ship = Ship(Dot(randint(0, size), randint(0, size)), l, randint(0,1))
        try:
            board.add_ship(ship)
            break
        except BoardWrongShipException:
            pass
    # board.begin()
    return board



# b = Board(hid = 0)
# s = Ship(Dot(0,5), 3, 1)

# b.add_ship(s)
# b.field()
# print(b)

b = random_place()
print(b)