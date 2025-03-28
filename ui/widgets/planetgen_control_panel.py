# /ui/widgets/planetgen_control_panel.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QFormLayout, QDoubleSpinBox, QSpinBox
)
from PySide6.QtCore import Qt
from logger.logger import LoggerFactory
from planet_generator.planet_config import PLANET_CONFIG

logger = LoggerFactory("planetgen_control_panel").get_logger()


class PlanetGenControlPanel(QWidget):
    """
    Widget for controlling planet generation parameters.
    Contains inputs for radius and subdivision level, and buttons
    to generate, export, reset, or go back.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ContextPanel")  # Allow styling via theme
        self.setAttribute(Qt.WA_StyledBackground, True)  # Allow stylesheet background to render

        # Diagnostic logging
        logger.info(f"PlanetGenControlPanel class: {self.metaObject().className()} | objectName: {self.objectName()}")

        self.setup_ui()
        logger.info("PlanetGenControlPanel initialized")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(12)

        # --- Form layout for inputs ---
        form = QFormLayout()

        self.radius_input = QDoubleSpinBox()
        self.radius_input.setRange(100, 50000)  # km
        self.radius_input.setValue(PLANET_CONFIG["planet_radius"])
        self.radius_input.setSuffix(" km")

        self.subdiv_input = QSpinBox()
        self.subdiv_input.setRange(0, 10)
        self.subdiv_input.setValue(PLANET_CONFIG["subdivisions"])

        form.addRow("Planet Radius:", self.radius_input)
        form.addRow("Subdivision Level:", self.subdiv_input)
        layout.addLayout(form)

        # --- Action buttons ---
        self.generate_btn = QPushButton("Generate Planet")
        self.export_btn = QPushButton("Export Planet to OBJ File")
        self.reset_btn = QPushButton("Reset Default Values")
        self.back_btn = QPushButton("Back")

        for btn in [
            self.generate_btn,
            self.export_btn,
            self.reset_btn,
            self.back_btn
        ]:
            layout.addWidget(btn)

        layout.addStretch()
