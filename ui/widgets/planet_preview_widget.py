# /ui/widgets/planet_preview_widget.py

from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
import numpy as np
import joblib
import os


from logger.logger import LoggerFactory

class PlanetPreviewWidget(QOpenGLWidget):
    """
    OpenGL widget to preview a generated planet mesh.
    Loads from joblib .mesh format and renders as triangle mesh.
    """

    def __init__(self, mesh_path, parent=None):
        super().__init__(parent)
        self.mesh_ready = False
        self.mesh_path = mesh_path
        self.vertices = None
        self.faces = None
        self.wireframe_mode = False
        self.logger = LoggerFactory("planet_preview").get_logger()

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
        glMatrixMode(GL_MODELVIEW)

    def set_wireframe_mode(self, enabled: bool):
        """Enable or disable OpenGL wireframe mode."""
        self.wireframe_mode = enabled
        self.update()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if self.wireframe_mode else GL_FILL)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if self.vertices is not None and len(self.vertices) > 0:
            radius = np.linalg.norm(self.vertices[0])
            distance = radius * 2.75
        else:
            distance = 15000.0

        glTranslatef(0.0, 0.0, -distance)
        glRotatef(30, 1.0, 0.0, 0.0)
        glRotatef(45, 0.0, 1.0, 0.0)
        self.draw_planet()

    def load_mesh(self):
        """Loads the mesh from a .mesh file using joblib."""
        if not os.path.exists(self.mesh_path):
            self.logger.warning(f"Mesh file not found: {self.mesh_path}")
            return

        mesh = joblib.load(self.mesh_path)
        self.vertices = mesh.vertices  # shape (n, 3), np.ndarray
        self.faces = mesh.faces       # shape (m, 3), np.ndarray
        self.logger.info(f"Loaded mesh with {len(self.vertices)} vertices and {len(self.faces)} faces")
        self.mesh_ready = True

    def draw_planet(self):
        if not self.mesh_ready or self.vertices is None or self.faces is None:
            return

        glColor3f(0.4, 0.8, 1.0)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for idx in face:
                v = self.vertices[int(idx)]
                glVertex3f(float(v[0]), float(v[1]), float(v[2]))
        glEnd()

    def reload_mesh(self):
        self.load_mesh()
        self.update()
