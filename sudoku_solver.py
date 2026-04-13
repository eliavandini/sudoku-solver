import random
import time

from tqdm import tqdm


class sudokuGrid:
    raw = []
    rating: str

    def __init__(self, rawInput: str, rating: str = "0.0"):
        """
        main class for sudoku numbermanaging
        :param rawInput: generates a sudoku grid based
        on the rawInput list. The numers inside the list
        are the numbers from left to right of the rows
        of a normal sudokugrid, starting from the top
        """
        # output = ""
        # for i in rawInput:
        #     output = f"{output}{i},"
        # output = output[:-1]
        self.raw = [int(i) for i in rawInput]
        self.rating = rating

    def setLine(self, Input, line):
        """
        set a line to a given list
        :param line: represents the line to be modified
        :param Input: represents the Input List witch contains 9 caracters
        """
        self.raw[line * 9 : ((line * 9) + 9)] = Input

    def getLine(self, line):
        """
        returns a list containing the values of a given line
        :param line: indicates the line to return
        """
        return self.raw[line * 9 : ((line * 9) + 9)]

    def setColumn(self, Input, column):
        """
        set a colums to a given list
        :param column: represents the line to be modified
        :param Input: represents the Input List witch contains 9 caracters
        """
        x = 0
        for i in range(column, 81, 9):
            self.raw[i] = Input[x]
            x += 1

    def getColumn(self, column):
        """
        returns a list containing the values of a given column
        :param column: indicates the column to return
        """
        return self.raw[column:81:9]

    def setSquare(self, Input, square):
        """
        set a colums to a given list
        :param square: represents the square to be modified
        :param Input: represents the Input List witch contains 9 caracters
        """
        f = ((square // 3) * 27) + ((square % 3) * 3)
        self.raw[f : f + 3] = Input[0:3]
        self.raw[f + 9 : f + 12] = Input[3:6]
        self.raw[f + 18 : f + 21] = Input[6:9]

    def getSquare(self, square):
        """
        returns a list containing the values of a given Square
        :param Square: indicates the column to return
        """
        f = ((square // 3) * 27) + ((square % 3) * 3)
        return (
            self.raw[f : f + 3] + self.raw[f + 9 : f + 12] + self.raw[f + 18 : f + 21]
        )

    # def setCell(self, x: int, y: int, val: int):

    def completeLine(self, index):
        missing_index = -1
        missing = -1
        for i, t in enumerate(self.getLine(index)):
            if t != 0:
                if missing_index != -1:
                    return
                missing_index = i
                missing = t

        if missing_index != -1:
            return
        self.raw[getRawPos(index, missing_index, "l")] = missing

    def completeColumn(self, index):
        missing_index = -1
        missing = -1
        for i, t in enumerate(self.getLine(index)):
            if t != 0:
                if missing_index != -1:
                    return
                missing_index = i
                missing = t

        if missing_index != -1:
            return
        self.raw[getRawPos(index, missing_index, "c")] = missing

    def completeSquare(self, index):
        missing_index = -1
        missing = -1
        for i, t in enumerate(self.getLine(index)):
            if t != 0:
                if missing_index != -1:
                    return
                missing_index = i
                missing = t

        if missing_index != -1:
            return
        self.raw[getRawPos(index, missing_index, "s")] = missing

    def printGrid(self):
        print(" ")
        for i in range(9):
            print(self.getLine(i))
        print(" ")

    def solved(self):
        if self.raw.count(0) > 0:
            return False
        for i in range(0, 9):
            if (
                not isStraight(self.getColumn(i))
                or not isStraight(self.getSquare(i))
                or not isStraight(self.getLine(i))
            ):
                return False
        return True

    def solve(self):

        ok0 = True
        while ok0:
            sudoku_hash = self.__hash__()

            for i in range(0, 9):
                self.completeLine(i)
                self.completeColumn(i)
                self.completeSquare(i)

            for i in range(0, 9):
                square = self.getSquare(i)
                for missing in getMissing(square):
                    available = -1
                    for target_index, target_cell in enumerate(square):
                        if target_cell != 0:
                            continue
                        line = self.getLine((i - (i % 3)) + (target_index // 3))
                        column = self.getColumn(((i * 3) % 9) + (target_index % 3))
                        if line.count(missing) <= 0 and column.count(missing) <= 0:
                            if available != -1:
                                available = -1
                                break
                            available = target_index
                    if available != -1:
                        # print(self.raw[getRawPos(i, available, "C")])
                        self.raw[getRawPos(i, available, "s")] = missing

            # self.printGrid()
            if sudoku_hash == self.__hash__():
                break

    def __hash__(self) -> int:
        return hash("".join(str(i) for i in self.raw))


def isStraight(Input: list[int]):
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        if Input.count(i) != 1:
            return False
    return True


def getMissing(Input):
    """
    returns a list containing the numbers from 1 to 9 missing in Input
    :param Input: a 9 number long list of numbers to be searched
    """
    param = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    out = []
    for t in param:
        if not Input.count(t) > 0:
            out.append(t)
    return out


def getMissingPos(Input):
    """
    :param Input: a 9 number long list of numbers to be searched
    :return returns a list containing all positions of 0
    """
    indices = []
    for e in range(len(Input)):
        if Input[e] == 0:
            indices.append(e)
    return indices


def getRawPos(subIndex: int, index: int, mode="r") -> int:
    """
    :param subIndex: Index of the subclass
    :param Index: Index of the searched number inside teh subclass
    :param mode: type of subclass to search ["r" = raw, "l" = Line, "c" = Column, "C" = Square]
    :return: returns the position of Index inside sudokuSolver.raw
    """
    if mode == "r":
        return index
    elif mode == "l":
        return (subIndex * 9) + index
    elif mode == "c":
        return (index * 9) + subIndex
    elif mode == "s":
        f = ((subIndex // 3) * 27) + ((subIndex % 3) * 3)
        if index < 3:
            return f + (index % 3)
        elif index < 6:
            return f + (index % 3) + 9
        else:
            return f + (index % 3) + 18
    return index


def getLine(RawIndex):
    """
    :param RawIndex: Index to be searched
    :return: The Line the RawIndex touches
    """
    return RawIndex // 9


def getColumn(RawIndex):
    """
    :param RawIndex: Index to be searched
    :return: The Column the RawIndex touches
    """
    return RawIndex % 9


def getSquare(RawIndex):
    """
    :param RawIndex: Index to be searched
    :return: The Square the RawIndex touches
    """
    return ((RawIndex // 9) // 3) * 3 + (RawIndex % 9) // 3


def listOverride(InputList, Input, Index):
    """
    :param InputList: Original List
    :param Input: List to be inserted
    :param Index: Index from where to start to overridden
    :return: returns a List of the sae lenght of Inputlist but
    the Items contained in it are overwritten by the Items of
    the second list, starting by a given Index
    """
    return (
        InputList[:Index]
        + Input[Index - len(InputList) - 1 : len(InputList) - Index]
        + InputList[Index + len(Input) :]
    )


def fillMissing(Input):
    """
    Automaticly fills in the last missing gap. won't work
    if there is more than one ore none
    :param Input: Input list of 9 numbers
    :return: A full list from the Input
    """
    if len(getMissing(Input)) == 1:
        return listOverride(Input, getMissing(Input), getMissingPos(Input)[0])
    return Input


def solve_db():
    modes = ["easy", "medium", "hard", "diabolical"]
    # modes = ["easy"]
    sudokus: list[sudokuGrid] = []
    for sudoku_mode in modes:
        with open(f"sudoku-exchange-puzzle-bank/{sudoku_mode}.txt") as databse_file:
            for num, line in enumerate(databse_file):
                if random.randint(0, 50) > 1:
                    continue
                line = line.strip().split(" ")
                sudokus.append(sudokuGrid(line[1], line[3]))

    out = []
    start_time = time.time()
    prog_bar = tqdm(
        total=len(sudokus),
    )
    for sudoku in sudokus:
        sudoku.solve()
        out.append((sudoku.rating, sudoku.solved()))
        prog_bar.update()

    end_time = time.time()
    ratings: dict = {}
    total_sum = 0
    for res in out:
        rate = ratings.get(res[0], (0, 0))[0]
        count = ratings.get(res[0], (0, 0))[1]
        new_rate = (rate * count + int(res[1])) / (count + 1)
        ratings[res[0]] = (new_rate, count + 1)
        if res[1]:
            total_sum += 1

    print("Performance per rating: ")
    for k, v in sorted(ratings.items(), key=lambda x: float(x[0])):
        print(f"{k}: {round(v[0] * 100, 2)}% ({v[1]} total)")
    print(
        f"overall: {round((total_sum / len(out)) * 100, 2)}% ({len(out)} total) in {end_time - start_time} seconds ({(round(end_time - start_time, 2)) / len(out)} per sudoku)"
    )


def solve_simple():
    sudoku = sudokuGrid(
        "050703060007000800000816000000030000005000100730040086906000204840572093000409000"
    )
    sudoku.printGrid()
    sudoku.solve()
    sudoku.printGrid()
    print(f"solved: {sudoku.solved()}")


# solve_simple()
solve_db()
