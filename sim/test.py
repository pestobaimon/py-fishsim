import math

from vector_math import Vector

vect = Vector(150,0);

vect = vect.rotate(math.pi*0.5, True)

print(vect.get_tuple())