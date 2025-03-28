# /ui/screens/planetgen.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt
from logger.logger import LoggerFactory
from ui.widgets.planetgen_control_panel import PlanetGenControlPanel
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
        self.left_panel = QLabel("[ Planet Preview Area ]")
        self.left_panel.setObjectName("ContentPanel")
        self.left_panel.setAlignment(Qt.AlignCenter)
        self.left_panel.setStyleSheet("border: 1px solid #666;")
        self.left_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
