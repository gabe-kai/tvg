# /ui/components/planet_viewer.py

import tkinter as tk
import threading
import moderngl_window as mglw
import moderngl
import numpy as np
import os
from planet_generator.planet_mesh import PlanetMesh

class PlanetViewerFrame(tk.Frame):
    """
    Embeds a 3D OpenGL-rendered preview of the planet mesh.
    Uses moderngl-window to load and display a spinning icosphere mesh.
    """

    def __init__(self, master, mesh_file_path=None, **kwargs):
        super().__init__(master, **kwargs)
        self.mesh_file_path = mesh_file_path or os.path.join("gamedata", "planets", "planet_test.mesh")

        self.canvas = tk.Canvas(self, width=300, height=300, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.after(100, self._start_viewer_thread)

    def _start_viewer_thread(self):
        thread = threading.Thread(target=self._launch_opengl_viewer, daemon=True)
        thread.start()

    def _launch_opengl_viewer(self):
        try:
            mesh = PlanetMesh.load(self.mesh_file_path)
            PlanetMeshPreviewer.mesh_data = mesh
            mglw.run_window_config(PlanetMeshPreviewer)
        except Exception as e:
            print(f"[PlanetViewerFrame] Failed to load or display mesh: {e}")


class PlanetMeshPreviewer(mglw.WindowConfig):
    mesh_data: PlanetMesh = None
    gl_version = (3, 3)
    title = "Planet Preview"
    window_size = (600, 600)
    aspect_ratio = None
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mesh = PlanetMeshPreviewer.mesh_data
        self.rotation = 0.0

        # Flatten mesh faces into triangles
        vertices = self.mesh.vertices
        faces = self.mesh.faces
        triangles = vertices[faces.flatten()]
        self.vertex_data = triangles.astype("f4")

        # Setup OpenGL resources
        self.prog = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec3 in_position;
            uniform mat4 mvp;
            void main() {
                gl_Position = mvp * vec4(in_position, 1.0);
            }
            """,
            fragment_shader="""
            #version 330
            out vec4 fragColor;
            void main() {
                fragColor = vec4(0.6, 0.8, 1.0, 1.0);
            }
            """
        )

        self.vbo = self.ctx.buffer(self.vertex_data.tobytes())
        self.vao = self.ctx.vertex_array(
            self.prog,
            [(self.vbo, "3f", "in_position")]
        )

        # Set up a basic projection matrix (we'll rotate model matrix)
        self.projection = self.create_perspective(45.0, self.wnd.aspect_ratio, 0.1, 100.0)

    def on_render(self, _time: float, frame_time: float):
        self.ctx.clear(0.05, 0.05, 0.1)
        self.ctx.enable_only(moderngl.DEPTH_TEST)

        self.rotation += frame_time * 0.5
        rotation_matrix = self.create_rotation_y(self.rotation)
        modelview = self.create_look_at((0, 0, 3), (0, 0, 0), (0, 1, 0)) @ rotation_matrix
        mvp = self.projection @ modelview

        self.prog["mvp"].write(mvp.astype("f4").tobytes())
        self.vao.render(moderngl.TRIANGLES)

    def create_perspective(self, fov, aspect, near, far):
        import math
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        return np.array([
            [f/aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
            [0, 0, -1, 0]
        ], dtype=np.float32)

    def create_look_at(self, eye, target, up):
        from numpy.linalg import norm
        eye = np.array(eye, dtype=np.float32)
        target = np.array(target, dtype=np.float32)
        up = np.array(up, dtype=np.float32)
        f = (target - eye); f /= norm(f)
        r = np.cross(f, up); r /= norm(r)
        u = np.cross(r, f)
        mat = np.eye(4, dtype=np.float32)
        mat[:3, 0] = r
        mat[:3, 1] = u
        mat[:3, 2] = -f
        mat[0, 3] = -np.dot(r, eye)
        mat[1, 3] = -np.dot(u, eye)
        mat[2, 3] = np.dot(f, eye)
        return mat

    def create_rotation_y(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
