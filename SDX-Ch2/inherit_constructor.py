import math

def shape_density(thing, weight):
    return weight / call(thing, "area")

# [shape]
def shape_new(name):
    return {
        "name": name,
        "_class": Shape
    }

Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None,
    "_new": shape_new,
    "_type": "Shape",
    "_cache": {}
}
# [/shape]

# [shape2D]
def shape2D_new(name):
    return make(Shape, name) | {
        "_class": Shape2D
    }

Shape2D = {
    "_parent": Shape,
    "_new": shape2D_new,
    "_type": "Shape2D",
    "_cache": {}
}

# [/shape2D]

# [make]
def make(cls, *args):
    return cls["_new"](*args)
# [/make]

def square_perimeter(thing):
    return 4 * thing["side"]

def square_area(thing):
    return thing["side"] ** 2

# [square]
def square_new(name, side):
    return make(Shape, name) | {
        "side": side,
        "_class": Square
    }

Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "_classname": "Square",
    "_parent": Shape,
    "_new": square_new
}
# [/square]

# [line]
def line_new(name, length):
    return make(Shape2D, name) | {
        "length": length,
        "_class": Line
    }

def line_length(thing):
    return thing["length"]

Line = {
    "length": line_length,
    "_parent": Shape2D,
    "_new": line_new
}
# [/line]

def circle_perimeter(thing):
    return 2 * math.pi * thing["radius"]

def circle_area(thing):
    return math.pi * thing["radius"] ** 2

def circle_new(name, radius):
    return make(Shape, name) | {
        "radius": radius,
        "_class": Circle
    }

Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "_classname": "Circle",
    "_parent": Shape,
    "_new": circle_new
}
def find(cls, method_name):
    current_cls = cls
    while current_cls is not None:
        if method_name in current_cls:
            return current_cls[method_name]
        current_cls = current_cls["_parent"]
    raise NotImplementedError(method_name)

def call(thing, method_name, *args, **kwargs):
    method = find(thing["_class"], method_name)
    return method(thing, *args, **kwargs)

# [call]
examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
for ex in examples:
    n = ex["name"]def shape_new(name):
        return {
            "name": name,
            "_class": Shape,
            "_type": lambda: "Shape",
        }

Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None,
    "_new": shape_new,
    "_type": lambda: "Shape"
}

def shape2D_new(name):
    return make(Shape, name) | {
        "_class": Shape2D,
        "_type": lambda: "Shape2D",
    }

Shape2D = {
    "_parent": Shape,
    "_new": shape2D_new,
    "_length": shape2D_length,
    "_type": lambda: "Shape2D",
    "_cache": {}
}
d = call(ex, "density", 5)
print(f"{n}: {d:.2f}")
# [/call]
