# /planet_generator/exporters/export_planet.py

import os
import argparse
import joblib
from logger.logger import LoggerFactory


class PlanetExporter:
    """
    Exports a PlanetMesh object to supported 3D formats (.obj).

    Attributes:
        mesh: A PlanetMesh-like object containing vertices and faces as numpy arrays.
        export_dir: The directory where output files will be saved.
        logger: Logger instance for tracking export process.
    """

    def __init__(self, mesh, export_dir: str = "gamedata/exports"):
        self.mesh = mesh
        self.export_dir = export_dir
        self.logger = LoggerFactory("PlanetExporter").get_logger()
        os.makedirs(export_dir, exist_ok=True)  # Ensure the directory exists

    def export_obj(self, filename: str, include_normals: bool = False):
        """
        Exports the mesh as a Wavefront .OBJ file.

        Args:
            filename: The name of the file to export (e.g., "planet.obj").
            include_normals: Whether to include per-face normals.
        """
        filepath = os.path.join(self.export_dir, filename)
        self.logger.info(f"Beginning OBJ export to {filepath} (normals={'on' if include_normals else 'off'})")

        with open(filepath, 'w') as obj_file:
            obj_file.write("# Exported Planet Mesh\n")

            # Write vertices
            for v in self.mesh.vertices:
                obj_file.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")

            # Optionally write normals
            if include_normals:
                for n in self.mesh.geometry.normals:
                    obj_file.write(f"vn {n[0]:.6f} {n[1]:.6f} {n[2]:.6f}\n")

            # Write faces (1-based indexing for OBJ)
            for idx, f in enumerate(self.mesh.faces):
                v1, v2, v3 = f.astype(int)
                if include_normals:
                    # Add normal index to each vertex
                    obj_file.write(f"f {v1+1}//{idx+1} {v2+1}//{idx+1} {v3+1}//{idx+1}\n")
                else:
                    obj_file.write(f"f {v1+1} {v2+1} {v3+1}\n")

        self.logger.info(f"OBJ export complete: {filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export a PlanetMesh to .OBJ format")
    parser.add_argument("input_mesh", type=str, help="Path to the saved planet mesh file (.mesh)")
    parser.add_argument("--output", type=str, default="planet.obj", help="Name of the output .obj file")
    parser.add_argument("--normals", action="store_true", help="Include per-face normals in the export")
    args = parser.parse_args()

    # Load mesh from file using joblib
    mesh = joblib.load(args.input_mesh)

    # Export to OBJ
    exporter = PlanetExporter(mesh)
    exporter.export_obj(args.output, include_normals=args.normals)
