# Project Status

`\Status.md`

This file is intended to help ChatGPT (and me) remember where we are in the project, and to get quickly caught up when it's time to start a new conversation.

---

## Daily Commit Summaries
 
- 2025.03.26: Rebuilt the icosphere generator, and pre-elevation modification steps with object-oriented code, and better logging.
- 2025.03.27: Implemented save-files for the Planet object. Implemented a basic UI for planet generation and viewing. Dismissed it all and started a new branch to build the UI with PySide6.

---

## In-Progress

Build basic UI and visualizer. You're in the "pyside6-ui-rebuild" git branch.

### 💾 Mesh Storage & Querying

- [x] Design and implement a `PlanetMesh` class to hold:
  - Vertices, faces, face geometry, adjacency
  - Spatial query helpers (by face index, lat/lon, center proximity)
- [ ] Build support for extracting local face groups (e.g. 7-tile hex rings)
- [ ] Add file-based persistence (Flatbuffers, MessagePack, or custom binary)
- [ ] Enable loading mesh data for off-screen processing (pathfinding, climate)

---

## ToDo

### 🖥️ UI + Visualization

- [ ] Implement a GUI for planet generation parameters
  - [ ] Use **PySide6** for simple controls (radius, subdivisions)
  - [ ] Include button to trigger mesh generation and show logs

- [ ] Add interactive mesh viewer
  - [ ] Use **QOpenGLWidget** for OpenGL-based GPU rendering
  - [ ] Display colored faces, camera control (orbit/zoom)
  - [ ] Prepare hooks for face selection and overlay layers (e.g., slope, biome)

### 🌐 Geometry & Mesh Analysis

- [ ] Add face curvature (convexity/concavity detection)
- [ ] Add vertex-to-face mapping for potential region-growing or river pathing
- [ ] Add neighbor-aware slope smoothing or erosion hooks

### 🌋 Tectonics & Terrain

- [ ] Seed initial cratons or tectonic plates
- [ ] Implement plate growth using adjacency map
- [ ] Handle plate collisions, subduction, and ridge formation
- [ ] Calculate elevation deformation based on plate stress

### 🗺️ Biomes & Environment

- [ ] Determine temperature map based on latitude and elevation
- [ ] Estimate sunlight (insolation) per face
- [ ] Apply slope and moisture to assign biome types

### 🧪 Debug & Output Enhancements

- [ ] Add data export (CSV, JSON, or flatbuffers)
- [ ] Preview map layers using matplotlib or Pillow
- [ ] Add ability to save and reload raw mesh state


---

## File & Folder Structure
```
tvg/
├── .venv/                          # Virtual environment (auto-managed by PyCharm)
│
├── gamedata/
│   ├── exports/                    # Storage for planets exported as OBJ files
│   └── planets/                    # Storage for planet objects
│
├── logger/                         # Centralized logging tools
│   ├── __init__.py                 # Marks as a package
│   └── logger.py                   # LoggerFactory with color output and rotating file handler
│
├── logs/                           # Auto-created directory for logs
│   └── tvg.log                     # Output file for logs (rotated based on config)
│
├── planet_generator/               # Main planetary generation module
│   ├── exporters/
│   │   ├── __init__.py             # Marks as a package
│   │   └── export_planet.py        # Takes PlanetMesh and exports an OBJ (# TODO: Add .Blend)
│   │
│   ├── geometry/                   # Planetary mesh generation and spatial data
│   │   ├── __init__.py             # Marks as a package
│   │   ├── adjacency.py            # Calculates which faces share edges
│   │   ├── face_geometry.py        # Computes face centers, normals, area, slope, and lat/lon
│   │   └── icosphere.py            # Builds and subdivides an icosahedral sphere mesh
│   │
│   ├── planet_utils/               # Shared utility methods for geometry/topology
│   │   ├── __init__.py             # Marks as a package
│   │   └── mesh_tools.py           # Mesh inspection tools (validate_vertex_distances, summarize_mesh_geometry, etc)
│   │
│   ├── __init__.py                 # Marks as a package
│   ├── generate_planet.py          # Orchestrates full generation process
│   ├── planet_config.py            # User-editable settings for world generation
│   └── planet_mesh.py              # Needs description
│
├── ui/                             # UI package for all interface logic
│   ├── components/                 # Reusable components more significant than widgets
│   │   ├── __init__.py
│   │
│   ├── screens/                    # Individual screens/views (e.g. welcome, settings)
│   │   ├── __init__.py
│   │   ├── planetgen.py            # Planet generation screen with options and previewer
│   │   └── welcome.py              # The game welcome screen (new game, load game, options, about, & quit)
│   │
│   ├── tests/                      # Standalone files for testing functionality before integration
│   │   └── test_opengl_widget.py   # OpenGL viewer test.
│   │
│   ├── widgets/                    # Reusable widgets (e.g., log viewer, sliders)
│   │   ├── __init__.py
│   │   ├── planet_preview_widget.py    # OpenGL viewer to watch the planet as it is generated.
│   │   ├── planet_control_panel.py     # Planet creation options widget
│   │   ├── planet_geometry_panel.py    # Planet summary widget (radius, surface area, circumference, etc)
│   │   └── planet_view_controls.py     # OpenGL viewer options (wireframe, rotation, etc)
│   │
│   ├── __init__.py
│   ├── main_ui.py                  # Needs description
│   └── theme.py                    # Stylesheet for the UI screens.
│
├── __init__.py                     # Marks the root folder as a Python package
├── config.py                       # Global logging configuration (used across modules)
├── main.py                         # Starts the UI (calls ui.main_ui)
└── Status.md                       # Project planning, notes, and developer checklist
```

---

## Methodology

### Logging System

The project uses a custom logger defined in `logger/logger.py`.
See `config.py` for:
- Log level (`LOG_LEVEL`)
- Whether to log to console or file (`LOG_TO_CONSOLE`, `LOG_TO_FILE`)
- File path, size limits, and retention policy

#### Usage
To use the logger in any file:
```python
from logger.logger import LoggerFactory
logger = LoggerFactory("MyModule").get_logger()
logger.info("Log message")
```
This ensures consistent formatting and routing to both console and file.

#### Developer Note
✅ **Always use `LoggerFactory` for logging** — do not use `print()` or `logging.basicConfig()`.
When continuing this project or sharing context in new sessions, always refer to this logging system.

### Mesh Data Format
`PlanetMesh.vertices` and `PlanetMesh.faces` are stored as NumPy arrays, not lists of tuples.
- This ensures efficient numerical operations but may require format-aware iteration when exporting or serializing.
- ⚠️ **Reminder**: NumPy is row-major, but OpenGL (and many viewers) may expect flat, interleaved vertex buffers. Always double-check the order of `vertices` and `faces` when passing data to shaders or rendering libraries.
- This ensures efficient numerical operations but may require format-aware iteration when exporting or serializing.

### Save File Format
Mesh save/load operations use JobLib (compress=3) instead of pickle.
- This reduces file size and improves speed, but requires using joblib.load() and joblib.dump() to avoid compatibility issues.

---

## Workflows

### Planet Generation

The `generate_planet.py` script coordinates procedural world generation. Below is the current workflow:

1. **Load Configuration**  
   Loads the `planet_radius` and `subdivisions` from `planet_config.py`. These define the planet's scale and mesh detail.

2. **Generate Icosphere Mesh**  
   Constructs a base icosahedron and recursively subdivides its faces to create a near-uniform spherical mesh. Outputs a list of vertices and triangle faces.

3. **Validate Vertex Distances**  
   Ensures all vertices lie on the intended spherical surface by checking distance to the origin. Logs warnings for any significant deviations.

4. **Build Face Adjacency Map**  
   Maps each triangle face to its neighbors by shared edges. This is useful for simulating tectonic movement, biome propagation, and pathfinding.

5. **Compute Face Geometry**  
   For each triangle face, calculates:
   - **Center** (geometric centroid)
   - **Normal vector** (surface orientation)
   - **Area** (in square kilometers)
   - **Slope** (in degrees from vertical)
   - **Latitude & Longitude** (derived from center)

6. **Summarize Mesh Geometry**  
   Calculates and logs high-level stats, including:
   - Planet radius and circumference
   - Ideal and actual surface area
   - Average triangle size and variation
   - Estimated hex-tile and pentagon-tile area equivalents

Each step builds on the last, with results logged to both console and UTF-8 rotating log file.
