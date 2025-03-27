# planet_generator/geometry/icosphere.py

import math
from typing import List, Tuple


class IcosphereGenerator:
    """
    Generates a subdivided icosahedron (icosphere) projected onto a sphere.
    Useful for building a planetary mesh with uniform triangle distribution.
    """

    def __init__(self, radius: float, subdivisions: int):
        """
        :param radius: Radius of the resulting sphere.
        :param subdivisions: Number of recursive triangle subdivisions.
        """
        self.radius = radius
        self.subdivisions = subdivisions
        self.vertices: List[Tuple[float, float, float]] = []
        self.faces: List[Tuple[int, int, int]] = []

    def generate(self) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int, int]]]:
        """
        Builds the icosphere and returns the final vertices and faces.
        :return: A tuple of (vertices, faces)
        """
        self._create_icosahedron()
        for _ in range(self.subdivisions):
            self._subdivide()
        self._normalize_vertices()
        return self.vertices, self.faces

    def _create_icosahedron(self):
        """
        Creates the initial 12 vertices and 20 triangular faces of an icosahedron.
        """
        self.vertices.clear()
        self.faces.clear()

        # Golden ratio
        phi = (1 + math.sqrt(5)) / 2

        # Create vertices
        points = [
            (-1,  phi,  0), (1,  phi,  0), (-1, -phi,  0), (1, -phi,  0),
            (0, -1,  phi), (0,  1,  phi), (0, -1, -phi), (0,  1, -phi),
            (phi,  0, -1), (phi,  0,  1), (-phi,  0, -1), (-phi,  0,  1),
        ]
        self.vertices = [self._normalize(v) for v in points]

        # Define 20 triangular faces
        self.faces = [
            (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
            (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
            (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
            (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
        ]

    def _subdivide(self):
        """
        Subdivides each triangular face into 4 smaller triangles.
        """
        midpoint_cache = {}
        new_faces = []

        def midpoint(idx1: int, idx2: int) -> int:
            key = tuple(sorted((idx1, idx2)))
            if key not in midpoint_cache:
                vert1 = self.vertices[idx1]
                vert2 = self.vertices[idx2]
                x = (vert1[0] + vert2[0]) / 2
                y = (vert1[1] + vert2[1]) / 2
                z = (vert1[2] + vert2[2]) / 2
                mid = (x, y, z)
                self.vertices.append(self._normalize(mid))
                midpoint_cache[key] = len(self.vertices) - 1
            return midpoint_cache[key]

        for tri in self.faces:
            i1, i2, i3 = tri
            a = midpoint(i1, i2)
            b = midpoint(i2, i3)
            c = midpoint(i3, i1)
            new_faces.extend([
                (i1, a, c),
                (i2, b, a),
                (i3, c, b),
                (a, b, c),
            ])

        self.faces = new_faces

    def _normalize(self, v: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """
        Normalizes a 3D vector to lie on the sphere with the specified radius.
        """
        x, y, z = v
        length = math.sqrt(x * x + y * y + z * z)
        return (x / length * self.radius, y / length * self.radius, z / length * self.radius)

    def _normalize_vertices(self):
        """
        Re-normalizes all vertices to correct for numerical drift after subdivision.
        """
        self.vertices = [self._normalize(v) for v in self.vertices]
