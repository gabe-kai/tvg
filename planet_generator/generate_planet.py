# planet_generator/generate_planet.py

from planet_generator.planet_config import PLANET_CONFIG
from planet_generator.geometry.icosphere import IcosphereGenerator
from planet_generator.geometry.adjacency import build_face_adjacency
from planet_generator.geometry.face_geometry import compute_face_geometry
from planet_generator.planet_utils.mesh_tools import validate_vertex_distances, summarize_mesh_geometry
from logger.logger import LoggerFactory


def main():
    """
    Entry point for procedural planet generation.
    Initializes config, logger, and starts mesh generation with debug info.
    """
    logger = LoggerFactory("PlanetGen").get_logger()
    logger.info("Starting planet generation...")

    # Step 1: Load config values
    radius = PLANET_CONFIG.get("planet_radius")
    subdivisions = PLANET_CONFIG.get("subdivisions")

    logger.info(f"Planet radius: {radius:,} km")
    logger.info(f"Icosphere subdivisions: {subdivisions:,}")

    # Step 2: Generate mesh
    generator = IcosphereGenerator(radius, subdivisions)
    vertices, faces = generator.generate()

    logger.info(f"Mesh generated with {len(vertices):,} vertices and {len(faces):,} faces.")
    logger.debug("Sample vertex: %.3f, %.3f, %.3f" % vertices[0])
    logger.debug("Sample face: %s" % str(faces[0]))

    # Step 3: Validate distances
    epsilon = 1e-3
    validate_vertex_distances(vertices, radius, epsilon, logger)

    # Step 4: Build face adjacency map
    adjacency = build_face_adjacency(faces)
    logger.info(f"Adjacency map built for {len(adjacency):,} faces.")
    logger.debug(f"Sample adjacency (face 0): {sorted(adjacency[0])}")

    # Step 5: Compute face geometry
    face_geometry = compute_face_geometry(vertices, faces)
    logger.info("Computed face centers, normals, areas, slopes, and coordinates.")
    logger.debug("Sample center (face 0): %.3f, %.3f, %.3f" % face_geometry.centers[0])
    logger.debug("Sample normal (face 0): %.3f, %.3f, %.3f" % face_geometry.normals[0])
    logger.debug("Sample area (face 0): %.6f" % face_geometry.areas[0])
    logger.debug("Sample slope (face 0): %.2f°" % face_geometry.slopes[0])
    logger.debug("Sample lat/lon (face 0): %.2f°, %.2f°" % (face_geometry.latitudes[0], face_geometry.longitudes[0]))

    logger.info("Planet generation complete.")

    summarize_mesh_geometry(radius, face_geometry.areas, logger)


if __name__ == "__main__":
    main()
