# planet_generator/planet_mesh.py

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class FaceGeometry:
    centers: List[Tuple[float, float, float]]
    normals: List[Tuple[float, float, float]]
    areas: List[float]
    latitudes: List[float]
    longitudes: List[float]
    slopes: List[float]


from logger.logger import LoggerFactory

class PlanetMesh:
    """
    Stores all planetary mesh data and provides access to geometry, topology, and spatial queries.
    """
    def __init__(
        self,
        radius: float,
        vertices: List[Tuple[float, float, float]],
        faces: List[Tuple[int, int, int]],
        face_geometry: FaceGeometry,
        face_adjacency: Dict[int, List[int]]
    ):
        self.radius = radius
        self.vertices = vertices
        self.faces = faces
        self.geometry = face_geometry
        self.adjacency = face_adjacency

        # Initialize shared logger instance
        self.logger = LoggerFactory("PlanetMesh").get_logger()

        # Optional cache: vertex-to-face map for spatial queries
        self._vertex_to_faces: Optional[Dict[int, List[int]]] = None

    def get_face_ring(self, center_index: int) -> List[int]:
        """
        Returns the 7-tile hex group centered on a given face index.
        Includes the center face and its 6 neighbors.
        """
        ring = [center_index] + list(self.adjacency.get(center_index, []))
        return ring[:7]  # safeguard in case neighbors < 6

    @staticmethod
    def get_pentagon_vertices() -> List[int]:
        """
        Returns the 12 vertex indices (0–11) that form the original icosahedron caps.
        These are the only vertices with 5 surrounding triangle faces.
        """
        return list(range(12))

    def build_vertex_face_map(self) -> Dict[int, List[int]]:
        """
        Constructs a mapping from vertex index to list of face indices sharing that vertex.
        This is useful for locating pentagon face groups and enabling vertex-based queries.
        """
        vertex_to_faces: Dict[int, List[int]] = {}
        for face_index, (v1, v2, v3) in enumerate(self.faces):
            for v in (v1, v2, v3):
                if v not in vertex_to_faces:
                    vertex_to_faces[v] = []
                vertex_to_faces[v].append(face_index)
        return vertex_to_faces

    def get_faces_sharing_vertex(self, vertex_index: int) -> List[int]:
        """
        Returns the list of face indices that include the given vertex.
        Requires calling build_vertex_face_map() first.
        """
        if not hasattr(self, "_vertex_to_faces"):
            self._vertex_to_faces = self.build_vertex_face_map()
        return self._vertex_to_faces.get(vertex_index, [])

    def verify_pentagon_vertices(self) -> bool:
        """
        Verifies that the 12 base icosahedron vertices are only part of 5 triangle faces each.
        Logs warnings for any that deviate from expected structure.
        """
        if self._vertex_to_faces is None:
            self._vertex_to_faces = self.build_vertex_face_map()

        valid = True
        for v in range(12):
            face_count = len(self._vertex_to_faces.get(v, []))
            if face_count != 5:
                self.logger.warning(f"Vertex {v} is part of {face_count} faces, expected 5.")
                valid = False
        return valid

    def save(self, filepath: str) -> None:
        """
        Saves the mesh object to a binary file using pickle.
        Automatically creates the parent directory if it doesn't exist.
        """
        import os
        import pickle
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
        self.logger.info(f"PlanetMesh saved to {filepath}")

    @staticmethod
    def load(filepath: str) -> "PlanetMesh":
        """
        Loads a mesh object from a binary file using pickle.
        """
        import pickle
        with open(filepath, "rb") as f:
            mesh = pickle.load(f)
        mesh.logger.info(f"PlanetMesh loaded from {filepath}")
        return mesh

    # TODO: Add lat/lon spatial queries
    # TODO: Add vertex-to-face index mapping for expansion
