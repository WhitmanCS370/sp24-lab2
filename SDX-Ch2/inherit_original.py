import math

class Shape2D:
    def __init__(self, name):
        self.name = name

    def perimeter(self):
        raise NotImplementedError("perimeter")

    def area(self):
        raise NotImplementedError("area")

# [shape]
class Shape(Shape2D):
    def __init__(self, name):
        self.name = name

    def density(self, weight):
        return weight / self.area()
# [/shape]

class Square(Shape):
    def __init__(self, name, side):
        super().__init__(name)
        self.side = side

    def perimeter(self):
        return 4 * self.side

    def area(self):
        return self.side ** 2

class Line(Shape):
    def __init__(self, name, length):
        super().__init__(name)
        self.length = length

class Circle(Shape2D):
    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius
    

# [use]
examples = [Square("sq", 3), Circle("ci", 2)]
for ex in examples:
    n = ex.name
    d = ex.density(5)
    print(f"{n}: {d:.2f}")
# [/use]
