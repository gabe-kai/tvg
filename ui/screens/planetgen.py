# /ui/screens/planetgen.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QSize, QEvent
from logger.logger import LoggerFactory
from planet_generator.planet_utils.mesh_tools import estimate_optimal_subdivision, summarize_mesh_geometry
from ui.widgets.planetgen_control_panel import PlanetGenControlPanel
from ui.widgets.planetgen_geometry_panel import PlanetGenGeometryPanel
from ui.widgets.planet_preview_widget import PlanetPreviewWidget
from ui.widgets.planetgen_view_controls import PlanetGenViewControls

logger = LoggerFactory("planetgen_screen").get_logger()


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

        title = QLabel("Planet Generator")
        title.setObjectName("Header1")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
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

        self.planet_preview = PlanetPreviewWidget("gamedata/planets/planet_test.mesh")
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

        # Connect signals
        self.control_panel.inputs_changed.connect(self.update_geometry_summary)
        self.control_panel.mesh_generated.connect(self.planet_preview.reload_mesh)
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
