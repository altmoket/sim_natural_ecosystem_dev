import heapq

class heap:
    def push(iterable, obj):
        heapq.heappush(iterable, MaxHeapObj(obj))

    def pop(iterable):
        return heapq.heappop(iterable).val

class MaxHeapObj(tuple):
    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val > other.val

    def __gt__(self, other):
        return self.val < other.val

    def __eq__(self, other):
        return self.val == other.val

    def __repr__(self) -> str:
        return self.val.__repr__()

    def __str__(self) -> str:
        return self.val.__str__()