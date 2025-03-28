# /ui/screens/planetgen_screen.py

import threading
import sys
import subprocess
import tkinter as tk
from tkinter import ttk
from logger.logger import LoggerFactory
from ui.widgets.planetgen.input_panel import InputPanel
from ui.widgets.shared.log_viewer import LogViewer


class PlanetGenScreen(tk.Frame):
    def __init__(self, master, state_manager):
        self.logger = LoggerFactory("PlanetGenScreen").get_logger()
        self.mesh_file_path = "gamedata/planets/planet_test.mesh"
        super().__init__(master)
        self.state_manager = state_manager
        self.log_expanded = False
        self._build_layout()

    def _build_layout(self):
        # Root container
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Footer area (initial height controlled by log box)
        self.footer = tk.Frame(container, bg="lightgray", bd=2, relief="groove")
        self.footer.pack(side="bottom", fill="x")

        # Log viewer widget
        self.log_box = LogViewer(self.footer, height=3)
        self.log_box.pack(fill="both", expand=True, side="left")

        # Expand/collapse toggle button
        toggle_btn = ttk.Button(self.footer, text="▲", width=3, command=self._toggle_log_height)
        toggle_btn.pack(side="right", padx=4, pady=4)
        self.toggle_button = toggle_btn

        # Main content area (everything above the footer)
        main_area = tk.Frame(container)
        main_area.pack(side="top", fill="both", expand=True)

        # Left panel
        left_panel = tk.Frame(main_area, bd=2, relief="ridge")
        left_panel.pack(side="left", fill="both", expand=True)

        # Right panel
        right_panel = tk.Frame(main_area, bd=2, relief="ridge", width=250)
        right_panel.pack(side="right", fill="y")

        # Input panel widget
        self.input_panel = InputPanel(
            right_panel,
            default_radius=6371,
            default_subdiv=6,
            on_generate=self._generate_planet,
            on_export=self._export_planet,
            on_back=self._go_back,
            on_reset=self._reset_to_defaults,
        )
        self.input_panel.pack(fill="both", expand=True)

    def _toggle_log_height(self):
        """
        Toggle the height of the log viewer between compact and expanded.
        When expanded, float the log viewer above main content with transparency.
        """
        if self.log_expanded:
            self.log_box.text.config(height=3)
            self.footer.place_forget()
            self.footer.pack(side="bottom", fill="x")
            self.toggle_button.config(text="▲")
        else:
            self.footer.pack_forget()
            self.footer.place(relx=0, rely=0.7, relwidth=1.0, relheight=0.3)
            self.footer.lift()
            self.footer.attributes = getattr(self.footer, 'attributes', lambda *args, **kwargs: None)
            self.footer.attributes("-alpha", 0.9)  # best-effort transparency
            self.log_box.text.config(height=15)
            self.toggle_button.config(text="▼")

        self.log_expanded = not self.log_expanded

    def _generate_planet(self):
        """
        Launches the planet generation subprocess and streams its stdout to the UI.
        """
        try:
            radius = float(self.input_panel.get_radius())
            subdivisions = int(self.input_panel.get_subdivisions())

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
        self.logger.info("Switching to welcome screen")
        self.state_manager.switch_screen("welcome")

    def _reset_to_defaults(self):
        if self.input_panel:
            self.input_panel.reset_defaults()

    def _append_log(self, message: str):
        """
        Appends a message to the read-only log box.
        Strips ANSI color codes for readability in plain Tkinter.
        TODO: Upgrade this to support colorized output using tag styles.
        """
        # Strip ANSI codes and append cleanly
        import re
        ansi_escape = re.compile(r"\[[0-9;]*m")
        clean_message = ansi_escape.sub("", message)
        self.log_box.append(clean_message)

    def _run_subprocess(self, cmd):
        import subprocess
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8") as proc:
            for line in proc.stdout:
                self._append_log(line)
