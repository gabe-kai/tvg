# /ui/widgets/shared/log_viewer.py

import tkinter as tk
from tkinter import ttk

class LogViewer(tk.Frame):
    """
    A reusable text log output widget with vertical scrollbar, fixed height, and word wrapping.
    Typically placed at the bottom of a UI for streaming status or log messages.
    """

    def __init__(self, master, height=3, **kwargs):
        super().__init__(master, **kwargs)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.text = tk.Text(
            self,
            height=height,
            wrap="word",
            state="disabled",
            bg="#f7f7f7",
            font=("Segoe UI", 10),
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.config(command=self.text.yview)

        self.scrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

    def append(self, message: str):
        """
        Appends a new line of text to the log viewer.
        Automatically scrolls to the end.
        """
        self.text.config(state="normal")
        self.text.insert("end", message)
        self.text.see("end")
        self.text.config(state="disabled")

    def clear(self):
        """
        Clears all content from the log.
        """
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        self.text.config(state="disabled")
