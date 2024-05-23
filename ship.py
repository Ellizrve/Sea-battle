# Список _cells будет сигнализировать о попадании соперником в какую-либо палубу корабля. Если стоит 1, то попадания не
# было, а если стоит значение 2, то произошло попадание в соответствующую палубу.
# При попадании в корабль (хотя бы одну его палубу), флаг _is_move устанавливается в False и перемещение корабля по
# игровому полю прекращается.
# В самом классе Ship должны быть реализованы следующие методы (конечно, возможны и другие, дополнительные):
# move(go) - перемещение корабля в направлении его ориентации на go клеток (go = 1 - движение в одну сторону на клетку;
# go = -1 - движение в другую сторону на одну клетку); движение возможно только если флаг _is_move = True;
# is_collide(ship) - проверка на столкновение с другим кораблем ship (столкновением считается, если другой корабль или
# пересекается с текущим или просто соприкасается, в том числе и по диагонали); метод возвращает True, если столкновение
# есть и False - в противном случае;
# is_out_pole(size) - проверка на выход корабля за пределы игрового поля (size - размер игрового поля, обычно, size = 10);
# возвращается булево значение True, если корабль вышел из игрового поля и False - в противном случае;


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self.__check_lenght(length)
        self.__check_tp(tp)
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = self.__form_cells()

    @classmethod
    def __check_lenght(cls, length):
        if type(length) != int or length not in range(1, 5):
            raise TypeError('Invalid length value. Please enter an integer value from 1 to 4')

    @classmethod
    def __check_tp(cls, tp):
        if type(tp) != int or tp not in range(1, 3):
            raise TypeError('Invalid orientation value. Please enter an integer value: 1 (horizontal) or 2 (vertical)')

    # @classmethod
    # def __check_coord(cls, coord):
    #     if type(coord) != int or coord not in range(0, GamePole._size):
    #         raise TypeError(f'Incorrect {coord} coordinate value. Please enter an integer value from 0 to {GamePole._size}')

    def __form_cells(self):
        return [1 for x in range(self._length)]

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    # def move(self, go):
    #     if self._is_move:
    #
    #
    # def is_collide(ship):
    #     return True
    #     # return False
    #
    # def is_out_pole(self, GamePole._size):

    def __check_indx(self, indx):
        if type(indx) != int or indx not in range(0, self._length):
            raise TypeError(f'Invalid index value. Please enter an integer value from 0 to {self._length - 1}')

    @classmethod
    def __check_value(cls, value):
        if type(value) != int or value not in range(1, 3):
            raise TypeError('Invalid value. Please enter an integer value: 1 or 2')

    def __getitem__(self, indx):
        self.__check_indx(indx)
        return self._cells[indx]

    def __setitem__(self, indx, value):
        self.__check_indx(indx)
        self._cells[indx] = value