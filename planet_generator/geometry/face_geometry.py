# planet_generator/geometry/face_geometry.py

import math
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class FaceGeometry:
    centers: List[Tuple[float, float, float]]
    normals: List[Tuple[float, float, float]]
    areas: List[float]
    latitudes: List[float]  # in degrees
    longitudes: List[float]  # in degrees
    slopes: List[float]  # in degrees


def compute_face_geometry(
    vertices: List[Tuple[float, float, float]],
    faces: List[Tuple[int, int, int]]
) -> FaceGeometry:
    """
    Computes the center, normal, area, latitude, longitude, and slope of each triangle face.

    :param vertices: List of 3D vertex coordinates
    :param faces: List of triangle faces (triplets of vertex indices)
    :return: A FaceGeometry dataclass with centers, normals, areas, lat/lon, and slopes
    """
    centers = []
    normals = []
    areas = []
    latitudes = []
    longitudes = []
    slopes = []

    for i1, i2, i3 in faces:
        v1 = vertices[i1]
        v2 = vertices[i2]
        v3 = vertices[i3]

        # Compute center
        cx = (v1[0] + v2[0] + v3[0]) / 3
        cy = (v1[1] + v2[1] + v3[1]) / 3
        cz = (v1[2] + v2[2] + v3[2]) / 3
        centers.append((cx, cy, cz))

        # Compute normal (unit vector)
        edge1 = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
        edge2 = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])
        nx = edge1[1] * edge2[2] - edge1[2] * edge2[1]
        ny = edge1[2] * edge2[0] - edge1[0] * edge2[2]
        nz = edge1[0] * edge2[1] - edge1[1] * edge2[0]

        length = math.sqrt(nx * nx + ny * ny + nz * nz)
        if length == 0:
            normals.append((0.0, 0.0, 0.0))
            areas.append(0.0)
            slopes.append(0.0)
        else:
            normals.append((nx / length, ny / length, nz / length))
            areas.append(0.5 * length)  # triangle area = 0.5 * |cross product|

            # Compute slope in degrees (angle from radial vector from planet center)
            center_len = math.sqrt(cx**2 + cy**2 + cz**2)
            center_unit = (cx / center_len, cy / center_len, cz / center_len)
            normal_unit = (nx / length, ny / length, nz / length)
            dot = sum(center_unit[i] * normal_unit[i] for i in range(3))
            dot = max(-1.0, min(1.0, dot))  # Clamp dot product to valid acos range
            angle_rad = math.acos(dot)
            slope_deg = math.degrees(angle_rad)
            slopes.append(slope_deg)

        # Convert center to latitude and longitude
        r = math.sqrt(cx * cx + cy * cy + cz * cz)
        lat = math.degrees(math.asin(cz / r))
        lon = math.degrees(math.atan2(cy, cx))
        latitudes.append(lat)
        longitudes.append(lon)

    # TODO: Add support for filtering specific face indices for partial updates
    return FaceGeometry(
        centers=centers,
        normals=normals,
        areas=areas,
        latitudes=latitudes,
        longitudes=longitudes,
        slopes=slopes
    )
