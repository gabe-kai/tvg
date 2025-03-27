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
) -> None:
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
