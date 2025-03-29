# planet_generator/planet_utils/mesh_tools.py

import math
import numpy as np
import logging

def validate_vertex_distances(
    vertices: np.ndarray,  # shape (n, 3)
    expected_radius: float,
    epsilon: float,
    logger: logging.Logger,
    max_output: int = 5
) -> None:
    """
    Validates that all vertices lie on a sphere of the given radius.

    :param vertices: List of 3D points
    :param expected_radius: Target radius
    :param epsilon: Acceptable distance error
    :param logger: Logger instance
    :param max_output: Max number of individual logs to emit
    """
    off_count = 0
    for i, v in enumerate(vertices):
        dist = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        if abs(dist - expected_radius) > epsilon:
            off_count += 1
            if off_count <= max_output:
                logger.warning(f"Vertex {i} is off-sphere: distance={dist:,.3f} (expected {expected_radius})")
        elif i < max_output:
            logger.debug(f"Vertex {i} lies on sphere: distance={dist:,.3f}")

    if off_count == 0:
        logger.info("All vertices lie within expected distance tolerance.")
    else:
        logger.warning(f"{off_count} vertices were off-sphere (>{epsilon:,.3g} tolerance).")

def summarize_mesh_geometry(
    radius: float,
    areas: np.ndarray,
    logger: logging.Logger
) -> dict[str, float]:
    """
    Logs a summary of the planet's geometry based on face areas and global shape.

    :param radius: Radius of the planet (assumed spherical)
    :param areas: List of per-face areas
    :param logger: Logger instance
    """
    num_faces = len(areas)
    total_area = sum(areas)
    average_area = total_area / num_faces if num_faces > 0 else 0.0
    stddev_area = math.sqrt(sum((a - average_area) ** 2 for a in areas) / num_faces) if num_faces > 0 else 0.0

    circumference = 2 * math.pi * radius
    sphere_area = 4 * math.pi * radius * radius

    # Estimate tile sizes (most tiles are hex-based with 6 triangles)
    avg_hex_area = average_area * 6
    avg_pentagon_area = average_area * 5

    logger.info("--- Planet Geometry Summary ---")
    logger.info(f"Planet radius: {radius:,.2f} km")
    logger.info(f"Planet circumference: {circumference:,.2f} km")
    logger.info(f"Planet surface area (ideal sphere): {sphere_area:,.2f} km²")
    logger.info(f"Calculated mesh surface area: {total_area:,.2f} km²")
    logger.info(f"Average triangle face area: {average_area:,.6f} km²")
    logger.info(f"Face area standard deviation: {stddev_area:,.6f} km²")
    logger.info(f"Approx. standard hex-tile area: {avg_hex_area:,.2f} km²")
    logger.info(f"Approx. 5-triangle pentagon tile area: {avg_pentagon_area:,.2f} km²")
    logger.info("--------------------------------\n")

    return {
        "radius_km": radius,
        "circumference_km": circumference,
        "ideal_sphere_area_km2": sphere_area,
        "mesh_area_km2": total_area,
        "average_face_area_km2": average_area,
        "stddev_face_area_km2": stddev_area,
        "hex_tile_area_km2": avg_hex_area,
        "pent_tile_area_km2": avg_pentagon_area,
        "num_faces": num_faces
    }

def estimate_optimal_subdivision(
    radius_km: float,
    target_hex_area_km2: float = 40000.0,
    min_hex_area_km2: float = 10000.0,
    max_subdivision: int = 16
) -> int:
    """
    Estimate the optimal subdivision level for a given radius that
    produces hex-tile areas close to the target without dropping below minimum.

    This uses an approximation:
      - sphere area: 4πr²
      - num triangles: 20 * 4^subdiv
      - hexes = (triangles - 12) / 6
      - avg hex area ≈ (4πr²) / ((20 * 4^n - 12) / 6)

    :param radius_km: Planet radius in kilometers
    :param target_hex_area_km2: Desired hex-tile area
    :param min_hex_area_km2: Minimum acceptable hex-tile area
    :param max_subdivision: Max allowed subdivision level to consider
    :return: Optimal subdivision level
    """
    best_level = 2
    best_area = 0

    sphere_area = 4 * math.pi * radius_km ** 2

    for subdiv in range(2, max_subdivision + 1):
        num_triangles = 20 * (4 ** subdiv)
        num_hexes = (num_triangles - 12) / 6
        avg_hex_area = sphere_area / num_hexes if num_hexes > 0 else 0

        if avg_hex_area < min_hex_area_km2:
            break  # Too small

        best_level = subdiv
        best_area = avg_hex_area

        if avg_hex_area <= target_hex_area_km2:
            break  # Good enough match

    return best_level
