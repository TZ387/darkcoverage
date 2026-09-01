# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this project is

DarkCoverage is a small PySide6 desktop GUI app for measuring dark/light
coverage of images against a configurable threshold grid. It has three
windows (main window, sliders window, reference window) built from plain
Qt widgets, plus a pure image-processing function.

- `src/darkcoverage/main.py` — entry point (`QApplication` bootstrap).
- `src/darkcoverage/gui.py` — main window (`ImageThresholdApp`): image
  loading/saving, coordinating the other two windows, triggering
  reprocessing.
- `src/darkcoverage/image_processing.py` — `process_image(...)`, a pure
  NumPy/Pillow function with no Qt dependency. This is the easiest part of
  the codebase to unit-test in isolation.
- `src/darkcoverage/widgets/` — `ImageLabel` (custom `QLabel` that paints
  the threshold grid overlay), `SlidersWindow`, `ReferenceWindow`.
- `tests/` — unit tests for `image_processing.py` (no Qt dependency) and
  for `SlidersWindow`'s grid-resize/threshold-collection logic (needs a
  headless Qt app; `conftest.py` provides a session-scoped `qapp` fixture
  for that — see its docstring). `gui.py`, `ImageLabel`, and
  `ReferenceWindow` are still not covered by automated tests — see
  "Testing GUI changes without a display" below for how to verify those
  manually.

## Environment / commands

This project uses `uv`.

- Install deps: `uv sync` (this also installs the `dev` dependency
  group, which currently just holds `pytest`)
- Run the app: `uv run python -m darkcoverage.main`
- Run tests: `uv run pytest`
- Lint/format: `uv run ruff check .` / `uv run ruff format .`
  (ruff is available but not currently pinned as a project dependency —
  don't assume a specific version is guaranteed across machines)

Tests run automatically on every push/PR via
`.github/workflows/tests.yml` (GitHub Actions, `uv sync` + `uv run
pytest` on `ubuntu-latest`). Keep new pure-logic code (i.e. anything
that doesn't need Qt) covered by tests in `tests/` so CI actually
catches regressions — `process_image` in `image_processing.py` is the
existing example to follow.

## Testing GUI changes without a display

This is a Qt GUI app, so it can't just be `import`ed and asserted on in
the usual way — but it *can* be exercised headlessly for verification,
which is the preferred way to check a change actually works before
calling it done:

```bash
QT_QPA_PLATFORM=offscreen uv run python - <<'EOF'
from PySide6.QtWidgets import QApplication
from darkcoverage.gui import ImageThresholdApp
from PIL import Image

app = QApplication([])
window = ImageThresholdApp()

img = Image.open("Example.jpg")
window.original_image = img.convert("L")
window.current_image = window.original_image.copy()
window.scale_image()
window.process_image()
print(window.total_result_label.text())
EOF
```

`Example.jpg` in the repo root is a ready-made sample image for this.
For widget-level checks (e.g. `ImageLabel` paint logic), instantiate the
widget directly, set a pixmap, and call `.grab()` to force `paintEvent`
to run.

## Conventions

- Commit messages: short, imperative, plain sentences (see `git log`).
  No conventional-commit prefixes (`feat:`, `fix:`, etc.) are used in
  this repo's history — don't introduce them unless asked.
- The repo owner commits their own changes after reviewing them. Don't
  run `git add`/`git commit` unless explicitly asked to — instead,
  propose a one-line commit message suggestion (in the style above) and
  let them commit it themselves.
- Keep changes minimal and behavior-preserving unless asked otherwise;
  this is a small hobby-scale project, not a place for speculative
  abstractions or new dependencies.
- Don't commit `__pycache__/` or `.venv/` (already gitignored).
