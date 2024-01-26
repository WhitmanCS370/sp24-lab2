import math

Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None,
    "_new": shape_new,
    "_type": "Shape",
    "_cache": {},
    "class_method": shape_class_method,  # Class method
    "static_method": static(shape_static_method),  # Static method
}

def shape_density(thing, weight):
    return weight / call(thing, "area")

# [shape]
def shape_new(name):
    return {
        "name": name,
        "_class": Shape
    }

def shape_class_method(cls, *args):
    # Implement your class method here
    pass

def shape_static_method(*args):
    # Implement your static method here
    pass


# [/shape]

# [shape2D]
Shape2D = {
    "_parent": Shape,
    "_new": shape2D_new,
    "type": "Shape2D",
    "_cache": {},
}


def shape2D_new(name):
    return make(Shape, name) | {
        "_class": Shape2D
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
Line = {
    "length": line_length,
    "_parent": Shape2D,
    "_new": line_new,
    "_type": "Line",
    "_cache": {},
}

def line_new(name, length):
    return make(Shape2D, name) | {
        "length": length,
        "_class": Line
    }

def line_length(thing):
    return thing["length"]

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
    n = ex["name"]
    

def shape_new(name):
        return {
            "name": name,
            "_class": Shape,
            "_type": lambda: "Shape",
        }

def shape2D_new(name):
    return make(Shape, name) | {
        "_class": Shape2D,
        "_type": lambda: "Shape2D",
    }

# [search]
def call(thing, method_name, *args):
    method = find(thing["_class"], method_name)
    return method(thing, *args)

def find(cls, method_name):
    while cls is not None:
        if method_name in cls:
            return cls[method_name]
        cls = cls["_parent"]
    raise NotImplementedError("method_name")
# [/search]

# [use]
examples = [square_new("sq", 3), circle_new("ci", 2)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")
# [/use]
