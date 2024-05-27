# move_ships() - перемещает каждый корабль из коллекции _ships на одну клетку (случайным образом вперед или назад)
# в направлении ориентации корабля; если перемещение в выбранную сторону невозможно (другой корабль или пределы
# игрового поля), то попытаться переместиться в противоположную сторону, иначе (если перемещения невозможны), оставаться на месте;

from random import randint


class GamePole:
    """This class provide work with the game pole and description it"""
    def __init__(self, size):
        self.__check_size(size)
        self._size = size
        self._ships = []
        self._pole = self.__form_pole()

    @classmethod
    def __check_size(cls, size):
        """Check size of game pole"""
        if type(size) != int or size <= 0:
            raise TypeError('Invalid size value. Please enter an integer positive value')

    def __form_pole(self):
        """Game pole formation.
        Game pole is two-dimensional tuple with size x size elements"""
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
        """Placing the ship on the pole"""
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

    def __install_coords(self):
        """Assignment of start coordinates"""
        initial_limit = 0
        final_limit = self._size - 1
        for ship in self._ships:
            intersection = True
            checking_ships = self._ships[:]
            checking_ships.remove(ship)
            while intersection is True:
                coord_x = randint(initial_limit, final_limit)
                coord_y = randint(initial_limit, final_limit)
                ship.set_start_coords(coord_x, coord_y)
                if ship.is_out_pole(self._size):
                    continue
                self.__put_on(ship)
                intersection_checklist = []
                for checking_ship in checking_ships:
                    intersection_checklist.append(ship.is_collide(checking_ship))
                if any(intersection_checklist):
                    intersection = True
                else:
                    intersection = False

    def init(self):
        """Initial initialization of the game pole"""
        self.__form_ships()
        self.__install_coords()

    def get_ships(self):
        """Moving each ship from the _ships collection"""
        return self._ships

    def show(self):
        """Displaying the game pole in the console"""
        for line in self._pole:
            print(*line, end='\n')

    def get_pole(self):
        """Getting the current game pole"""
        return tuple((tuple(line) for line in self._pole))