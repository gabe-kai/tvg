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
│   ├── exports/                    # Storage for exported files (e.g., OBJ, GLTF) for use outside the app
│   └── planets/                    # Folder-based save directories for each generated planet (one folder per planet)
│
├── logger/                         # Centralized logging tools
│   ├── __init__.py
│   └── logger.py                   # LoggerFactory with color output and rotating file handler
│
├── logs/                           # Auto-created log output directory
│   └── tvg.log                     # Output file for logs (rotated based on config settings in config.py)
│
├── planet_generator/               # All backend logic for planet generation, geometry, and persistence
│   ├── exporters/
│   │   ├── __init__.py
│   │   └── export_planet.py        # Exports a PlanetMesh to OBJ format for 3D visualization (# TODO: Add .blend or GLTF export)
│   │
│   ├── geometry/                   # Geometry creation and spatial data tools
│   │   ├── __init__.py
│   │   ├── adjacency.py            # Calculates face adjacency (neighbors by shared edges)
│   │   ├── face_geometry.py        # Computes face centers, normals, area, slope, latitude & longitude
│   │   └── icosphere.py            # Builds and recursively subdivides an icosahedral sphere mesh
│   │
│   ├── io/                         # Planet save/load system using the Planet wrapper class
│   │   ├── __init__.py
│   │   └── planet_io.py            # Defines the Planet wrapper and handles folder-based save/load with joblib and metadata
│   │
│   ├── planet_utils/               # Helper utilities for geometry, inspection, and debugging
│   │   ├── __init__.py
│   │   └── mesh_tools.py           # Utilities for validating mesh geometry and summarizing mesh statistics
│   │
│   ├── __init__.py
│   ├── generate_planet.py          # CLI entry point for full procedural planet generation
│   ├── planet_config.py            # Default planet configuration settings (e.g. radius, subdivisions)
│   └── planet_mesh.py              # PlanetMesh class that stores mesh data, face geometry, and adjacency map
│
├── ui/                             # PySide6-based GUI implementation
│   ├── components/                 # (Reserved for) complex, reusable UI components that aren't atomic widgets
│   │   └── __init__.py
│   │
│   ├── screens/                    # Top-level screens / views (Welcome, PlanetGen, etc)
│   │   ├── __init__.py
│   │   ├── planetgen.py            # Layout and logic for the planet generation screen and preview display
│   │   └── welcome.py              # The game's welcome screen (new game, load game, settings, about, quit)
│   │
│   ├── state/                      # Centralized state manager for controlling screen transitions
│   │   ├── __init__.py
│   │   └── ui_state_manager.py     # Manages transitions between UI states (welcome → planetgen → editor, etc)
│   │
│   ├── tests/                      # Self-contained OpenGL and UI test files
│   │   └── test_opengl_widget.py   # Test harness for debugging OpenGL rendering in isolation
│   │
│   ├── widgets/                    # Reusable UI widgets, composable in screens or other widgets
│   │   ├── __init__.py
│   │   ├── planet_preview_widget.py    # OpenGL viewer that renders the planet from a saved mesh file
│   │   ├── planet_control_panel.py     # Sidebar for planet parameters (name, seed, radius, subdivisions)
│   │   ├── planet_geometry_panel.py    # Summary panel for mesh geometry stats (area, tile sizes, etc)
│   │   └── planet_view_controls.py     # Viewer overlay for toggling wireframe mode and other view settings
│   │
│   ├── __init__.py
│   ├── main_ui.py                  # Entry point for launching the main GUI application and its screens
│   └── theme.py                    # Central stylesheet and theming setup for PySide6 widgets and layouts
│
├── __init__.py                     # Marks project root as a package
├── config.py                       # Global logging and configuration settings
├── main.py                         # Application entry point — initializes and launches the main UI
├── requirements.txt                # Python dependencies (PySide6, numpy, OpenGL, joblib, etc.)
└── Status.md                       # Project planning, TODOs, dev notes, and daily status summaries

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
