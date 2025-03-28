# /ui/widgets/planetgen_geometry_panel.py

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt


class PlanetGenGeometryPanel(QWidget):
    """
    A floating panel to display planet geometry summary information.
    This widget is designed to overlay the planet preview panel.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: transparent; border: none;")

        # Layout and content
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(8)

        self.label = QLabel("[ Geometry Summary Panel ]")
        self.label.setStyleSheet("background-color: #2a2a2a; border: 1px solid #555; padding: 6px;")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.label)

    def update_summary(self, data: dict):
        """
        Update the panel contents with a geometry summary dictionary.

        :param data: Dictionary of geometry values (float or str)
        """
        lines = []
        for key, value in data.items():
            if isinstance(value, float):
                lines.append(f"{key.replace('_', ' ').title()}: {value:,.2f}")
            else:
                lines.append(f"{key.replace('_', ' ').title()}: {value:,}")

        self.label.setText("\n".join(lines))
        self.label.setWordWrap(True)
        self.label.adjustSize()
        self.adjustSize()
