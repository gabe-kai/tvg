# /ui/tests/test_opengl_widget.py

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
import joblib
import numpy as np
import os
import sys


class PlanetMeshPreviewWidget(QOpenGLWidget):
    """
    A standalone OpenGL widget that loads and renders a generated planet mesh.
    Used to debug rendering of gamedata/planets/planet_test.mesh
    """

    def __init__(self, mesh_path, parent=None):
        super().__init__(parent)
        self.mesh_path = mesh_path
        self.vertices = None
        self.faces = None

    def initializeGL(self):
        glClearColor(0.05, 0.05, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)
        self.load_mesh()

    def resizeGL(self, w, h):
        aspect = w / h if h else 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, aspect, 100.0, 100000.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Dynamically calculate camera distance based on radius
        if self.vertices is not None and len(self.vertices) > 0:
            radius = np.linalg.norm(self.vertices[0])
            distance = radius * 2.75
        else:
            distance = 12000.0  # fallback value

        glTranslatef(0.0, 0.0, -distance)
        glRotatef(30, 1.0, 0.0, 0.0)
        glRotatef(45, 0.0, 1.0, 0.0)
        self.draw_planet()

    def load_mesh(self):
        if not os.path.exists(self.mesh_path):
            print(f"[Test] Mesh file not found: {self.mesh_path}")
            return

        mesh = joblib.load(self.mesh_path)
        self.vertices = mesh.vertices
        self.faces = mesh.faces
        print(f"[Test] Loaded mesh: {len(self.vertices)} vertices, {len(self.faces)} faces")

    def draw_planet(self):
        if self.vertices is None or self.faces is None:
            return

        glColor3f(0.4, 0.8, 1.0)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for idx in face:
                v = self.vertices[int(idx)]
                glVertex3f(float(v[0]), float(v[1]), float(v[2]))
        glEnd()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("OpenGL Test - Planet Mesh")
    window.setGeometry(100, 100, 800, 600)
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    mesh_path = os.path.join(root_dir, "gamedata", "planets", "planet_test.mesh")
    preview = PlanetMeshPreviewWidget(mesh_path)
    window.setCentralWidget(preview)
    window.show()
    sys.exit(app.exec())
