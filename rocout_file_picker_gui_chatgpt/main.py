import eel
from dataclasses import dataclass
from pathlib import Path

# Tkinter is in the Python standard library
import tkinter as tk
from tkinter import filedialog


@dataclass
class ProjectIdentity:
    """
    Why a class here?
    - Because you're modeling a "thing" (a project's identity/state) that will grow over time.
    - This keeps your project-related state in one place instead of scattered globals.
    """
    model_directory: str | None = None


project_identity = ProjectIdentity()


@eel.expose
def choose_model_directory() -> str | None:
    """
    Called from the GUI.
    Opens a native folder selection dialog and returns the chosen path (or None if canceled).
    """
    root = tk.Tk()
    root.withdraw()  # Hide the empty Tk window
    root.attributes("-topmost", True)  # Try to keep the dialog above the browser window

    folder = filedialog.askdirectory(title="Select ROCETS Model Root Directory")

    root.destroy()

    if not folder:
        return None

    # Normalize the path (nice-to-have, helps avoid path weirdness)
    folder_path = str(Path(folder).resolve())

    # Store it in your "ProjectIdentity" object
    project_identity.model_directory = folder_path

    print(f"[ProjectIdentity] model_directory set to: {project_identity.model_directory}")
    return folder_path


def main():
    eel.init("web")
    eel.start("index.html", size=(900, 500))


if __name__ == "__main__":
    main()
