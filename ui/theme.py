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
    
    QWidget#HeaderPanel {
        background-color: #222;
        border-bottom: 2px solid #333;
    }
    
    QWidget#FooterPanel {
        background-color: #222;
        border-top: 2px solid #333;
    }
    
    QWidget#LeftPanel {
        background-color: #2b2b2b;
        border-right: 2px solid #333;
        padding: 4px;
        margin: 0px;
    }
    
    QWidget#RightPanel {
        background-color: #2b2b2b;
        border-left: 2px solid #333;
        padding: 4px;
        margin: 0px;
    }
    
    QWidget#ContentPanel {
        background-color: #1e1e1e;
        padding: 4px;
        margin: 0px;
    }
    
    QWidget#SmallContentPane {
        background-color: transparent;
        border: 1px solid #333;
        padding: 2px;
    }
    
    QTextEdit#SummaryTextBox {
        background: transparent;
        border: none;
    }

    QFrame#FloatingPanel {
        background-color: rgba(43, 43, 43, 224);
        border: 1px solid #333;
    }
    
    QLabel {
        color: #ccc;
        background-color: transparent;
        border: none;
    }
    
    QLabel#Title {
        color: #eee;
        font-size: 32px;
        font-weight: bold;
    }

    QLabel#Header1 {
        color: #eee;
        font-size: 24px;
        font-weight: bold;
    }

    QSpinBox, QDoubleSpinBox {
        background-color: #333;
        color: #eee;
        border: 1px solid #555;
        padding: 4px;
    }
    
    QCheckBox {
        background-color: transparent;
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
