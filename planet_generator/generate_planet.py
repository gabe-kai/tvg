# planet_generator/generate_planet.py

from planet_generator.planet_config import PLANET_CONFIG
from planet_generator.geometry.icosphere import IcosphereGenerator
from planet_generator.geometry.adjacency import build_face_adjacency
from planet_generator.geometry.face_geometry import compute_face_geometry
from planet_generator.planet_utils.mesh_tools import validate_vertex_distances, summarize_mesh_geometry
from planet_generator.planet_mesh import PlanetMesh
from logger.logger import LoggerFactory
import os


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
    v0 = vertices[0]
    logger.debug("Sample vertex: %.3f, %.3f, %.3f" % (float(v0[0]), float(v0[1]), float(v0[2])))
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
    logger.debug("Sample center (face 0): %.3f, %.3f, %.3f" % (float(face_geometry.centers[0][0]), float(face_geometry.centers[0][1]), float(face_geometry.centers[0][2])))
    n0 = face_geometry.normals[0]
    logger.debug("Sample normal (face 0): %.3f, %.3f, %.3f" % (float(n0[0]), float(n0[1]), float(n0[2])))
    logger.debug("Sample area (face 0): %.6f" % float(face_geometry.areas[0]))
    logger.debug("Sample slope (face 0): %.2f°" % float(face_geometry.slopes[0]))
    logger.debug("Sample lat/lon (face 0): %.2f°, %.2f°" % (float(face_geometry.latitudes[0]), float(face_geometry.longitudes[0])))

    logger.info("Planet generation complete.")

    summarize_mesh_geometry(radius, face_geometry.areas, logger)

    # Step 6: Construct PlanetMesh and test save/load
    mesh = PlanetMesh(
        radius=radius,
        vertices=vertices,
        faces=faces,
        face_geometry=face_geometry,
        face_adjacency=adjacency
    )

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(root_dir, "gamedata", "planets", "planet_test.mesh")
    mesh.save(save_path)
    mesh2 = PlanetMesh.load(save_path)
    mesh2.verify_pentagon_vertices()


if __name__ == "__main__":
    main()
