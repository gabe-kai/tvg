# /ui/screens/planetgen_screen.py

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from logger.logger import LoggerFactory
import subprocess
import threading
import sys
import re
from planet_generator.planet_config import PLANET_CONFIG
from ui.components.planet_viewer import PlanetViewerFrame

if TYPE_CHECKING:
    from ui.state_manager import UIStateManager

# Regex to strip ANSI escape sequences from subprocess output
ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')

class PlanetGenScreen(tk.Frame):
    """
    The screen responsible for configuring and initiating planet generation.
    Displays controls for radius, subdivision levels, and a button to start generation.
    """

    def __init__(self, master, state_manager: "UIStateManager"):
        """
        Initializes the PlanetGenScreen.

        Args:
            master (tk.Tk or tk.Frame): The parent widget.
            state_manager (UIStateManager): Object managing screen transitions.
        """
        super().__init__(master)
        self.state_manager = state_manager
        self.logger = LoggerFactory("PlanetGenScreen").get_logger()
        self.configure(padx=50, pady=50)

        self.default_radius = PLANET_CONFIG.get("planet_radius", 6371)
        self.default_subdiv = PLANET_CONFIG.get("subdivisions", 3)

        self._build_widgets()

    def _build_widgets(self):
        """
        Builds and places the UI widgets for planet generation configuration.
        """
        title = ttk.Label(self, text="Planet Generation", font=("Arial", 18, "bold"))
        title.pack(pady=(0, 20))

        # Radius Input
        radius_label = ttk.Label(self, text="Planet Radius (km):")
        radius_label.pack(anchor="w")
        self.radius_entry = ttk.Entry(self)
        self.radius_entry.insert(0, str(self.default_radius))
        self.radius_entry.pack(fill="x", pady=(0, 10))
        self._add_tooltip(self.radius_entry, "Recommended: 3390 - 25500 km\nMinimum allowed: 10 km")

        # Subdivision Input
        subdiv_label = ttk.Label(self, text="Subdivision Level:")
        subdiv_label.pack(anchor="w")
        self.subdiv_entry = ttk.Entry(self)
        self.subdiv_entry.insert(0, str(self.default_subdiv))
        self.subdiv_entry.pack(fill="x", pady=(0, 10))
        self._add_tooltip(self.subdiv_entry, "Controls mesh detail level (min: 2, max: 12)")

        # Reset Button
        reset_btn = ttk.Button(self, text="Reset to Defaults", command=self._reset_to_defaults)
        reset_btn.pack(fill="x", pady=(0, 10))

        # Generate Button
        generate_btn = ttk.Button(self, text="Generate Planet", command=self._generate_planet)
        generate_btn.pack(fill="x")

        # Export OBJ Button
        export_btn = ttk.Button(self, text="Export Planet as OBJ", command=self._export_planet)
        export_btn.pack(fill="x", pady=(10, 0))

        # Back Button
        back_btn = ttk.Button(self, text="Back to Main Menu", command=self._go_back)
        back_btn.pack(fill="x", pady=(10, 0))

        # Output Log Box
        self.log_box = tk.Text(self, height=12, wrap="word", state="disabled", bg="#f7f7f7", font=("Segoe UI", 10))
        self.log_box.pack(fill="both", expand=True, pady=(20, 0))

        # Planet Viewer Frame
        import os
        self.mesh_file_path = os.path.join("gamedata", "planets", "planet_test.mesh")
        self.viewer = PlanetViewerFrame(self, mesh_file_path=self.mesh_file_path, launch_viewer=False)
        self.viewer.pack(fill="both", expand=True, pady=(20, 0))

    def _reset_to_defaults(self):
        """
        Resets the radius and subdivision inputs to default values from config.
        """
        self.radius_entry.delete(0, tk.END)
        self.radius_entry.insert(0, str(self.default_radius))

        self.subdiv_entry.delete(0, tk.END)
        self.subdiv_entry.insert(0, str(self.default_subdiv))

    def _generate_planet(self):
        """
        Launches the planet generation subprocess and streams its stdout to the UI.
        """
        try:
            radius = float(self.radius_entry.get())
            subdivisions = int(self.subdiv_entry.get())

            if radius < 10:
                raise ValueError("Planet radius must be at least 10 km.")
            if subdivisions < 2 or subdivisions > 12:
                raise ValueError("Subdivision level must be between 2 and 12.")

            self.logger.info(f"Launching subprocess with radius={radius}, subdivisions={subdivisions}")
            self._append_log(f"Generating planet with radius={radius}, subdivisions={subdivisions}...\n")

            cmd = [
                sys.executable, "-m", "planet_generator.generate_planet",
                "--radius", str(radius),
                "--subdivisions", str(subdivisions)
            ]

            thread = threading.Thread(target=self._run_subprocess, args=(cmd,))
            thread.start()

        except ValueError as e:
            self._append_log(f"Input Error: {e}\n")
            self.logger.error(f"Input validation failed: {e}")

    def _run_subprocess(self, cmd):
        """
        Runs a subprocess and streams output to the log box.
        """
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            for line in process.stdout:
                self._append_log(line)
            process.wait()

            if process.returncode == 0:
                self._append_log("Planet generation completed successfully.")
                self.viewer.destroy()
                from ui.components.planet_viewer import PlanetMeshPreviewer
                PlanetMeshPreviewer.debug_wireframe = PLANET_CONFIG.get("debug_wireframe", True)
                self.viewer = PlanetViewerFrame(self, mesh_file_path=self.mesh_file_path)
                self.viewer.pack(fill="both", expand=True, pady=(20, 0))
            else:
                self._append_log(f"Error: process exited with code {process.returncode}\n")

        except Exception as e:
            self._append_log(f"Exception occurred: {e}\n")
            self.logger.exception("Subprocess failed")

    def _append_log(self, message):
        """
        Appends a message to the read-only log box.
        Strips ANSI color codes for readability in plain Tkinter.
        TODO: Upgrade this to support colorized output using tag styles.
        """
        clean_message = ANSI_ESCAPE.sub('', message)
        self.log_box.config(state="normal")
        self.log_box.insert("end", clean_message)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def _add_tooltip(self, widget, text):
        """
        Binds a simple tooltip to a given widget.
        """
        def on_enter(event):
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + 20
            self.tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 9))
            label.pack()

        def on_leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                del self.tooltip

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def _export_planet(self):
        """
        Exports the most recently generated planet mesh as an OBJ file via CLI hook.
        """
        import os

        try:
            cmd = [
                sys.executable,
                os.path.join("planet_generator", "exporters", "export_planet.py"),
                self.mesh_file_path,
                "--output", "planet.obj", "--normals"
            ]
            self._append_log("Exporting planet to OBJ format with normals via command line...")
            subprocess.run(cmd, check=True)
            self._append_log("Planet exported to OBJ format: gamedata/exports/planet.obj")
        except subprocess.CalledProcessError as e:
            self._append_log(f"Export process failed: {e}")
            self.logger.exception("Export subprocess failed")
        except Exception as e:
            self._append_log(f"Export failed: {e}")
            self.logger.exception("Unexpected error during export")

    def _go_back(self):
        """
        Returns the user to the welcome screen.
        """
        self.state_manager.switch_screen("welcome")
