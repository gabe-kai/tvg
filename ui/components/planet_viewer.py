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
    Embeds a 3D OpenGL-rendered preview of the planet mesh using moderngl-window.
    This is a headless container that spawns the OpenGL viewer as a separate window.
    """
    viewer_thread = None  # Class-level reference to track the running viewer

    def __init__(self, master, mesh_file_path=None, launch_viewer=True, **kwargs):
        """
        Args:
            master (tk.Widget): Parent widget.
            mesh_file_path (str): Path to the saved .mesh file.
            launch_viewer (bool): Whether to launch the OpenGL viewer thread immediately.
        """
        super().__init__(master, **kwargs)
        self.mesh_file_path = mesh_file_path or os.path.join("gamedata", "planets", "planet_test.mesh")

        self.canvas = tk.Canvas(self, width=300, height=300, bg="black")
        self.canvas.pack(fill="both", expand=True)

        if launch_viewer:
            self.after(100, self._start_viewer_thread)

    def _start_viewer_thread(self):
        """
        Safely launches the OpenGL viewer in a background thread, if not already running.
        """
        if not os.path.exists(self.mesh_file_path):
            print(f"[PlanetViewerFrame] Mesh file not found: {self.mesh_file_path}")
            return

        if PlanetViewerFrame.viewer_thread and PlanetViewerFrame.viewer_thread.is_alive():
            print("[PlanetViewerFrame] Viewer already running — skipping launch.")
            return

        thread = threading.Thread(target=self._launch_opengl_viewer, daemon=True)
        PlanetViewerFrame.viewer_thread = thread
        thread.start()

    def _launch_opengl_viewer(self):
        """
        Loads the mesh file and launches the moderngl-window viewer window.
        """
        import os
        os.environ["MODERNGL_WINDOW"] = "glfw"  # Explicitly choose GLFW backend
        try:
            mesh = PlanetMesh.load(self.mesh_file_path)
            PlanetMeshPreviewer.mesh_data = mesh
            mglw.run_window_config(PlanetMeshPreviewer)
        except Exception as e:
            print(f"[PlanetViewerFrame] Failed to load or display mesh: {e}")


class PlanetMeshPreviewer(mglw.WindowConfig):
    """
    A moderngl-window subclass that displays a spinning 3D preview of the planet mesh.
    """
    debug_wireframe: bool = True  # Set externally or from config
    mesh_data: PlanetMesh = None
    gl_version = (3, 3)
    title = "Planet Preview"
    window_size = (600, 600)
    aspect_ratio = None
    resizable = True

    def __init__(self, **kwargs):
        """
        Initializes OpenGL resources and loads the mesh geometry into buffers.
        """
        super().__init__(**kwargs)
        self.mesh = PlanetMeshPreviewer.mesh_data
        self.rotation = 0.0

        # Upload vertices and index buffer (using indexed drawing)
        self.vertex_data = self.mesh.vertices.astype("f4")
        self.index_data = self.mesh.faces.astype("i4").flatten()  # Flatten faces for index buffer

        # Compile GLSL shaders
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
                fragColor = vec4(0.85, 0.85, 0.85, 1.0);  // Neutral gray for wireframe
            }
            """
        )

        # Upload mesh to GPU buffers
        self.vbo = self.ctx.buffer(self.vertex_data.tobytes())
        self.ibo = self.ctx.buffer(self.index_data.tobytes())
        self.vao = self.ctx.vertex_array(
            self.prog,
            [(self.vbo, "3f", "in_position")],
            self.ibo
        )

        # Compute perspective projection matrix once
        radius = np.linalg.norm(self.mesh.vertices[0])
        far_plane = radius * 6.0
        self.projection = self.create_perspective(45.0, self.wnd.aspect_ratio, 0.1, far_plane)

    def on_render(self, _time: float, frame_time: float):
        """
        Called every frame. Applies rotation and renders the planet mesh.
        """
        self.ctx.clear(0.05, 0.05, 0.1)
        self.ctx.enable_only(moderngl.DEPTH_TEST)

        # Rotate mesh continuously over time
        self.rotation += frame_time * 0.5
        rotation_matrix = self.create_rotation_y(self.rotation)

        # Camera distance = 3x radius of planet
        radius = np.linalg.norm(self.mesh.vertices[0])
        eye_distance = radius * 3.0

        # Compute model-view-projection matrix
        view = self.create_look_at((0, 0, eye_distance), (0, 0, 0), (0, 1, 0))
        model = self.create_rotation_y(self.rotation)
        mvp = self.projection @ view @ model

        self.prog["mvp"].write(mvp.astype("f4").T.tobytes())
        if self.debug_wireframe:
            self.ctx.wireframe = True
        self.vao.render(mode=moderngl.TRIANGLES)

    @staticmethod
    def create_perspective(fov, aspect, near, far):
        """
        Creates a standard perspective projection matrix.
        """
        import math
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        return np.array([
            [f/aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
            [0, 0, -1, 0]
        ], dtype=np.float32)

    @staticmethod
    def create_look_at(eye, target, up):
        """
        Creates a view (camera) matrix for looking at a target point.
        """
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

    @staticmethod
    def create_rotation_y(angle):
        """
        Creates a Y-axis rotation matrix.
        """
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
