import math

def shape_density(thing, weight):
    return weight / call(thing, "area")

def new_shape2D(name):
 return make(name) | {
     "name": name,
     "_class": Shape2D
 }

Shape2D = {
    "density": shape_density,
    "_new" : new_shape2D,
    "_class" : "Shape2D"
}


# [shape]
def shape_new(name):
    return {
        "name": name,
        "_class": Shape
    }

Shape = {
    "_classname": "Shape",
    "_parent": Shape2D,
    "_new": shape_new
}
# [/shape]

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
    "_parent": Shape2D,
    "_new": square_new
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
    "_new": circle_new
}



def line_new(name, length):
    return make(Shape, name) | {
        "length": length, 
        "_class": Line
}

Line = {
    "_classname": "Line",
    "_parent": Shape,
    "_new": line_new
}


def cls_type(thing):
    return thing["_class"]["_classname"]


def find(cls, method_name):
    if cls is None:
        raise NotImplementedError("method_name")
    if method_name in cls:
        return cls[method_name]
    return find(cls["_parent"], method_name)

def non_rec_find(cls, method_name):

    while method_name not in cls:
        if (cls["_parent"] == None):
                raise NotImplementedError("method_name")
        cls = cls["_parent"]
    return cls["method_name"]

def call(thing, method_name, *args, **kwargs):
    method = find(thing["_class"], method_name)
    return method(thing, *args, **kwargs)

# [call]
examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", weight = 5)
    print(cls_type(ex))
    print(f"{n}: {d:.2f}")
# [/call]

