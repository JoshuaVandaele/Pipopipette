from jeu.engine.Square.Square import Square
from functools import wraps
from time import perf_counter

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        print(f'Benchmarking function {f.__name__}')
        ts = perf_counter()
        result = list(f(*args, **kw))
        te = perf_counter()
        print(f'Function {f.__name__} took {te-ts:2.4f}')
        return result
    return wrap

list_square = [Square(i) for i in range(1000)]

@timing
def list_moves1():
    # List of checked sides: dict[side, list[square_id]]
    checked_sides: dict[str, list[int]] = {'l': [], 'r': [], 't': [], 'd': []}
    width: int = 10
    
    for square in list_square:
        if square.square_owner == -1:
            if square.left.owner_ID == -1 and (square.ID not in checked_sides["l"]):
                checked_sides["r"].append(square.ID-1)
                yield square.ID, 'l'
            if square.top.owner_ID == -1 and (square.ID not in checked_sides["t"]):
                checked_sides["d"].append(square.ID-width)
                yield square.ID, 't'
            if square.right.owner_ID == -1 and (square.ID not in checked_sides["r"]):
                checked_sides["l"].append(square.ID+1)
                yield square.ID, 'r'
            if square.down.owner_ID == -1 and (square.ID not in checked_sides["d"]):
                checked_sides["t"].append(square.ID+width)
                yield square.ID, 'd'

@timing
def list_moves2():
    checked_sides: dict[str, set[int]] = {'l': set(), 'r': set(), 't': set(), 'd': set()}
    width: int = 10

    for square in list_square:
        if square.square_owner == -1:
            square_id = square.ID

            if square.left.owner_ID == -1 and square_id not in checked_sides["l"]:
                checked_sides["r"].add(square_id - 1)
                yield square_id, 'l'

            if square.top.owner_ID == -1 and square_id not in checked_sides["t"]:
                checked_sides["d"].add(square_id - width)
                yield square_id, 't'

            if square.right.owner_ID == -1 and square_id not in checked_sides["r"]:
                checked_sides["l"].add(square_id + 1)
                yield square_id, 'r'

            if square.down.owner_ID == -1 and square_id not in checked_sides["d"]:
                checked_sides["t"].add(square_id + width)
                yield square_id, 'd'


print(list_moves1() == list_moves2())
