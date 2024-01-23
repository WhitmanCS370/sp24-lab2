import math

_log = True

# [shapeD]
def shape_new(name):
    Shape["count"] += 1
    return {
        "name": name,
        "_class": Shape
    }

Shape = {
    "_classname": "Shape",
    "_parent": None,
    "_new": shape_new,
    "count" : 0
}
# [/shape]

def line_new(name, length):
    return {
        "name": name,
        "length": length,
        "_class": Line
    }

Line = {
    "_classname": "Line",
    "_parent": Shape,
    "_new": line_new    
}

def shape2D_density(thing, weight):
    return weight / call(thing, "area")

# [shape2D]
def shape2D_new(name):
    return shape_new(name) | {
        "_class": Shape2D
    }

Shape2D = {
    "density": shape2D_density,
    "_classname": "Shape2D",
    "_parent": Shape,
    "_new": shape2D_new
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

_method_cache = {}
def find(cls, method_name):
    global _method_cache
    key = (cls["_classname"], method_name)
    if key in _method_cache:
        if _log: print(f"Calling cached method {key}")
        return _method_cache[key]
    while cls is not None:
        if method_name in cls:
            if _log: print(f"Caching method {key}")
            method = cls[method_name]
            _method_cache[key] = method
            return method
        cls = cls["_parent"]
    raise NotImplementedError("method_name")

def call(thing, method_name, *args, **kwargs):
    method = find(thing["_class"], method_name)
    return method(thing, *args, **kwargs)

def type(thing):
    return thing["_class"]["_classname"]

def isinstance(thing, targetclass):
    currentclass = thing["_class"]
    while currentclass != targetclass:
        if currentclass["_parent"] is None:
            return False
        currentclass = currentclass["_parent"]
    return True

# [call]
examples = [make(Square, "sq", 3), 
            make(Circle, "ci", 2), 
            make(Line, "li", 5)]
for ex in examples:
    n = ex["name"]
    b = isinstance(ex, Shape2D)
    print(f"{n}: {b}")
examples = [make(Square, "sq", 3), 
            make(Circle, "ci", 2), 
            make(Square, "sq", 5), 
            make(Circle, "ci", 5)]
for ex in examples:
    n = ex["name"]
    p = call(ex, "perimeter")
    a = call(ex, "area")
    print(f"{n}: perimeter:{p} area:{a}")
    
print("Total shapes:", Shape["count"])
# [/call]
