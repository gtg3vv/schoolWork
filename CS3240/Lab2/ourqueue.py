__author__ = 'horton'

class OurQueue:

    def __init__(self, init_values=[]):
        self.values = init_values

    def __str__(self):
        return str(self.values)

    def __len__(self):
        return len(self.values)

    def add(self, item):
        self.values.append(item)

    def front(self):
        if len(self.values) == 0:
            return None
        return self.values[0]

    def remove(self):
        if len(self.values) == 0:
            return None
        result = self.values[0]
        del self.values[0]
        return result


if __name__ == '__main__':
    pass
