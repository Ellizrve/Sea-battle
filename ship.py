class Ship:
    """This class provide work with ships and description it"""
    def __init__(self, length, tp=1, x=None, y=None):
        self.__check_lenght(length)
        self.__check_tp(tp)
        if x is not None:
            self.__check_coord(x)
        if y is not None:
            self.__check_coord(y)
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = self.__form_cells()

    @classmethod
    def __check_lenght(cls, length):
        """Checking for correct length"""
        if type(length) != int or length not in range(1, 5):
            raise TypeError('Invalid length value. Please enter an integer value from 1 to 4')

    @classmethod
    def __check_tp(cls, tp):
        """Checking for correct orientation"""
        if type(tp) != int or tp not in range(1, 3):
            raise TypeError('Invalid orientation value. Please enter an integer value: 1 (horizontal) or 2 (vertical)')

    @classmethod
    def __check_coord(cls, coord):
        """Checking for correct coordinate"""
        if type(coord) != int or coord not in range(0, GamePole._size):
            raise TypeError(f'Incorrect {coord} coordinate value. Please enter an integer value from 0 to {GamePole._size}')

    def __form_cells(self):
        """Cells list formation.
        A list with the length of the parameter _length consisting of 1"""
        return [1 for x in range(self._length)]

    def set_start_coords(self, x, y):
        """Setting initial coordinates.
        Writing values to local attributes _x, _y"""
        self._x = x
        self._y = y

    def get_start_coords(self):
        """Getting the initial ship's coordinates"""
        return self._x, self._y

    def __check_hit(self):
        """Checking for hits on a ship's deck.
        If _cells has a value of 2 the deck has been hit."""
        if 2 in self._cells:
            self._is_move = False

    def move(self, go):
        """Moving the ship in the direction of its orientation on 'go' cells"""
        self.__check_hit()
        if self._is_move:
            if self._tp == 1:
                self._x += go
            else:
                self._y += go

    def is_collide(self, ship):
        """Checking for collision with another ship"""
        if ship._x is None and ship._y is None:
            return False
        if self._x == ship._x and self._y == ship._y:
            return True
        if self._tp == 1:
            counter_x = self._x - 1
            for line in range(self._length + 2):
                if ship._tp == 1:
                    ship_counter = ship._x
                    for line2 in range(ship._length):
                        if counter_x == ship_counter and self._y + 1 == ship._y or \
                                counter_x == ship_counter and self._y == ship._y or \
                                counter_x == ship_counter and self._y - 1 == ship._y:
                            return True
                        ship_counter += 1
                if ship._tp == 2:
                    ship_counter = ship._y
                    for line2 in range(ship._length):
                        if counter_x == ship._x and self._y + 1 == ship_counter or \
                                counter_x == ship._x and self._y == ship_counter or \
                                counter_x == ship._x and self._y - 1 == ship_counter:
                            return True
                        ship_counter += 1
                counter_x += 1
        if self._tp == 2:
            counter_y = self._y - 1
            for line in range(self._length + 2):
                if ship._tp == 1:
                    ship_counter = ship._x
                    for line2 in range(ship._length):
                        if counter_y == ship._y and self._x + 1 == ship_counter or \
                                counter_y == ship._y and self._x == ship_counter or \
                                counter_y == ship._y and self._x - 1 == ship_counter:
                            return True
                        ship_counter += 1
                if ship._tp == 2:
                    ship_counter = ship._y
                    for line2 in range(ship._length):
                        if counter_y == ship_counter and self._x + 1 == ship._x or \
                                counter_y == ship_counter and self._x == ship._x or \
                                counter_y == ship_counter and self._x - 1 == ship._x:
                            return True
                        ship_counter += 1
                counter_y += 1
        return False

    def is_out_pole(self, game_pole_size):
        """Checking for the ship to leave the playing field"""
        if self._y < 0 or self._x < 0:
            return True
        if self._tp == 2 and self._y + len(self._cells) > game_pole_size:
            return True
        if self._tp == 1 and self._x + len(self._cells) > game_pole_size:
            return True
        return False

    def get_coords(self):
        coord_x = self._x
        coord_y = self._y
        coords_of_ship = []
        if self._tp == 1:
            for deck in range(self._length):
                coords_of_ship.append((coord_x, coord_y))
                coord_x += 1
        if self._tp == 2:
            for deck in range(self._length):
                coords_of_ship.append((coord_x, coord_y))
                coord_y += 1
        return coords_of_ship

    def hit_the_ship(self, coord):
        deck = self.get_coords().index(coord)
        self._cells[deck] = 2

    def __check_indx(self, indx):
        """Index check for __getitem__ and __setitem__"""
        if type(indx) != int or indx not in range(0, self._length):
            raise TypeError(f'Invalid index value. Please enter an integer value from 0 to {self._length - 1}')

    @classmethod
    def __check_value(cls, value):
        """Value check for __setitem__"""
        if type(value) != int or value not in range(1, 3):
            raise TypeError('Invalid value. Please enter an integer value: 1 or 2')

    def __getitem__(self, indx):
        self.__check_indx(indx)
        return self._cells[indx]

    def __setitem__(self, indx, value):
        self.__check_indx(indx)
        self.__check_value(value)
        self._cells[indx] = value