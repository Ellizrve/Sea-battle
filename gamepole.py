from random import randint, randrange


class GamePole:
    """This class provide work with the playing field and description it"""
    def __init__(self, size):
        self.__check_size(size)
        self._size = size
        self._ships = []
        self._pole = self.__form_pole()

    @classmethod
    def __check_size(cls, size):
        """Check size of playing field"""
        if type(size) != int or size <= 0:
            raise TypeError('Invalid size value. Please enter an integer positive value')

    def __form_pole(self):
        """Playing field formation.
        Playing field is two-dimensional tuple with size x size elements"""
        return [[0 for line in range(self._size)] for column in range(self._size)]

    def __form_ships(self):
        """Ship formation.
        Ships in the _ships collection are formed as follows:
        single-deck - 4; two-deck – 3; three-deck – 2; four-deck - 1.
        The orientation of these ships random."""
        amount_of_ships = 1
        length_of_ships = 4
        while amount_of_ships != 5:
            for i in range(amount_of_ships):
                self._ships.append(Ship(length_of_ships, tp=randint(1, 2)))
            amount_of_ships += 1
            length_of_ships -= 1

    def __put_on(self, ship):
        """Placing the ship on the playing field"""
        x_coord = ship._x
        y_coord = ship._y
        decks = ship._cells
        counter = 0
        while counter != len(decks):
            if ship._tp == 2:
                self._pole[y_coord][x_coord] = decks[counter]
                y_coord += 1
                counter += 1
            else:
                self._pole[y_coord][x_coord] = decks[counter]
                x_coord += 1
                counter += 1

    def __put_away(self, ship):
        """Removing a ship from the playing field"""
        x_coord = ship._x
        y_coord = ship._y
        decks = ship._cells
        counter = 0
        while counter != len(decks):
            if ship._tp == 2:
                self._pole[y_coord][x_coord] = 0
                y_coord += 1
                counter += 1
            else:
                self._pole[y_coord][x_coord] = 0
                x_coord += 1
                counter += 1

    def is_collide_collection(self, obj, collection):
        """Multiple ship crossing check"""
        for checking_object in collection:
            if obj.is_collide(checking_object):
                return True
        return False

    def __install_coords(self):
        """Assignment of start coordinates"""
        for ship in self._ships:
            initial_limit = 0
            final_limit = self._size - 1
            checking_ships = self._ships[:]
            checking_ships.remove(ship)
            intersection = True
            while intersection is True:
                coord_x = randint(initial_limit, final_limit)
                coord_y = randint(initial_limit, final_limit)
                ship.set_start_coords(coord_x, coord_y)
                if ship.is_out_pole(self._size):
                    continue
                if self.is_collide_collection(ship, checking_ships):
                    continue
                intersection = False
                self.__put_on(ship)

    def init(self):
        """Initial initialization of the playing field"""
        self.__form_ships()
        self.__install_coords()

    def get_ships(self):
        """Moving each ship from the _ships collection"""
        return self._ships

    def show(self):
        """Displaying the playing field in the console"""
        for line in self._pole:
            print(*line, end='\n')

    def get_pole(self):
        """Getting the current playing field"""
        return tuple((tuple(line) for line in self._pole))

    def move_ships(self):
        """Moving each ship on the playing field of the ship's orientation"""
        for ship in self._ships:
            checking_ships = self._ships[:]
            checking_ships.remove(ship)
            step_bak = -1
            step_forward = 1
            step_of_ship = randrange(step_bak, step_forward, 2)
            variation = 2
            self.__put_away(ship)
            for x in range(variation):
                intersection = False
                ship.move(step_of_ship)
                if ship.is_out_pole(self._size):
                    intersection = True
                if self.is_collide_collection(ship, checking_ships):
                    intersection = True
                if intersection is True:
                    ship.move(-step_of_ship)
                    step_of_ship = -step_of_ship
                    continue
                else:
                    break
            self.__put_on(ship)