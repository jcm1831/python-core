import abc
from random import randint


class MoveStrategy(abc.ABC):
    @abc.abstractmethod
    def __call__(self, board) -> None:
        raise NotImplementedError()


class RandomMoveStrategy(MoveStrategy):
    def __call__(self, board):
        print('Making move level "easy"')
        is_occupied = True
        while is_occupied:
            x, y = randint(0, 2), randint(0, 2)
            if board[x][y] == ' ':
                return x, y
            else:
                continue


class InputMoveStrategy(MoveStrategy):
    def __call__(self, board):
        coordinates = []
        move_is_valid = True
        while move_is_valid:
            move = input('Enter the coordinates: ')
            # check if input type is valid
            try:
                coordinates = [int(x) for x in move.split(' ')]
            except ValueError:
                print('You should enter numbers!')
                continue

            # check if input range is valid
            valid_range = range(1, 4, 1)
            if any([x not in valid_range for x in coordinates]):
                print('Coordinates should be from 1 to 3!')
                continue

            # check if cell is already occupied
            x, y = coordinates
            if board[x - 1][y - 1] != ' ':
                print('This cell is occupied! Choose another one!')
                continue

            move_is_valid = False
        return [(x - 1) for x in coordinates]
