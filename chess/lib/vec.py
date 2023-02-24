# Vector implementation

def is_num_type(a):
    a_type = type(a)
    return a_type == int or a_type == float 

def is_vec_num_type(a):
    return is_num_type(a) or type(a) == vec

def is_vec_type(a):
    return type(a) == vec

def is_tuple_type(a):
    return type(a) == tuple

class NotNumericTypeError(TypeError):
    def __init__(self, value = None):
        self.value = value

    def __str__(self):
        got =  f". Got  {self.value}." if self.value is not None else ""
        return f"Type is not a numeric type (int or float)" + got

class NotNumericVecTypeError(TypeError):
    def __init__(self, value = None):
        self.value = value

    def __str__(self):
        got =  f". Got  {self.value}." if self.value is not None else ""
        return f"Type is not a numeric or vec type" + got

class vec:
    def __init__(self, x, y = None) -> None:
        if type(x) == vec:
            self.x = x.x
            self.y = x.y
            return 
        elif not (is_num_type(x) and is_num_type(y)):
            raise NotNumericTypeError
        if y is None:
            y = x
        self.x = x
        self.y = y
    
    def __add__(self, vec2):
        if is_num_type(vec2):
            x = self.x + vec2
            y = self.y + vec2
        
        elif is_vec_type(vec2):
            x = self.x + vec2.x
            y = self.y + vec2.y
        elif is_tuple_type(vec2):
            x = self.x + vec2[0]
            y = self.y + vec2[1]
        else:
            raise NotNumericVecTypeError

        return vec(x, y)

    def __iadd__(self, vec2):
        if is_num_type(vec2):
            self.x += vec2
            self.y += vec2
        
        elif is_vec_type(vec2):
            self.x += vec2.x
            self.y += vec2.y
        elif is_tuple_type(vec2):
            self.x += vec2[0]
            self.y += vec2[1]
        else:
            raise NotNumericVecTypeError

        return self

    def __sub__(self, vec2):
        if is_num_type(vec2):
            x = self.x - vec2
            y = self.y - vec2
        
        elif is_vec_type(vec2):
            x = self.x - vec2.x
            y = self.y - vec2.y
        elif is_tuple_type(vec2):
            x = self.x - vec2[0]
            y = self.y - vec2[1]
        else:
            raise NotNumericVecTypeError

        return vec(x, y)
    
    def __isub__(self, vec2):
        if is_num_type(vec2):
            self.x -= vec2
            self.y -= vec2
        
        elif is_vec_type(vec2):
            self.x -= vec2.x
            self.y -= vec2.y
        elif is_tuple_type(vec2):
            self.x -= vec2[0]
            self.y -= vec2[1]
        else:
            raise NotNumericVecTypeError

        return self

    def __mul__(self, vec2):
        if is_num_type(vec2):
            x = self.x * vec2
            y = self.y * vec2
        
        elif is_vec_type(vec2):
            x = self.x * vec2.x
            y = self.y * vec2.y
        elif is_tuple_type(vec2):
            x = self.x * vec2[0]
            y = self.y * vec2[1]
        else:
            raise NotNumericVecTypeError

        return vec(x, y)

    def __imul__(self, vec2):
        if is_num_type(vec2):
            self.x *= vec2
            self.y *= vec2
        
        elif is_vec_type(vec2):
            self.x *= vec2.x
            self.y *= vec2.y
        elif is_tuple_type(vec2):
            self.x *= vec2[0]
            self.y *= vec2[1]
        else:
            raise NotNumericVecTypeError

        return self

    def __truediv__(self, vec2):
        if is_num_type(vec2):
            x = self.x / vec2
            y = self.y / vec2
        
        elif is_vec_type(vec2):
            x = self.x / vec2.x
            y = self.y / vec2.y
        elif is_tuple_type(vec2):
            x = self.x / vec2[0]
            y = self.y / vec2[1]
        else:
            raise NotNumericVecTypeError

        return vec(x, y)

    def __idiv__(self, vec2):
        if is_num_type(vec2):
            self.x /= vec2
            self.y /= vec2
        
        elif is_vec_type(vec2):
            self.x /= vec2.x
            self.y /= vec2.y
        elif is_tuple_type(vec2):
            self.x /= vec2[0]
            self.y /= vec2[1]
        else:
            raise NotNumericVecTypeError

        return self

    def __floordiv__(self, vec2):
        if is_num_type(vec2):
            x = self.x // vec2
            y = self.y // vec2
        
        elif is_vec_type(vec2):
            x = self.x // vec2.x
            y = self.y // vec2.y
        elif is_tuple_type(vec2):
            x = self.x // vec2[0]
            y = self.y // vec2[1]
        else:
            raise NotNumericVecTypeError
        return vec(x, y)
        
    def __ifloordiv__(self, vec2):
        if is_num_type(vec2):
            self.x //= vec2
            self.y //= vec2
        
        elif is_vec_type(vec2):
            self.x //= vec2.x
            self.y //= vec2.y
        elif is_tuple_type(vec2):
            self.x //= vec2[0]
            self.y //= vec2[1]
        else:
            raise NotNumericVecTypeError

        return self

    def __eq__(self, other: 'vec') -> bool:
        if not (hasattr(other, 'x') or hasattr(other, 'y')):
            return False
        return self.x == other.x and self.y == other.y 

    def __ne__(self, other: 'vec') -> bool:
        return not self.__eq__(other)

    


    def __repr__(self) -> str:
        return f"vec({self.x}, {self.y})"

    def __getitem__(self, p):
        if p == 0:
            return self.x
        elif p == 1:
            return self.y
        elif type(p) == int:
            raise IndexError("Index out of range (0, 1)")
        raise TypeError('Unsupported type')

    def __tuple__(self) -> tuple:
        return (self.x, self.y)

    def __float__(self):
        return (self.x**2 + self.y**2) ** .5


    def __iter__(self) -> list:
        return iter([self.x, self.y])

    def __next__(self):
        pass

    def copy(self):
        return vec(self)