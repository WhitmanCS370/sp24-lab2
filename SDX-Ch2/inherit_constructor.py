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
    "_new": shape_new
}

def type(thing):
    return thing["_classname"]

def isinstance(thing): 
    if thing["_parent"]: 
        return True
    return False 

def shape2d_perimeter(thing, length):
    return call(thing, "perimeter")

def shape2d_area(thing, length):
    return call(thing, "area")

def shape2d_new(name):
    return {
        "name": name, 
        "_class" : Shape2D
    }


Shape2D = {
    "perimeter" : shape2d_perimeter,
    "area": shape2d_area, 
    "_parent" : Shape, 
    "_new" : shape2d_new

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

def find(cls, method_name):
    while True:
        if cls is None:
            raise NotImplementedError("method name")
        if method_name in cls:
            return cls[method_name]
        else:
            cls = cls["_parent"]


def call(thing, method_name, *args, **kwargs):
    method = find(thing["_class"], method_name)
    return method(thing, *args, **kwargs)

# [call]
examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")

def line_new(name, length): 
    return make(Shape, name) |{
        "length" : length,
        "_class" : Line
    }

Line = {
    "_classname": "Line",
    "_parent" : Shape, 
    "_new": line_new,
}


# [/call]
