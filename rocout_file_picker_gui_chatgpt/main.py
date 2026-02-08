from __future__ import annotations

import os
import socket
import threading
import time
from dataclasses import dataclass
from typing import Optional

import eel

# Only import pywebview if we need it (keeps dependencies optional in the future)
try:
    import webview  # pywebview
except Exception:
    webview = None


# -------------------------
# Config / Settings
# -------------------------

@dataclass(frozen=True)
class AppConfig:
    web_dir: str = "web"
    start_page: str = "index.html"

    # Toggle: external Edge app-mode vs embedded pywebview
    use_embedded_webview: bool = True

    # If port is None, we auto-pick a free one (recommended for dev)
    port: Optional[int] = None
    host: str = "127.0.0.1"

    # Window sizing
    width: int = 1200
    height: int = 800

    # Set to True if you want devtools later (optional)
    enable_devtools: bool = False


# -------------------------
# Helpers
# -------------------------

def find_edge_exe() -> str:
    """Find Edge executable in common install locations."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    raise RuntimeError("Edge not found (unexpected on Windows).")


def pick_free_port(host: str) -> int:
    """Pick an unused TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))
        return int(s.getsockname()[1])


def wait_for_server(host: str, port: int, timeout_s: float = 5.0) -> None:
    """
    Wait until a TCP connection to (host, port) succeeds.
    This avoids pywebview opening a blank page before Eel is listening.
    """
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.25):
                return
        except OSError:
            time.sleep(0.05)
    raise TimeoutError(f"Eel server did not start listening on {host}:{port} within {timeout_s}s")


# -------------------------
# Launch paths
# -------------------------

def start_with_external_edge(config: AppConfig) -> None:
    """
    Normal Eel flow: start server + open Edge in app-mode.
    """
    eel.init(config.web_dir)

    # Tell Eel where Edge is (best-effort; some Eel versions may still use `start msedge`)
    try:
        eel.browsers.set_path("edge", find_edge_exe())
    except Exception:
        # Not fatal; Eel might still be able to launch Edge via `msedge`
        pass

    eel.start(
        config.start_page,
        host=config.host,
        port=config.port or 0,  # 0 lets Eel auto-pick
        mode="edge",
        cmdline_args=[
            "--app={url}",
            f"--window-size={config.width},{config.height}",
            "--disable-features=TranslateUI",
            "--no-first-run",
            "--disable-sync",
        ],
    )


def start_with_embedded_webview(config: AppConfig) -> None:
    """
    Start Eel WITHOUT opening a browser, then open a pywebview window to the local URL.
    """
    if webview is None:
        raise RuntimeError("pywebview is not installed or failed to import.")

    eel.init(config.web_dir)

    # Choose a deterministic port (pywebview needs a URL to load)
    port = config.port or pick_free_port(config.host)
    url = f"http://{config.host}:{port}/{config.start_page}"

    # Start Eel server in a background thread (non-blocking)
    def run_eel():
        eel.start(
            config.start_page,
            host=config.host,
            port=port,
            block=True,     # keep server running in this thread
            mode=None,      # IMPORTANT: don't open an external browser
        )

    t = threading.Thread(target=run_eel, daemon=True)
    t.start()

    # Wait until server is reachable before opening the window
    wait_for_server(config.host, port, timeout_s=10.0)

    # Create the native window
    window = webview.create_window(
        title="ROCout",
        url=url,
        width=config.width,
        height=config.height,
    )

    # Start pywebview loop (blocks until window closes)
    # NOTE: debug/devtools varies by platform/backend; keep False for now.
    webview.start(debug=config.enable_devtools)


def start_app(config: Optional[AppConfig] = None) -> None:
    config = config or AppConfig()

    print("🚀 ROCout starting...")
    print(f"   Embedded webview: {config.use_embedded_webview}")

    if config.use_embedded_webview:
        start_with_embedded_webview(config)
    else:
        start_with_external_edge(config)


if __name__ == "__main__":
    start_app()
