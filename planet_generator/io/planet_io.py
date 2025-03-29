import os
import json
import joblib
import numpy as np
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from planet_generator.planet_mesh import PlanetMesh
from logger.logger import LoggerFactory

logger = LoggerFactory("PlanetIO").get_logger()


@dataclass
class Planet:
    """
    Wrapper class for a full planet, including geometry, simulation layers, and metadata.
    """
    name: str
    seed: int
    mesh: PlanetMesh
    elevation: Optional[np.ndarray] = None        # shape: (n_faces,)
    cratons: Optional[np.ndarray] = None          # shape: (n_faces,) - int plate IDs
    biome_tags: Optional[List[str]] = None        # list of biome tags per face or index map
    generation_time: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    version: str = "1.0"


class PlanetIO:
    """
    Handles saving and loading Planet objects using modular file-based layout.
    """

    @staticmethod
    def save(planet: Planet, folder_path: str) -> None:
        os.makedirs(folder_path, exist_ok=True)

        # Save mesh using joblib with higher compression
        mesh_path = os.path.join(folder_path, "mesh.joblib")
        joblib.dump(planet.mesh, mesh_path, compress=("lzma", 9))
        logger.info(f"Saved mesh to {mesh_path}")

        # Save elevation
        if planet.elevation is not None:
            elevation_path = os.path.join(folder_path, "elevation.npy")
            np.save(elevation_path, planet.elevation)
            logger.info(f"Saved elevation to {elevation_path}")
        else:
            logger.info("No elevation data to save.")

        # Save craton map
        if planet.cratons is not None:
            cratons_path = os.path.join(folder_path, "cratons.npy")
            np.save(cratons_path, planet.cratons)
            logger.info(f"Saved craton map to {cratons_path}")
        else:
            logger.info("No craton map to save.")

        # Save biome tags (as JSON string list)
        if planet.biome_tags is not None:
            biomes_path = os.path.join(folder_path, "biomes.json")
            with open(biomes_path, "w", encoding="utf-8") as f:
                json.dump(planet.biome_tags, f, indent=2)
            logger.info(f"Saved biome tags to {biomes_path}")
        else:
            logger.info("No biome tags to save.")

        # Save metadata
        metadata = {
            "name": planet.name,
            "seed": planet.seed,
            "generation_time": planet.generation_time,
            "version": planet.version,
        }
        metadata_path = os.path.join(folder_path, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Saved metadata to {metadata_path}")

        logger.info(f"Planet save complete: {folder_path}")

    @staticmethod
    def load(folder_path: str) -> Planet:
        # Load mesh
        mesh_path = os.path.join(folder_path, "mesh.joblib")
        mesh = joblib.load(mesh_path)
        logger.info(f"Loaded mesh from {mesh_path}")

        # Load metadata
        metadata_path = os.path.join(folder_path, "metadata.json")
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        logger.info(f"Loaded metadata from {metadata_path}")

        # Optional layers
        elevation_path = os.path.join(folder_path, "elevation.npy")
        elevation = np.load(elevation_path) if os.path.exists(elevation_path) else None
        if elevation is not None:
            logger.info(f"Loaded elevation from {elevation_path}")
        else:
            logger.info("No elevation data found.")

        cratons_path = os.path.join(folder_path, "cratons.npy")
        cratons = np.load(cratons_path) if os.path.exists(cratons_path) else None
        if cratons is not None:
            logger.info(f"Loaded craton map from {cratons_path}")
        else:
            logger.info("No craton map found.")

        biomes_path = os.path.join(folder_path, "biomes.json")
        if os.path.exists(biomes_path):
            with open(biomes_path, "r", encoding="utf-8") as f:
                biomes = json.load(f)
            logger.info(f"Loaded biome tags from {biomes_path}")
        else:
            biomes = None
            logger.info("No biome tags found.")

        logger.info(f"Planet load complete: {folder_path}")

        return Planet(
            name=metadata["name"],
            seed=metadata["seed"],
            generation_time=metadata["generation_time"],
            version=metadata.get("version", "1.0"),
            mesh=mesh,
            elevation=elevation,
            cratons=cratons,
            biome_tags=biomes,
        )
