# /ui/screens/planetgen.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, QEvent
from logger.logger import LoggerFactory
from planet_generator.planet_utils.mesh_tools import estimate_optimal_subdivision, summarize_mesh_geometry
from ui.widgets.planetgen_control_panel import PlanetGenControlPanel
from ui.widgets.planetgen_geometry_panel import PlanetGenGeometryPanel
from ui.theme import DARK_THEME

logger = LoggerFactory("planetgen_screen").get_logger()


class PlanetGenScreen(QWidget):
    """
    A screen for customizing and previewing planet generation.
    Includes a header, footer (log), left-side preview area, and right-side controls.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(DARK_THEME)  # Apply global dark theme
        self.setup_ui()
        self.update_geometry_summary()
        logger.info("PlanetGenScreen initialized")

    def setup_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Header ---
        header = QLabel("Planet Generator")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("background-color: #333333; color: white; border: 1px solid #555; padding: 8px;")
        header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(header)

        # --- Central Horizontal Layout ---
        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        # Left Panel (Planet Preview)
        self.left_panel = QWidget()
        self.left_panel.setObjectName("ContentPanel")
        self.left_panel.setStyleSheet("border: 1px solid #666;")
        self.left_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Use absolute positioning inside left_panel
        self.planet_preview_label = QLabel("[ Planet Preview Area ]", self.left_panel)
        self.planet_preview_label.setAlignment(Qt.AlignCenter)
        self.planet_preview_label.setGeometry(0, 0, 1, 1)  # Will stretch by size policy
        self.planet_preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.summary_panel = PlanetGenGeometryPanel(self.left_panel)
        self.summary_panel.move(10, 10)  # Top-right can be adjusted later

        center_layout.addWidget(self.left_panel, stretch=3)

        # Right Panel (Inputs and Controls)
        self.right_panel = PlanetGenControlPanel(self)
        self.right_panel.setObjectName("ContextPanel")
        self.right_panel.setStyleSheet("border: 1px solid #666;")
        self.right_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        center_layout.addWidget(self.right_panel, stretch=1)

        main_layout.addLayout(center_layout)

        # --- Footer (Log Viewer Placeholder) ---
        self.footer = QLabel("[ Log Viewer Placeholder ]")
        self.footer.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.footer.setStyleSheet("border: 1px solid #444; background-color: #1a1a1a; color: #aaa; padding: 4px;")
        self.footer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(self.footer)

        # Connect control panel input signal
        self.right_panel.inputs_changed.connect(self.update_geometry_summary)
        self.update_geometry_summary()  # Initial fill

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_geometry_summary()

    def update_geometry_summary(self):
        """Update the geometry summary panel based on current radius and subdivision inputs."""
        radius = self.right_panel.radius_input.value()
        subdivisions = self.right_panel.subdiv_input.value()

        # Use approximation to estimate face count and hex area
        optimal_level = estimate_optimal_subdivision(radius)

        # Estimate face count and area assuming 20 * 4^n faces
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

        """Repositions the floating summary panel to the top-right corner of the left panel."""
        if hasattr(self, 'left_panel') and hasattr(self, 'summary_panel'):
            margin = 10
            panel_width = self.summary_panel.width()
            x = self.left_panel.width() - panel_width - margin
            y = margin
            self.summary_panel.move(x, y)
