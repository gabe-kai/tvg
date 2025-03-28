# /ui/theme.py

"""
Centralized theme configuration for UI elements.
Supports swappable light and dark modes.
"""

DARK_THEME = """
    QWidget {
        background-color: #222;
        color: #eee;
    }
    
    #ContextPanel {
        background-color: #2b2b2b;
    }
    
    #ContentPanel {
        background-color: #1e1e1e;
    }

    QLabel {
        color: #ccc;
        background-color: transparent;
    }

    QSpinBox, QDoubleSpinBox {
        background-color: #333;
        color: #eee;
        border: 1px solid #555;
        padding: 4px;
    }

    QPushButton {
        background-color: #444;
        color: black;
        border: 1px solid #666;
        padding: 8px 16px;
        font-size: 16px;
    }

    QPushButton:hover {
        background-color: #555;
    }

    QPushButton:pressed {
        background-color: #333;
    }
"""
