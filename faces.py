# | Level | Count | Possible Polytope       | Center Coordinates   | Notes                      |
# |-------|-------|-------------------------|----------------------|----------------------------|
# | 1     | 17337 | Dimyriagon   20k        | ???                  | Approximate 20000 faces    |
# | 2     | 17225 | Dimyriagon   20k        | (x1, y1, z1)         | 20000 faces                |
# | 3     | 13570 | Dimyriagon   20k        | (x5, y5, z5)         | Approximate 20000 faces    |
# | 4     | 8266  | Enneakischiliagon  9k   | (x5, y5, z5)         | Approximate 9000 faces     |
# | 5     | 3600  | 3600-gon                | (x5, y5, z5)         | 3600 faces                 |
# | 6     | 562   | Hexahectagon (600-gon)  | (x2, y2, z2)         | Words from level 2         |
# | 7     | 31    | Truncated Icosidodecahedron | (x1', y1', z1')  | 62 faces                   |

# Please replace "(x1, y1, z1)", "(x5, y5, z5)", "(x2, y2, z2)", and "(x1', y1', z1')" with the actual coordinates for the centers of the respective polytopes.

from fractions import Fraction

# Define prime numbers
primes = [2, 3, 5, 7, 11, 13, 17]  # You can add more primes as needed

# Quantize coordinates by finding nearest rational multiple of primes
quantized_vertices = np.zeros_like(vertices)
for i, vertex in enumerate(vertices):
    quantized_vertex = [Fraction(coordinate).limit_denominator(prime) for coordinate, prime in zip(vertex, primes)]
    quantized_vertices[i] = quantized_vertex

# ... (continue with the rest of the code)

# Plot the vertices and faces using quantized coordinates
for face in faces:
    poly_vertices = quantized_vertices[face]
    poly = Polyhedron(vertices=poly_vertices)
    poly.plot(ax)
