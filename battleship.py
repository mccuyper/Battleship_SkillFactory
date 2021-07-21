class Dot:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):  
		return self.x == other.x and self.y == other.y 

	def __repr__(self):
		return f"({self.x}, {self.y})"


class Ship:
	def __init__(self, ship, length, orientation):
		self.ship = ship
		self.length = length
		self.orientation = orientation

	@property
	def dots(self):
		ship_dots = []

		for i in range(self.length): # start loop with a ship length
			
			cur_x = self.ship.x
			cur_y = self.ship.y

			if self.orientation == 0: # horizontal position of ship
				cur_x += i

			elif self.orientation == 1: # vertical position 
				cur_y += i

			ship_dots.append(Dot(cur_x, cur_y))

		return ship_dots

	def shooten(self):
		return shot in self.dots


class Board:
	def __init__(self, hid = False, size = 6):
		self.size = size
		self.hid = hid

		self.count = 0
		self.field = [ ["O"]*size for _ in range(size) ] # 6*6 field

		self.busy = []
		self.ships = []

	def add_ship(self, ship):
		for i in ship.dots:
			self.field[i.x][i.y] = "■"

	def __str__(self):
		res = ""
		res += "■ | 1 | 2 | 3 | 4 | 5 | 6 | \n---------------------------"
		for i, row in  enumerate(self.field):
			res +=f"\n{i+1} | " + " | ".join(row) + " |"
		
		if self.hid:
			res = res.replace("■", 'O')

		return res



b = Board(hid = True)
s = Ship(Dot(1,1), 3, 0)

b.add_ship(s)
# b.field()
print(b)