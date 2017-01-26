from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prex = 30


class Vector(object):
    def __init__(self, coordinates):
        CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'

        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        result = []

        for i in xrange( max(self.dimension, v.dimension) ):
            result.append(self.coordinates[i] + v.coordinates[i])

        return Vector(result)

    def minus(self, v):
        result = [x + y for x, y in zip(self.coordinates, v.coordinates)]

        return Vector(result)

    def times_scalar(self, c):
        result = [Decimal(c) * x for x in self.coordinates]

        return Vector(result)

    def magnitude(self):
        square_sum = sum([x**2 for x in self.coordinates])

        return sqrt(square_sum)

    def normalized(self):
        try:
            magnitude = self.magnitude()

            return self.times_scalar(1./magnitude)

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        result = [x * y for x, y in zip(self.coordinates, v.coordinates)]

        return sum(result)

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = acos( u1.dot(u2) )

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e
