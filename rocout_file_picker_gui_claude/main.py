"""
main.py — Minimal Eel backend for the "New Project" workflow.

WORKFLOW:
    1. Eel starts, serves the HTML/JS frontend
    2. User clicks "New Project" button in the GUI
    3. JavaScript calls eel.browse_for_model_directory()
    4. Python opens a native OS folder-picker dialog
    5. User navigates to the ROCETS model directory, clicks "Select Folder"
    6. Python receives the path, creates a ProjectIdentity, returns confirmation
    7. JavaScript updates the GUI to show the selected path

WHY tkinter FOR THE DIALOG?
    Eel runs a web-based GUI, but web browsers can't open native OS folder
    pickers (they can only do file uploads). So we borrow tkinter's
    filedialog — it's part of Python's standard library, requires zero
    extra installs, and gives us a proper native OS "Browse for Folder"
    dialog. We only use tkinter for this ONE thing; the actual GUI is
    still 100% Eel/HTML/CSS/JS.

WHY A SEPARATE MODULE IN PRODUCTION?
    In your real app, the browse function and ProjectIdentity creation
    would live in separate backend modules (separation of concerns).
    Here, everything is in one file for clarity. I'll note where the
    seams would be.
"""

import os
import eel
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any


# =============================================================================
# ProjectIdentity (same frozen dataclass from our earlier work)
# =============================================================================
# In your real app: `from project_identity import ProjectIdentity`

@dataclass(frozen=True)
class ProjectIdentity:
    """Immutable facts about a ROCETS project."""

    model_directory: Path
    project_name: str
    created_at: datetime

    def __post_init__(self):
        if isinstance(self.model_directory, str):
            object.__setattr__(self, "model_directory", Path(self.model_directory))

    @property
    def cfg_directory(self) -> Path:
        return self.model_directory / "config"

    @property
    def output_directory(self) -> Path:
        return self.model_directory / "output"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_directory": str(self.model_directory),
            "project_name": self.project_name,
            "created_at": self.created_at.isoformat(),
        }


# =============================================================================
# Module-level state
# =============================================================================
# In your real app, this would live in SessionState or an app controller.
# For this demo, a simple module-level variable keeps it minimal.

current_project: ProjectIdentity | None = None


# =============================================================================
# Eel-exposed backend functions
# =============================================================================

@eel.expose
def browse_for_model_directory():
    """
    Open a native OS folder-picker dialog and return the selected path.

    WHY a function (not a class method)?
        This is a one-shot action triggered by a GUI event — no state to
        manage between calls, no data to encapsulate. A plain function is
        the right tool here. It will eventually live in a utility module
        like `backend/dialogs.py`.

    Returns:
        dict with keys:
            - "success" (bool):  whether a folder was selected
            - "path" (str):      the selected directory path (or "")
            - "project_name" (str): derived project name (or "")
    """
    import tkinter as tk
    from tkinter import filedialog

    # --- Create and HIDE the tkinter root window ---
    # tkinter always needs a root window, but we don't want it visible.
    # withdraw() hides it immediately so the user only sees the dialog.
    root = tk.Tk()
    root.withdraw()

    # --- Bring the dialog to the front ---
    # Without this, the folder dialog can hide behind the Eel/Chrome window.
    root.attributes("-topmost", True)

    selected_path = filedialog.askdirectory(
        title="Select ROCETS Model Directory",
        # mustexist=True ensures user can only pick real directories
        mustexist=True,
    )

    # --- Clean up the hidden tkinter window ---
    root.destroy()

    if selected_path:
        return {
            "success": True,
            "path": selected_path,
            # Derive project name from the folder name (user can rename later)
            "project_name": Path(selected_path).name,
        }
    else:
        # User clicked Cancel
        return {
            "success": False,
            "path": "",
            "project_name": "",
        }


@eel.expose
def create_new_project(model_directory: str, project_name: str):
    """
    Create a ProjectIdentity from the user's selections.

    WHY a separate function from browse_for_model_directory()?
        Separation of concerns:
        - browse_for_model_directory() handles the OS dialog (UI concern)
        - create_new_project() handles data creation (business logic)

        This means you could later create a project from a config file,
        a recent-projects list, or a CLI — none of which need the browse
        dialog. Keeping them separate makes both reusable.

    Args:
        model_directory: Path string from the browse dialog
        project_name: Human-readable project name

    Returns:
        dict with the created project's data, or an error message
    """
    global current_project

    try:
        current_project = ProjectIdentity(
            model_directory=Path(model_directory),
            project_name=project_name,
            created_at=datetime.now(),
        )

        print(f"✅ Project created: {current_project.project_name}")
        print(f"   Model dir:  {current_project.model_directory}")
        print(f"   CFG dir:    {current_project.cfg_directory}")
        print(f"   Output dir: {current_project.output_directory}")

        return {
            "success": True,
            "project": current_project.to_dict(),
        }

    except Exception as e:
        print(f"❌ Error creating project: {e}")
        return {
            "success": False,
            "error": str(e),
        }


# =============================================================================
# App entry point
# =============================================================================
def find_edge() -> str:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    raise RuntimeError("Edge not found (unexpected).")


def start_app():
    """
    Initialize and launch the Eel application.

    WHY a function instead of bare code at module level?
        1. Testability — you can import this module without auto-launching
        2. Reusability — other scripts can call start_app() with different args
        3. Clean __main__ guard — standard Python best practice
    """
    eel.init("web")  # Point Eel at the web/ folder for frontend files

    edge = find_edge()

    # ✅ Tell Eel explicitly where Edge is
    eel.browsers.set_path("edge", edge)

    # edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    # if not os.path.exists(edge):
    #     edge = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    # if not os.path.exists(edge):
    #     raise RuntimeError("Edge not found (unexpected).")

    mode = f'"{edge}" --app={{url}} --window-size=1200,800'

    print("   Click 'New Project' in the GUI to get started.")
    # eel.start(
    #     "index.html",
    #     size=(900, 600),       # Initial window size
    #     port=0,                # Auto-pick an available port
    #     mode=mode,
    # )
    print("🚀 ROCETS GUI starting...")
    eel.start(
        "index.html",
        mode="edge",                 # ✅ must be a known mode name
        port=0,
        # ✅ flags go here
        cmdline_args=[
            "--app={url}",           # ✅ kills address bar/tabs/bookmarks
            "--window-size=1200,800",
            "--disable-features=TranslateUI",
        ],
        # ⚠️ OPTIONAL: remove size when using --app/--window-size (avoids confusion)
        # size=(900, 600),
    )


if __name__ == "__main__":
    start_app()
