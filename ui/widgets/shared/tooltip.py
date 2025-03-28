# /ui/widgets/shared/tooltip.py

import tkinter as tk

class Tooltip:
    """
    A lightweight tooltip for tkinter widgets.
    Appears on hover, disappears on leave or click.
    """

    def __init__(self, widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay  # milliseconds before showing
        self.tip_window = None
        self._after_id = None

        self.widget.bind("<Enter>", self._schedule)
        self.widget.bind("<Leave>", self._unschedule)
        self.widget.bind("<ButtonPress>", self._unschedule)

    def _schedule(self, event=None):
        self._unschedule()
        self._after_id = self.widget.after(self.delay, self._show_tooltip)

    def _unschedule(self, event=None):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        self._hide_tooltip()

    def _show_tooltip(self):
        if self.tip_window or not self.text:
            return

        x, y, _, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + cy + 5

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # no border or title
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw, text=self.text, justify="left",
            background="#ffffe0", relief="solid", borderwidth=1,
            font=("Segoe UI", 9)
        )
        label.pack(ipadx=4, ipady=2)

    def _hide_tooltip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
