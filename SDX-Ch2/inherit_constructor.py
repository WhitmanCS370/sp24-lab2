import math


# [shape]
def shape_new(name):
    return {
        "name": name,
        "_class": Shape
    }

Shape = {
    "_classname": "Shape",
    "_parent": None,
    "_new": shape_new,
    "_cache": {},
    "_static_methods": set()
}
# [/shape]

def shape2d_density(thing, weight):
    return weight / call(thing, "area")

def shape2d_new(name):
    return make(Shape, name) | {
        "density": shape2d_density,
        "_class": Shape2D
    }

# [shape2d]
Shape2D = {
    "density": shape2d_density,
    "_classname": "Shape2d",
    "_parent": Shape,
    "_new": shape2d_new,
    "_cache": {},
    "_static_methods": set()
}

# [make]
def make(cls, *args):
    return cls["_new"](*args)
# [/make]

def square_perimeter(thing):
    return 4 * thing["side"]

def square_area(thing):
    return thing["side"] ** 2

def num_corners():
    return 4

# [square]
def square_new(name, side):
    return make(Shape, name) | {
        "side": side,
        "_class": Square
    }

Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "num_corners": num_corners,
    "_classname": "Square",
    "_parent": Shape2D,
    "_new": square_new,
    "_cache": {},
    "_static_methods": {"num_corners"}
}
# [/square]

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
    "_parent": Shape2D,
    "_new": circle_new,
    "_cache": {},
    "_static_methods": set()
}

# [line]
def line_new(name, length):
    return make(Shape, name) | {
        "length": length,
        "_class": Line
    }

def line_length(thing):
    return thing["length"]

Line = {
    "length": line_length,
    "_classname": "Line",
    "_parent": Shape,
    "_new": line_new,
    "_cache": {},
    "_static_methods": set()
}
# [/line]

# We think that it might make more sense to have a global cache
# rather than a separate one for each object.
# Adding caching is not very many extra lines in the find function,
# but the user needs to remember to add a cache to every object (without a global cache).
def find(cls, method_name):
    if cls is None:
        raise NotImplementedError("method_name")
    if method_name in cls["_cache"]:
        return cls["_cache"]
    if method_name in cls:
        return cls[method_name]
    result = find(cls["_parent"], method_name)
    cls["_cache"]["method_name"] = result
    return result

def call(thing, method_name, *args, **kwargs):
    method = find(thing["_class"], method_name)
    if method_name in thing["_class"]["_static_methods"]:
        return method(*args, **kwargs)
    return method(thing, *args, **kwargs)

def type(thing):
    return thing["_class"]["_classname"]

# [call]
examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")
# [/call]
    
l = make(Line, "line", 5)
if call(l, "length") != 5:
    print("Incorrect line length")

if type(l) != "Line":
    print("Incorrect line type")

s = make(Square, "s", 3)
if call(s, "num_corners") != 4:
    print("Incorrect number of corners")

# 6
    # Class methods depend on the class (ex: area of a particular square)
    # Static methods are the same for every instance of a class (ex: number of corners in a square)
