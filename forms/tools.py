from datetime import datetime

class TimeIt(object):
    def __init__(self, name, silent=False):
        self.name = name
        self.start = 0
        self.end = 0
        self.silent = silent

    def __enter__(self):
        self.start = datetime.now()

    def __exit__(self, *args, **kwds):
        self.end = datetime.now()
        if not self.silent:
            s = self.elapsed().total_seconds()
            print(s)
            if s == 0:
                return
            fps = 1.0/s
            print(f'Elapsed {self.name}: {self.elapsed()} Frames: {fps}')

    def elapsed(self):
        return self.end - self.start

def product(*arrays, repeat=1):
    pools = [tuple(pool) for pool in arrays] * repeat
    result = [[]]

    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

if __name__ == '__main__':
    with TimeIt('product') as t:
        a = 'abc'
        b = 'def'
        c = product(range(2), repeat=8)
    print(tuple(c))

