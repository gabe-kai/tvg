# /ui/widgets/planetgen/input_panel.py

import tkinter as tk
from tkinter import ttk
from ui.widgets.shared.tooltip import Tooltip

class InputPanel(tk.Frame):
    """
    Planet generation input panel containing radius/subdiv fields and action buttons.
    Designed to be mounted on the right side of the screen.
    """

    def __init__(self, master, default_radius, default_subdiv,
                 on_generate, on_export, on_back, on_reset, **kwargs):
        super().__init__(master, **kwargs)

        self.default_radius = default_radius
        self.default_subdiv = default_subdiv

        self._build_ui(on_generate, on_export, on_back, on_reset)

    def _build_ui(self, on_generate, on_export, on_back, on_reset):
        title = ttk.Label(self, text="Planet Generation", font=("Arial", 18, "bold"))
        title.pack(pady=(0, 20))

        # Radius input
        radius_label = ttk.Label(self, text="Planet Radius (km):")
        radius_label.pack(anchor="w")
        self.radius_entry = ttk.Entry(self)
        self.radius_entry.insert(0, str(self.default_radius))
        self.radius_entry.pack(fill="x", pady=(0, 10))
        Tooltip(self.radius_entry, "Recommended: 3390 - 25500 km\nMinimum allowed: 10 km")

        # Subdivision input
        subdiv_label = ttk.Label(self, text="Subdivision Level:")
        subdiv_label.pack(anchor="w")
        self.subdiv_entry = ttk.Entry(self)
        self.subdiv_entry.insert(0, str(self.default_subdiv))
        self.subdiv_entry.pack(fill="x", pady=(0, 10))
        Tooltip(self.subdiv_entry, "Controls mesh detail level (min: 2, max: 12)")

        # Buttons
        reset_btn = ttk.Button(self, text="Reset to Defaults", command=on_reset)
        reset_btn.pack(fill="x", pady=(0, 10))

        generate_btn = ttk.Button(self, text="Generate Planet", command=on_generate)
        generate_btn.pack(fill="x")

        export_btn = ttk.Button(self, text="Export Planet as OBJ", command=on_export)
        export_btn.pack(fill="x", pady=(10, 0))

        back_btn = ttk.Button(self, text="Back to Main Menu", command=on_back)
        back_btn.pack(fill="x", pady=(10, 0))

    def get_radius(self) -> float:
        return float(self.radius_entry.get())

    def get_subdivisions(self) -> int:
        return int(self.subdiv_entry.get())

    def reset_defaults(self):
        self.radius_entry.delete(0, "end")
        self.radius_entry.insert(0, str(self.default_radius))

        self.subdiv_entry.delete(0, "end")
        self.subdiv_entry.insert(0, str(self.default_subdiv))
