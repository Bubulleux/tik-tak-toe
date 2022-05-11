class RangeXD:
    def __init__(self, *args):
        self.ranges = []
        self.end = False
        for _arg in args:
            if type(_arg) == tuple:
                print(_arg[0], "_arg[0]")
                if len(_arg) == 1:
                    self.ranges.append((0, _arg[0], 1))
                elif len(_arg) == 2:
                    self.ranges.append((_arg[0], _arg[1], 1))
                elif len(_arg) == 3:
                    self.ranges.append(_arg)
            elif type(_arg) == list:
                self.ranges.append(_arg)
            elif type(_arg) == float or type(_arg) == int:
                self.ranges.append((0, _arg, 1))
            else:
                raise TypeError()
        self.counter = []
        for _range in self.ranges:
            if type(_range) == tuple:
                self.counter.append(_range[0])
            else:
                self.counter.append(0)


    def next(self, index):
        if index >= len(self.ranges) or index < 0:
            return True

        if type(self.ranges[index]) == tuple:
            start, stop, step = self.ranges[index]
        else:
            start = 0
            stop = len(self.ranges[index])
            step = 1
        self.counter[index] += step

        if (step > 0 and  self.counter[index] >= stop) or (step < 0 and self.counter[index] <= stop):
            self.counter[index] = start
            return self.next(index + 1)
        return False

    def __iter__(self):
        return self

    def __next__(self):
        output = tuple([i if type(_range) == tuple else _range[i]  for i, _range in zip(self.counter, self.ranges)])
        if self.end:
            raise StopIteration()
        self.end = self.next(0)
        return output






