# move(go) - перемещение корабля в направлении его ориентации на go клеток (go = 1 - движение в одну сторону на клетку;
# go = -1 - движение в другую сторону на одну клетку); движение возможно только если флаг _is_move = True;

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
        if self._is_move:
            pass

    def is_collide(self, ship, pole):
        """Checking for collision with another ship"""
        if ship._x is None and ship._y is None:
            return False

        if self._x == 0 and self._y == 0:
            if pole._pole[self._y + 1][self._x] == 1 or pole._pole[self._y][self._x + 1] == 1 or \
                    pole._pole[self._y + 1][self._x + 1] == 1:
                return True
        if self._x == 0 and self._y == 9:
            if pole._pole[self._y - 1][self._x] == 1 or pole._pole[self._y][self._x + 1] == 1 or \
                    pole._pole[self._y - 1][self._x + 1] == 1:
                return True
        if self._x == 9 and self._y == 0:
            if pole._pole[self._y + 1][self._x] == 1 or pole._pole[self._y][self._x - 1] == 1 or \
                    pole._pole[self._y + 1][self._x - 1] == 1:
                return True
        if self._x == 9 and self._y == 9:
            if pole._pole[self._y - 1][self._x] == 1 or pole._pole[self._y][self._x - 1] == 1 or \
                    pole._pole[self._y - 1][self._x - 1] == 1:
                return True

        if self._tp == 1:
            counter_x = self._x
            for line in range(self._length):

                if self._x in range(1, 9):

                    if self._y in range(1, 9):
                        if pole._pole[self._y - 1][counter_x - 1] == 1 or pole._pole[self._y - 1][counter_x] == 1 or \
                                pole._pole[self._y - 1][counter_x + 1] == 1:
                            return True
                        if pole._pole[self._y][counter_x - 1] == 1 or pole._pole[self._y][counter_x] == 1 or \
                                pole._pole[self._y][counter_x + 1] == 1:
                            return True
                        if pole._pole[self._y + 1][counter_x - 1] == 1 or pole._pole[self._y + 1][counter_x] == 1 or \
                                pole._pole[self._y + 1][counter_x + 1] == 1:
                            return True

                    if self._y == 0:
                        if pole._pole[self._y][counter_x - 1] == 1 or pole._pole[self._y][counter_x] == 1 or \
                                pole._pole[self._y][counter_x + 1] == 1:
                            return True
                        if pole._pole[self._y + 1][counter_x - 1] == 1 or pole._pole[self._y + 1][counter_x] == 1 or \
                                pole._pole[self._y + 1][counter_x + 1] == 1:
                            return True

                    if self._y == 9:
                        if pole._pole[self._y - 1][counter_x - 1] == 1 or pole._pole[self._y - 1][counter_x] == 1 or \
                                pole._pole[self._y - 1][counter_x + 1] == 1:
                            return True
                        if pole._pole[self._y][counter_x - 1] == 1 or pole._pole[self._y][counter_x] == 1 or \
                                pole._pole[self._y][counter_x + 1] == 1:
                            return True

                if self._x == 0:
                    if pole._pole[self._y - 1][counter_x] == 1 or pole._pole[self._y - 1][counter_x + 1] == 1:
                        return True
                    if pole._pole[self._y][counter_x] == 1 or pole._pole[self._y][counter_x + 1] == 1:
                        return True
                    if pole._pole[self._y + 1][counter_x] == 1 or pole._pole[self._y + 1][counter_x + 1] == 1:
                        return True

                if self._x == 9:
                    if pole._pole[self._y - 1][counter_x] == 1 or pole._pole[self._y - 1][counter_x - 1] == 1:
                        return True
                    if pole._pole[self._y][counter_x] == 1 or pole._pole[self._y][counter_x - 1] == 1:
                        return True
                    if pole._pole[self._y + 1][counter_x] == 1 or pole._pole[self._y + 1][counter_x - 1] == 1:
                        return True

                counter_x += 1

        if self._tp == 2:
            counter_y = self._y
            for line in range(self._length):

                if counter_y in range(1, 9):

                    if self._x in range(1, 9):
                        if pole._pole[counter_y - 1][self._x - 1] == 1 or pole._pole[counter_y - 1][self._x] == 1 or \
                                pole._pole[counter_y - 1][self._x + 1] == 1:
                            return True
                        if pole._pole[counter_y][self._x - 1] == 1 or pole._pole[counter_y][self._x] == 1 or \
                                pole._pole[counter_y][self._x + 1] == 1:
                            return True
                        if pole._pole[counter_y + 1][self._x - 1] == 1 or pole._pole[counter_y + 1][self._x] == 1 or \
                                pole._pole[counter_y + 1][self._x + 1] == 1:
                            return True

                    if self._x == 0:
                        if pole._pole[counter_y - 1][self._x] == 1 or pole._pole[counter_y - 1][self._x + 1] == 1:
                            return True
                        if pole._pole[counter_y][self._x] == 1 or pole._pole[counter_y][self._x + 1] == 1:
                            return True
                        if pole._pole[counter_y + 1][self._x] == 1 or pole._pole[counter_y + 1][self._x + 1] == 1:
                            return True

                    if self._x == 9:
                        if pole._pole[counter_y - 1][self._x] == 1 or pole._pole[counter_y - 1][self._x - 1] == 1:
                            return True
                        if pole._pole[counter_y][self._x] == 1 or pole._pole[counter_y][self._x - 1] == 1:
                            return True
                        if pole._pole[counter_y + 1][self._x] == 1 or pole._pole[counter_y + 1][self._x - 1] == 1:
                            return True

                if counter_y == 0:
                    if pole._pole[counter_y][self._x - 1] == 1 or pole._pole[counter_y][self._x] == 1 or \
                            pole._pole[counter_y][self._x + 1] == 1:
                        return True
                    if pole._pole[counter_y + 1][self._x - 1] == 1 or pole._pole[counter_y + 1][self._x] == 1 or \
                            pole._pole[counter_y + 1][self._x + 1] == 1:
                        return True

                if counter_y == 9:
                    if pole._pole[counter_y - 1][self._x - 1] == 1 or pole._pole[counter_y - 1][self._x] == 1 or \
                            pole._pole[counter_y - 1][self._x + 1] == 1:
                        return True
                    if pole._pole[counter_y][self._x - 1] == 1 or pole._pole[counter_y][self._x] == 1 or \
                            pole._pole[counter_y][self._x + 1] == 1:
                        return True

                counter_y += 1

        return False

    def is_out_pole(self, game_pole_size):
        """Checking for the ship to leave the playing pole"""
        if self._tp == 2 and self._y + len(self._cells) > game_pole_size:
            return True
        if self._tp == 1 and self._x + len(self._cells) > game_pole_size:
            return True
        return False

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