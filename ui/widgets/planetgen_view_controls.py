# /ui/widgets/planetgen_view_controls.py

from PySide6.QtWidgets import QWidget, QCheckBox, QVBoxLayout
from PySide6.QtCore import Qt
from logger.logger import LoggerFactory


class PlanetGenViewControls(QWidget):
    """
    A floating widget with options for viewing the planet mesh preview.
    Currently includes a wireframe toggle.
    """

    def __init__(self, parent=None, preview_widget=None):
        super().__init__(parent)
        self.preview_widget = preview_widget
        self.logger = LoggerFactory("planet_view_controls").get_logger()
        self.setFixedWidth(200)
        self.setObjectName("SmallContentPane")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        self.wireframe_toggle = QCheckBox("Wireframe Mode")
        self.wireframe_toggle.stateChanged.connect(self.toggle_wireframe)
        layout.addWidget(self.wireframe_toggle)

    def toggle_wireframe(self, state):
        if self.preview_widget is None:
            return

        enable_wireframe = state != 0
        self.logger.info(f"Wireframe toggle: {'ON' if enable_wireframe else 'OFF'} (raw state: {state})")
        self.preview_widget.set_wireframe_mode(enable_wireframe)
