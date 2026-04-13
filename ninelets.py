from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Grid import sudokuGrid


class Ninelet:
    def __init__(self, grid: "sudokuGrid", pos) -> None:
        self.grid: sudokuGrid = grid
        self.pos = pos
        self.completed = self.isStraight()

    @abstractmethod
    def value(self) -> list[int]:
        pass

    def index(self, val) -> int:
        return self.value().index(val)

    def count(self, val) -> int:
        return self.value().count(val)

    def isStraight(self):
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if self.count(i) != 1:
                return False
        return True

    def getMissing(self):
        """
        returns a list containing the numbers from 1 to 9 missing
        """
        param = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        out = []
        for t in param:
            if not self.count(t) > 0:
                out.append(t)
        return out

    def getMissingPos(self):
        """
        :return returns a list containing all empty cells
        """
        indices = []
        for i, cell in enumerate(self):
            if cell == 0:
                indices.append(i)
        return indices

    def tryComplete(self) -> bool:
        missing_index = -1
        missing = -1
        for i, t in enumerate(self.value()):
            if t != 0:
                if missing_index != -1:
                    return False
                missing_index = i
                missing = t

        if missing_index != -1:
            return True
        self.value()[missing_index] = missing
        self.completed = True
        return True

    @abstractmethod
    def rawIndex(self, offset=0) -> int:
        pass

    def getCellParents(self, offset):
        return self.grid.getCellParents(self.rawIndex(offset))

    def __iter__(self):
        return self.value().__iter__()

    def __getitem__(self, index) -> int:
        return self.value().__getitem__(index)

    def __setitem__(self, index, val) -> None:
        if self.value().__getitem__(index) != 0:
            raise Exception("cell is not empty")
        if val not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            raise Exception("invalid value")
        return self.grid.raw.__setitem__(self.rawIndex(index), val)

    def __len__(self) -> int:
        return 9

    def __contains__(self, key) -> bool:
        return self.value().__contains__(key)

    def __eq__(self, value) -> bool:
        return self.value().__eq__(value)

    def __str__(self) -> str:
        return str(self.value())


class Line(Ninelet):
    def value(self) -> list[int]:
        return self.grid.getLine(self.pos)

    def rawIndex(self, offset=0):
        return self.pos * 9 + offset


class Column(Ninelet):
    def value(self) -> list[int]:
        return self.grid.getColumn(self.pos)

    def rawIndex(self, offset=0):
        return self.pos + offset * 9


class Square(Ninelet):
    def value(self) -> list[int]:
        return self.grid.getSquare(self.pos)

    def rawIndex(self, offset=0):
        f = ((self.pos // 3) * 27) + ((self.pos % 3) * 3)
        return f + offset + ((offset // 3) * 6)
