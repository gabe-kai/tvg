# /ui/widgets/planetgen_geometry_panel.py

from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt


class PlanetGenGeometryPanel(QWidget):
    """
    A floating panel to display planet geometry summary information.
    This widget is designed to overlay the planet preview panel.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setObjectName("SmallContentPane")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Layout and content
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(8)

        self.textbox = QTextEdit()
        self.textbox.setObjectName("SummaryTextBox")
        self.textbox.setReadOnly(True)
        self.textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(self.textbox)

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

        content = "\n".join(lines)
        self.textbox.setText(content)

        # Resize textbox height to match number of lines (up to 8)
        font_metrics = self.textbox.fontMetrics()
        line_height = font_metrics.lineSpacing()
        line_count = content.count("\n") + 1
        max_lines = 8

        height = min(line_count, max_lines) * line_height + 12
        self.textbox.setMinimumHeight(height)
        self.textbox.setMaximumHeight(height if line_count <= max_lines else line_height * max_lines + 12)
