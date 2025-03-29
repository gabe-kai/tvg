# /ui/screens/planetgen.py

import os
import json
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt
from logger.logger import LoggerFactory
from planet_generator.planet_utils.mesh_tools import estimate_optimal_subdivision, summarize_mesh_geometry
from ui.widgets.planetgen_control_panel import PlanetGenControlPanel
from ui.widgets.planetgen_geometry_panel import PlanetGenGeometryPanel
from ui.widgets.planet_preview_widget import PlanetPreviewWidget
from ui.widgets.planetgen_view_controls import PlanetGenViewControls

logger = LoggerFactory("planetgen_screen").get_logger()


def find_most_recent_planet_folder():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "gamedata", "planets")
    if not os.path.exists(base_dir):
        return None
    subdirs = [
        os.path.join(base_dir, name) for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name))
    ]
    subdirs = sorted(subdirs, key=lambda d: os.path.getmtime(os.path.join(d, "metadata.json")) if os.path.exists(os.path.join(d, "metadata.json")) else 0, reverse=True)
    return subdirs[0] if subdirs else None


def load_most_recent_metadata(folder):
    try:
        with open(os.path.join(folder, "metadata.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Could not load metadata from {folder}: {e}")
        return None


class PlanetGenScreen(QWidget):
    """
    A screen for customizing and previewing planet generation.
    Includes a header, footer (log), left-side preview area, and right-side controls.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.update_geometry_summary()
        logger.info("PlanetGenScreen initialized")

    def setup_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Header Container ---
        self.header_container = QWidget()
        self.header_container.setObjectName("HeaderPanel")
        self.header_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        header_layout = QVBoxLayout(self.header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel("Planet Preview:")
        self.title_label.setObjectName("Header1")
        self.title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.title_label)
        main_layout.addWidget(self.header_container)

        # --- Central Horizontal Layout ---
        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        # --- Left Content Panel ---
        self.left_panel_container = QWidget()
        self.left_panel_container.setObjectName("ContentPanel")
        self.left_panel_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_panel_container.setAttribute(Qt.WA_StyledBackground, True)
        layout = QVBoxLayout(self.left_panel_container)
        layout.setContentsMargins(0, 0, 0, 0)

        recent_folder = find_most_recent_planet_folder()
        mesh_path = os.path.join(recent_folder, "mesh.joblib") if recent_folder else ""
        self.planet_preview = PlanetPreviewWidget(mesh_path)
        layout.addWidget(self.planet_preview)
        self.planet_preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Floating overlay panel inside left panel
        self.floating_panel = QFrame(self.left_panel_container)
        self.floating_panel.setObjectName("FloatingPanel")
        float_layout = QVBoxLayout(self.floating_panel)
        float_layout.setContentsMargins(6, 6, 6, 6)
        float_layout.setSpacing(8)

        self.summary_panel = PlanetGenGeometryPanel(self.floating_panel)
        self.view_controls = PlanetGenViewControls(self.floating_panel, self.planet_preview)

        float_layout.addWidget(self.summary_panel)
        float_layout.addWidget(self.view_controls)

        self.floating_panel.adjustSize()
        center_layout.addWidget(self.left_panel_container, stretch=3)

        # --- Right Panel ---
        self.right_panel_container = QWidget()
        self.right_panel_container.setObjectName("RightPanel")
        self.right_panel_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.right_panel_container.setAttribute(Qt.WA_StyledBackground, True)

        right_layout = QVBoxLayout(self.right_panel_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.control_panel = PlanetGenControlPanel(self)
        right_layout.addWidget(self.control_panel)

        center_layout.addWidget(self.right_panel_container, stretch=1)
        main_layout.addLayout(center_layout)

        # --- Footer Container ---
        self.footer_container = QWidget()
        self.footer_container.setObjectName("FooterPanel")
        self.footer_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        footer_layout = QVBoxLayout(self.footer_container)
        footer_layout.setContentsMargins(0, 0, 0, 0)

        self.footer = QLabel("[ Log Viewer Placeholder ]")
        self.footer.setObjectName("LogViewer")
        self.footer.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.footer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        footer_layout.addWidget(self.footer)
        main_layout.addWidget(self.footer_container)

        # Prefill control panel if recent planet metadata exists
        if recent_folder:
            metadata = load_most_recent_metadata(recent_folder)
            if metadata:
                planet_name = metadata.get("name")
                planet_seed = metadata.get("seed")
                if planet_name:
                    self.title_label.setText(f"Planet Preview: {planet_name}")
                    self.control_panel.name_input.setText(planet_name)
                if planet_seed is not None:
                    self.control_panel.seed_input.setValue(int(planet_seed))
                planet_radius = metadata.get("radius")
                subdivisions = metadata.get("subdivisions")
                if planet_radius is not None:
                    self.control_panel.radius_input.setValue(float(planet_radius))
                if subdivisions is not None:
                    self.control_panel.subdiv_input.setValue(int(subdivisions))

        # Connect signals
        self.control_panel.inputs_changed.connect(self.update_geometry_summary)
        self.control_panel.mesh_generated.connect(self.handle_mesh_generated)
        self.update_geometry_summary()  # Initial fill

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_geometry_summary()

    def update_geometry_summary(self):
        """Update the geometry summary panel based on current radius and subdivision inputs."""
        radius = self.control_panel.radius_input.value()
        subdivisions = self.control_panel.subdiv_input.value()

        optimal_level = estimate_optimal_subdivision(radius)
        num_faces = 20 * (4 ** subdivisions)
        triangle_area = (4 * 3.1415926535 * radius ** 2) / num_faces
        mesh_area = triangle_area * num_faces
        avg_hex_area = triangle_area * 6
        avg_pent_area = triangle_area * 5

        summary_data = {
            "radius_km": radius,
            "subdivisions": subdivisions,
            "mesh_area_km2": mesh_area,
            "triangle_face_area_km2": triangle_area,
            "hex_tile_area_km2": avg_hex_area,
            "pent_tile_area_km2": avg_pent_area,
            "estimated_faces": num_faces,
            "suggested_subdiv_level": optimal_level
        }

        self.summary_panel.update_summary(summary_data)

        # Reposition floating summary panel
        if hasattr(self, 'left_panel_container') and hasattr(self, 'floating_panel'):
            margin = 10
            panel_width = self.floating_panel.width()
            x = self.left_panel_container.width() - panel_width - margin
            y = margin
            self.floating_panel.move(x, y)

    def handle_mesh_generated(self):
        """Update header title when mesh is generated."""
        name = self.control_panel.name_input.text()
        self.title_label.setText(f"Planet Preview: {name}")
                # Wait for the new mesh file to appear (max 2 sec)
        planet_name = self.control_panel.name_input.text()
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "gamedata", "planets")
        mesh_path = os.path.join(base_dir, planet_name, "mesh.joblib")

        wait_time = 0
        while not os.path.exists(mesh_path) and wait_time < 2.0:
            time.sleep(0.1)
            wait_time += 0.1

        if os.path.exists(mesh_path):
            self.planet_preview.set_mesh_path(mesh_path)
            self.planet_preview.reload_mesh()
        else:
            logger.warning(f"Mesh file not found after generation: {mesh_path}")
