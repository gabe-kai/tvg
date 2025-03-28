# /ui/widgets/planetgen_control_panel.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QFormLayout, QDoubleSpinBox, QSpinBox, QCheckBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from logger.logger import LoggerFactory
from planet_generator.planet_config import PLANET_CONFIG
from planet_generator.planet_utils.mesh_tools import estimate_optimal_subdivision
import subprocess
import sys
import os

logger = LoggerFactory("planetgen_control_panel").get_logger()


class PlanetGenControlPanel(QWidget):
    """
    Widget for controlling planet generation parameters.
    Contains inputs for radius and subdivision level, and buttons
    to generate, export, reset, or go back.
    """
    inputs_changed = Signal()  # Emitted when radius or subdivision values change
    mesh_generated = Signal()  # Emitted when mesh is successfully generated

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ContextPanel")  # Allow styling via theme

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

        # Radius input
        self.radius_input = QDoubleSpinBox()
        self.radius_input.setRange(10, 51000)  # km
        self.radius_input.setValue(PLANET_CONFIG["planet_radius"])
        self.radius_input.setSuffix(" km")
        self.radius_input.setToolTip("Radius of the planet in kilometers. Min: 10 km, Max: 51,000 km")
        self.radius_input.valueChanged.connect(self.on_radius_changed)

        # Subdivision suggestion label
        self.suggested_label = QLabel()

        # Subdivision input
        self.subdiv_input = QSpinBox()
        self.subdiv_input.setRange(2, 16)
        self.subdiv_input.setValue(PLANET_CONFIG["subdivisions"])
        self.subdiv_input.setToolTip("Number of icosphere subdivisions. Min: 2, Max: 16")
        self.subdiv_input.valueChanged.connect(lambda _: self.inputs_changed.emit())

        form.addRow("Planet Radius:", self.radius_input)
        form.addRow("", self.suggested_label)
        form.addRow("Subdivision Level:", self.subdiv_input)
        layout.addLayout(form)

        self.update_subdivision_suggestion(PLANET_CONFIG["planet_radius"])

        # --- Action buttons ---
        self.generate_btn = QPushButton("Generate Planet")
        self.export_btn = QPushButton("Export Planet to OBJ File")
        self.reset_btn = QPushButton("Reset Default Values")
        self.back_btn = QPushButton("Back")

        layout.addWidget(self.generate_btn)
        layout.addWidget(self.export_btn)

        # --- Export Options Panel ---
        export_options = QFrame()
        export_options_layout = QVBoxLayout(export_options)
        export_options_layout.setContentsMargins(16, 0, 0, 0)
        self.include_normals_checkbox = QCheckBox("Include Normals in Export")
        self.include_normals_checkbox.setChecked(False)
        export_options_layout.addWidget(self.include_normals_checkbox)
        layout.addWidget(export_options)

        layout.addWidget(self.reset_btn)
        layout.addWidget(self.back_btn)

        layout.addStretch()

        # Connect signals
        self.back_btn.clicked.connect(self.go_back_to_welcome)
        self.reset_btn.clicked.connect(self.reset_defaults)
        self.generate_btn.clicked.connect(self.run_planet_generation_cli)
        self.export_btn.clicked.connect(self.run_export_planet_cli)

    def on_radius_changed(self, value):
        """Respond to radius changes and update suggestion label."""
        self.inputs_changed.emit()
        self.update_subdivision_suggestion(value)

    def update_subdivision_suggestion(self, radius):
        """Update the label with the recommended subdivision for the current radius."""
        suggestion = estimate_optimal_subdivision(radius)
        self.suggested_label.setText(f"Suggested Subdivision: {suggestion}")

    def go_back_to_welcome(self):
        """
        Slot: Trigger UI state change to return to the welcome screen.
        """
        logger.info("Back button clicked. Returning to Welcome screen.")

        from ui.state.ui_state_manager import UIState

        ui_manager = self.get_ui_state_manager()
        if ui_manager:
            ui_manager.set_state(UIState.WELCOME)
        else:
            logger.warning("No UI state manager found to handle transition.")

    def reset_defaults(self):
        """
        Slot: Reset input fields to default values from configuration.
        """
        logger.info("Resetting input fields to default values.")
        self.radius_input.setValue(PLANET_CONFIG["planet_radius"])
        self.subdiv_input.setValue(PLANET_CONFIG["subdivisions"])

    def run_planet_generation_cli(self):
        """
        Slot: Call the generate_planet.py script with CLI args.
        """
        radius = self.radius_input.value()
        subdivisions = self.subdiv_input.value()

        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "..", "planet_generator", "generate_planet.py"
        )
        script_path = os.path.normpath(script_path)

        logger.info(f"Running planet generator script with radius={radius}, subdivisions={subdivisions}")

        try:
            subprocess.run(
                [sys.executable, script_path, "--radius", str(radius), "--subdivisions", str(subdivisions)],
                check=True
            )
            logger.info("Planet generation subprocess completed successfully.")
            self.mesh_generated.emit()
        except subprocess.CalledProcessError as e:
            logger.error(f"Planet generation script failed: {e}")

    def run_export_planet_cli(self):
        """
        Slot: Call the export_planet.py script as a subprocess.
        """
        input_path = os.path.normpath(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "..", "gamedata", "planets", "planet_test.mesh"
        ))

        script_path = os.path.normpath(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "..", "planet_generator", "exporters", "export_planet.py"
        ))

        logger.info(f"Exporting mesh from: {input_path}")
        include_normals = self.include_normals_checkbox.isChecked()

        try:
            cmd = [sys.executable, script_path, input_path, "--output", "planet.obj"]
            if include_normals:
                cmd.append("--normals")

            subprocess.run(cmd, check=True)
            logger.info("Export to OBJ completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Export script failed: {e}")

    def get_ui_state_manager(self):
        """
        Traverse upward to find a parent with set_state method.
        """
        widget = self.parent()
        while widget:
            if hasattr(widget, "set_state"):
                return widget
            widget = widget.parent()
        return None
