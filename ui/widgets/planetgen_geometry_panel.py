# /ui/widgets/planetgen_geometry_panel.py

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class PlanetGenGeometryPanel(QWidget):
    """
    A floating panel to display planet geometry summary information.
    This widget is designed to overlay the planet preview panel.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(280, 140)
        self.setStyleSheet(
            """
            background-color: #333;
            color: #ccc;
            border: 1px solid #555;
            padding: 6px;
            """
        )
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Layout and content
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setSpacing(4)

        self.label = QLabel("[ Geometry Summary Panel ]")
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
