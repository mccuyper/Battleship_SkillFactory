from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

""" 
------------------EXCEPTIONS--------------------
"""
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Your are trying to shoot out of the board!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "You've already shooted here!!!"

class BoardWrongShipException(BoardException):
    pass
"""-----------------------------------------------"""

class Ship:
    def __init__(self, ship, length, orientation):
        self.ship = ship
        self.length = length
        self.orientation = orientation
        self.lives = length

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
        self.field = [["☐"]*size for _ in range(size)]  # 6*6 field

        self.busy = []
        self.ships = []


    def begin(self):
        self.busy = []


    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = '☠'  # ✘ ྾ ☒ ☉
                if ship.lives == 0:
                    self.count += 1
                    self.ship_shape(ship, verb = True)
                    print("Ship's been sinked!")
                    return True  # continue shooting
                else:
                    print('Ship\'s shooted! ')
                    return True  # continue shooting
        self.field[d.x][d.y] = "•"
        print("You missed")
        return False # stop shooting if you miss

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for i in ship.dots:
            self.field[i.x][i.y] = "■"
            self.busy.append(i)

        self.ships.append(ship)
        self.ship_shape(ship)



    def ship_shape(self, ship,verb = False ): 
        near = [
          (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
        


    def out(self, d):
        return not((0<=d.x < self.size) and (0<= d.y < self.size))
 

        # Print Board
    def __str__(self):
        res = ""
        res += "■ | 1 | 2 | 3 | 4 | 5 | 6 | \n---------------------------"
        for i, row in  enumerate(self.field):
            res +=f"\n{i+1} | " + " | ".join(row) + " |"
        
        if self.hid:
            res = res.replace("■", '☐')

        return res


# Place Ships on  the Board
def random_place(size=6):
    lens = [3, 2, 2, 1, 1, 1, 1] # !!! - First need to go big-sized ships  - !!!
    board = Board()
    attempts = 0
    for l in lens:
        while True:
            # If no space to place all ships on the Board - return None
            attempts += 1
            if attempts > 2000:
                return None
            ship = Ship(Dot(randint(0, size), randint(0, size)), l, randint(0,1))
            try:
                board.add_ship(ship)
                break
            except BoardWrongShipException:
                pass
    
    return board



class Game:

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        comp = self.random_board()
        comp.hid = True
        self.ai = AI(comp,pl)
        self.user = User(pl, comp)
        
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    # Place Ships on  the Board(6X6)
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1] # !!! - First need to go big-sized ships  - !!!
        board = Board()
        attempts = 0
        for l in lens:
            while True:
                # If no space to place all ships on the Board - return None
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board


    def greet(self):
        print("-------------------")
        print("|    Welcome to   |")
        print("|    ----------   |")
        print("| BATTLESHIP GAME | ")
        print("-------------------")
        print(" Main rules:       ")
        print(" x - input for column  ")
        print(" y - input for row ")

    def loop(self):
        num = 0
       
        while True:
            print("-"*20+"\nYour Board: ")
            print(self.user.board)
            print("-"*20+"\nComputer Board: ")
            print(self.ai.board)
            if num %2 == 0:
                print("-"*20+"\nYour Move Now (x y): ")
                repeat = self.user.move()
                 
            else:
                print("-"*20+"\nComputer Move Now: ")
                repeat = self.ai.move()

            if repeat:
                num-=1
            if self.ai.board.count == 7:
                print("-"*20+"\nYou Win! ")
                break
            elif self.user.board.count == 7:
                print("-"*20+"\nYou Lost! ")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()


class Player:
    def __init__(self,  board, enemyBoard):
        
        self.board = board
        self.enemyBoard = enemyBoard

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemyBoard.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0,5),randint(0,5))
        print(f"Computer is shooting! {d.x+1}  {d.y+1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Your turn: ").split()
            
            if len(cords) != 2:
                print("---> Put coordinates(column row) where to shoot(e.g.: 3 2)! ")
                continue
            
            x, y = cords
            
            if not(x.isdigit()) or not(y.isdigit()):
                print(" Put digits only please! ")
                continue
            
            x, y = int(x), int(y)
            
            return Dot(x-1, y-1)

g = Game()
g.start()
