import random
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def getProximity(self, otherPoint):
        return math.sqrt((self.x - otherPoint.x)**2 + (self.y - otherPoint.y)**2)

class Ship:
    _DIRECTION_INDICATOR_HORIZONTAL = '-'
    _DIRECTION_INDICATOR_VERTICAL = '|'

    def __init__(self, upperLeft, length, isHorizontal, identifier):
        self._upperLeft = upperLeft
        self._length = length
        self._isHorizontal = isHorizontal
        self._identifier = identifier
        self._hits = 0

    def __str__(self):
        return f'{self._identifier} at {self._upperLeft} {self._DIRECTION_INDICATOR_HORIZONTAL if self._isHorizontal else self._DIRECTION_INDICATOR_VERTICAL} {self._length}'

    def markHit(self):
        self._hits += 1

    def getHits(self):
        return self._hits

    def isSunk(self):
        return self._hits >= self._length
    
    def getIdentifier(self):
        return self._identifier

    def contains(self, point):
        if (self._isHorizontal):
            return ((point.y == self._upperLeft.y) and (point.x >= self._upperLeft.x) and (point.x < (self._upperLeft.x + self._length)))
        else:
            return ((point.x == self._upperLeft.x) and (point.y >= self._upperLeft.y) and (point.y < (self._upperLeft.y + self._length)))

    def getProximity(self, otherShip):
        closestDistance = 9999
        for i in range(self._length):
            for j in range(otherShip._length):
                distance = self.getPoint(i).getProximity(otherShip.getPoint(j))
                if (distance < closestDistance):
                    closestDistance = distance
        return closestDistance

    def getPoint(self, location):
        if (self._isHorizontal):
            return Point(self._upperLeft.x + location, self._upperLeft.y)
        else:
            return Point(self._upperLeft.x, self._upperLeft.y + location)

    def doesLieWithin(self, boundary):
        if (self._isHorizontal):
            return ((0 <= self._upperLeft.y) and (boundary.y > self._upperLeft.y) and (0 <= self._upperLeft.x) and (boundary.x > (self._upperLeft.x + self._length)))
        else:
            return ((0 <= self._upperLeft.x) and (boundary.x > self._upperLeft.x) and (0 <= self._upperLeft.y) and (boundary.y > (self._upperLeft.y + self._length)))

class Board:
    _MIN_SHIP_LENGTH = 2
    _MAX_SHIP_LENGTH = 6

    def __init__(self, size, numberOfShips):
        self._size = size
        self._shots = [[False] * size.x for i in range(size.y)]
        self._ships = []
        self._createShips(numberOfShips)

    def _getShipAt(self, point):
        for ship in self._ships:
            if ship.contains(point):
                return ship
        return None

    def _displayHeader(self):
        print("")
        print("    ", end="")
        for x in range(self._size.x):
            print(f"{x:02} ", end="")
        print("")

        print("    ", end="")
        for x in range(self._size.x):
            print("-- ", end="")
        print("")

    def _addShip(self, ship):
        for existingShip in self._ships:
            if (ship.getProximity(existingShip) < 1.5):
                # print(f"New ship {ship} rejected for being too close to existing ship {existingShip}.")
                return False
        self._ships.append(ship)
        # print(f"New ship {ship} added to board")
        # self.display(True)
        return True

    def _createShip(self, identifier):
        isHorizontal = (random.randrange(2) == 1)
        length = random.randrange(self._MIN_SHIP_LENGTH, self._MAX_SHIP_LENGTH + 1)
        if (isHorizontal):
            maxX = self._size.x - length
            maxY = self._size.y
        else:
            maxX = self._size.x
            maxY = self._size.y - length

        location = Point(random.randrange(maxX), random.randrange(maxY))
        return self._addShip(Ship(location, length, isHorizontal, identifier))

    def _createShips(self, numberOfShips):
        for i in range(numberOfShips):
            while not self._createShip(chr(ord('A') + i)):
                pass


    def getNumberOfShips(self):
        return len(self._ships)

    def shootAt(self, point):
        if self._shots[point.y][point.x]:
            print(f"Location {point} has already been targeted")
            return False

        self._shots[point.y][point.x] = True
        
        ship = self._getShipAt(point)
        if ship is None:
            print(f"Plop. Nothing at {point}")
            return False

        ship.markHit()
        if ship.isSunk():
            print(f"You sunk ship {ship} at {point}!")
            return True

        print(f"You hit something at {point}!")
        return True

    def areAllShipsSunk(self):
        for ship in self._ships:
            if not ship.isSunk():
                return False
        return True

    def display(self, showShips):
        self._displayHeader()

        for y in range(self._size.y):
            print(f"{y:02}: ", end="")
            for x in range(self._size.x):
                ship = self._getShipAt(Point(x, y))
                if ship is not None:
                    if ship.isSunk():
                        print(" @ ", end="")
                    elif self._shots[y][x]:
                        print(" ! ", end="")
                    elif showShips:
                        print(f" {ship.getIdentifier()} ", end="")
                    else:
                        print(" . ", end="")
                elif self._shots[y][x]:
                    print(" * ", end="")
                else:
                    print(" . ", end="")
            print("")


class Game:
    def __init__(self, width, height, numberOfShips):
        random.seed(a=None, version=2)
        self._board = Board(Point(width, height), numberOfShips)
        self._shots = 0

    def _takeTurn(self):
        self._board.display(False)

        while True:
            choice = input("Enter quit, peek, or coordinates to shoot: ")
            if choice == "quit":
                return False
        
            if choice == "peek":
                self._board.display(True)
                continue

            try: 
                a = choice.split(",")
                x = int(a[0].strip())
                y = int(a[1].strip())
                break
            except ValueError:
                print("Invalid input. Try again.")
                continue

        self._shots += 1
        self._board.shootAt(Point(x, y))

        if self._board.areAllShipsSunk():
            self._board.display(False)
            print(f"All {self._board.getNumberOfShips()} enemy ships have been sunk! Congratulations!")
            print(f"It took you {self._shots} shots to get them all.")
            return False
        return True

    def play(self):
        while self._takeTurn():
            pass
        print("Game Over")




        
if __name__ == "__main__":
    game = Game(10, 10, 5)
    game.play()

