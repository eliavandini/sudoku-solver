from ninelets import Column, Line, Square


class sudokuGrid:
    raw = []
    rating: str
    lines: list[Line] = []
    columns: list[Column] = []
    squares: list[Square] = []

    def __init__(self, rawInput: str, rating: str = "0.0"):
        """
        main class for sudoku numbermanaging
        :param rawInput: generates a sudoku grid based
        on the rawInput list. The numers inside the list
        are the numbers from left to right of the rows
        of a normal sudokugrid, starting from the top
        """
        self.raw = [int(i) for i in rawInput]
        self.rating = rating
        self.lines = [Line(self, i) for i in range(9)]
        self.columns = [Column(self, i) for i in range(9)]
        self.squares = [Square(self, i) for i in range(9)]

    def getLine(self, line):
        """
        returns a list containing the values of a given line
        :param line: indicates the line to return
        """
        return self.raw[line * 9 : ((line * 9) + 9)]

    def getColumn(self, column):
        """
        returns a list containing the values of a given column
        :param column: indicates the column to return
        """
        return self.raw[column:81:9]

    def getSquare(self, square):
        """
        returns a list containing the values of a given Square
        :param Square: indicates the column to return
        """
        f = ((square // 3) * 27) + ((square % 3) * 3)
        return (
            self.raw[f : f + 3] + self.raw[f + 9 : f + 12] + self.raw[f + 18 : f + 21]
        )

    def getCellParents(self, rawIndex) -> tuple[Line, Column, Square]:
        return (
            self.lines[rawIndex // 9],
            self.columns[rawIndex % 9],
            self.columns[(((rawIndex // 9) // 3) * 3) + ((rawIndex % 9) // 3)],
        )

    def __str__(self):
        return "\n".join([str(self.getLine(i)) for i in range(9)]) + "\n"

    def solved(self):
        if self.raw.count(0) > 0:
            return False
        for line, col, square in zip(self.lines, self.columns, self.squares):
            if not line.isStraight() or not col.isStraight() or not square.isStraight():
                return False
        return True

    def solve(self):

        ok0 = True
        while ok0:
            sudoku_hash = self.__hash__()
            for line, col, square in zip(self.lines, self.columns, self.squares):
                line.tryComplete()
                col.tryComplete()
                square.tryComplete()

            for square in self.squares:
                if square.completed:
                    continue
                for missing in square.getMissing():
                    available = -1
                    for target in square.getMissingPos():
                        line, column, _ = square.getCellParents(target)
                        if missing not in line and missing not in column:
                            if available != -1:
                                available = -1
                                break
                            available = target
                    if available != -1:
                        square[available] = missing

            # self.printGrid()
            if sudoku_hash == self.__hash__():
                break

    def __hash__(self) -> int:
        return hash("".join(str(i) for i in self.raw))
