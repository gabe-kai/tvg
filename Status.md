# Project Status

`\Status.md`

This file is intended to help ChatGPT (and me) remember where we are in the project, and to get quickly caught up when it's time to start a new conversation.

---

## Daily Commit Summaries

---

## In-Progress

We are rebuilding the old progress as Object Oriented Programming with a logging/debugging-first ideology.

---

## ToDo

---

## File & Folder Structure
```
tvg/
├── .venv/                      # Virtual environment (auto-managed by PyCharm)
├── __init__.py                 # Marks the root folder as a Python package
├── config.py                   # Global logging configuration (used across modules)
├── main.py                     # Entry point for launching the application
├── Status.md                   # Project planning, notes, and developer checklist
│
├── logger/                     # Centralized logging tools
│   ├── __init__.py             # Marks as a package
│   └── logger.py               # LoggerFactory with color output and rotating file handler
│
├── logs/                       # Auto-created directory for logs
│   └── tvg.log                 # Output file for logs (rotated based on config)
│
├── planet_generator/           # Main planetary generation module
│   ├── __init__.py             # Marks as a package
│   ├── planet_config.py        # User-editable settings for world generation
│   ├── generate_planet.py      # Orchestrates full generation process
│   │
│   ├── geometry/               # Planetary mesh generation and spatial data
│   │   ├── __init__.py         # Marks as a package
│   │   ├── icosphere.py        # Builds and subdivides an icosahedral sphere mesh
│   │   ├── adjacency.py        # Calculates which faces share edges
│   │   └── face_geometry.py    # Computes face centers, normals, area, slope, and lat/lon
│   │
│   ├── planet_utils/           # Shared utility methods for geometry/topology
│   │   ├── __init__.py         # Marks as a package
│   │   └── mesh_tools.py       # Mesh inspection tools (e.g. vertex distance checks)
```

---

## Logging System

The project uses a custom logger defined in `logger/logger.py`.
See `config.py` for:
- Log level (`LOG_LEVEL`)
- Whether to log to console or file (`LOG_TO_CONSOLE`, `LOG_TO_FILE`)
- File path, size limits, and retention policy

### Usage
To use the logger in any file:
```python
from logger.logger import LoggerFactory
logger = LoggerFactory("MyModule").get_logger()
logger.info("Log message")
```
This ensures consistent formatting and routing to both console and file.

### Developer Note
✅ **Always use `LoggerFactory` for logging** — do not use `print()` or `logging.basicConfig()`.
When continuing this project or sharing context in new sessions, always refer to this logging system.

---

## Workflows

### Planet Generation