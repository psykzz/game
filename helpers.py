import math

# Helpers
class Vector2(tuple):
    def __new__(typ, x=1.0, y=1.0):
        n = tuple.__new__(typ, (int(x), int(y)))
        n.x = x
        n.y = y
        return n

    def __mul__(self, other):
        return self.__new__(type(self), self.x*other, self.y*other)
    def __imul__(self, other):
        return self.__mul__(other)
    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        return self.__new__(type(self), self.x+other.x, self.y+other.y)
    def __iadd__(self, other):
        return self.__add__(other)
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__new__(type(self), self.x-other.x, self.y-other.y)
    def __isub__(self, other):
        return self.__sub__(other)
    def __rsub__(self, other):
        return self.__sub__(other)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    @staticmethod
    def from_points(P1, P2):
        return Vector2( P2[0] - P1[0], P2[1] - P1[1] )

    @staticmethod
    def from_rect(rect):
        return Vector2(rect.x, rect.y)

    def get_magnitude(self):
        return math.sqrt( self.x**2 + self.y**2 )

    def normalize(self):
        magnitude = self.get_magnitude()
        if magnitude == 0:
            return
        self.x /= magnitude
        self.y /= magnitude

    def interpolate(self, other, multi=1):
        return multi * other + (1 - multi) * self

    def update(self, x, y):
        self.x = x
        self.y = y
