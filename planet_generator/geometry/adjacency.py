# planet_generator/geometry/adjacency.py

from typing import List, Tuple, Dict, Set
import numpy as np


def build_face_adjacency(faces: np.ndarray) -> Dict[int, Set[int]]:
    """
    Constructs a face adjacency map from a list of triangular faces.

    Each face is connected to 3 neighboring faces that share an edge with it.
    The resulting adjacency map is a dictionary where each key is a face index
    and the value is a set of neighboring face indices.

    :param faces: List of triangle indices (triplets of vertex indices)
    :return: Dictionary mapping face index to a set of adjacent face indices
    """
    edge_map: Dict[Tuple[int, int], List[int]] = {}
    adjacency_map: Dict[int, Set[int]] = {i: set() for i in range(len(faces))}

    for i, (a, b, c) in enumerate(faces):
        edges = [(a, b), (b, c), (c, a)]
        for v1, v2 in edges:
            v_low, v_high = sorted((v1, v2))
            key: Tuple[int, int] = (v_low, v_high)
            if key not in edge_map:
                edge_map[key] = []
            edge_map[key].append(i)

    for edge, face_list in edge_map.items():
        if len(face_list) == 2:
            f1, f2 = face_list
            adjacency_map[f1].add(f2)
            adjacency_map[f2].add(f1)

    return adjacency_map
