import random
import time

from tqdm import tqdm

from Grid import sudokuGrid


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
    print(sudoku)
    sudoku.solve()
    print(sudoku)
    print(f"solved: {sudoku.solved()}")


# solve_simple()
solve_db()
