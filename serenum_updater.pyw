# -*- coding: utf-8 -*-
"""Serenum desktop updater: find newest Downloads/serenum.py and reinstall safely."""
from __future__ import annotations

import ast
import os
import queue
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

APP_NAME = "Serenum"
INSTALL_DIR = Path(r"C:\xampp\htdocs\AI automation\serenum")
SETUP_SCRIPT = INSTALL_DIR / "serenum_setup.pyw"
SKIP_DIRS = {
    "__pycache__", ".git", ".venv", "venv", "env", "site-packages",
    "node_modules", "build", "dist", "_update_backups", "temp", "tmp",
}


def get_downloads_folder() -> Path:
    """Resolve the actual Windows Downloads known folder, with a safe fallback."""
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _kind = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")
            expanded = os.path.expandvars(value)
            candidate = Path(expanded).expanduser()
            if candidate.is_dir():
                return candidate
    except Exception:
        pass
    profile = Path(os.environ.get("USERPROFILE", str(Path.home())))
    for candidate in (profile / "Downloads", Path.home() / "Downloads"):
        if candidate.is_dir():
            return candidate
    return profile / "Downloads"


def is_valid_serenum_script(path: Path) -> tuple[bool, str]:
    try:
        if not path.is_file() or path.name.casefold() != "serenum.py":
            return False, "Not the expected serenum.py file."
        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source, filename=str(path))
        names = {
            node.name for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }
        required = {"execute_engine", "SerenumApp"}
        missing = sorted(required - names)
        if missing:
            return False, "The script does not contain the expected Serenum application components: " + ", ".join(missing)
        if len(source) < 100_000:
            return False, "The script is unexpectedly small and may be incomplete."
        return True, "Valid Serenum application script."
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def _stamp(path: Path) -> tuple[int, int, int]:
    """Use directory creation/modify time to identify the newest extracted folder."""
    try:
        folder = path.parent.stat()
    except OSError:
        folder = path.stat()
    file_stat = path.stat()
    folder_created = int(getattr(folder, "st_birthtime", folder.st_ctime) * 1_000_000_000)
    file_created = int(getattr(file_stat, "st_birthtime", file_stat.st_ctime) * 1_000_000_000)
    return (max(folder_created, file_created), int(file_stat.st_mtime_ns), int(file_stat.st_size))


def find_latest_download_script(progress=None) -> tuple[Path | None, int]:
    downloads = get_downloads_folder()
    if not downloads.is_dir():
        return None, 0
    matches: list[Path] = []
    scanned = 0
    for root, dirs, files in os.walk(downloads, topdown=True):
        dirs[:] = [
            d for d in dirs
            if d.casefold() not in SKIP_DIRS
            and not d.startswith(".")
            and not d.casefold().endswith(".zip")
        ]
        scanned += 1
        if progress and scanned % 25 == 0:
            progress(scanned)
        folder = Path(root)
        # Only consider real extracted directories whose own name includes Serenum.
        if "serenum" not in folder.name.casefold():
            continue
        for filename in files:
            if filename.casefold() == "serenum.py":
                candidate = folder / filename
                # Exclude the installed production script if Downloads was redirected there.
                try:
                    if os.path.normcase(str(candidate.resolve())) == os.path.normcase(str((INSTALL_DIR / "serenum.py").resolve())):
                        continue
                except Exception:
                    pass
                valid, _reason = is_valid_serenum_script(candidate)
                if valid:
                    matches.append(candidate)
    if not matches:
        return None, scanned
    matches.sort(key=_stamp, reverse=True)
    return matches[0], scanned


def running_serenum_processes() -> list:
    """Return running app/worker processes that reference the installed serenum.py."""
    try:
        import psutil
    except Exception:
        return []
    target = os.path.normcase(str((INSTALL_DIR / "serenum.py").resolve()))
    found = []
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if proc.pid in (os.getpid(), os.getppid()):
                continue
            cmdline = proc.info.get("cmdline") or []
            joined = " ".join(str(v) for v in cmdline)
            if not joined:
                continue
            normalized = os.path.normcase(joined)
            if target in normalized and "serenum_updater.pyw" not in normalized:
                found.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found


def stop_running_serenum(processes: list) -> tuple[bool, str]:
    try:
        import psutil
    except Exception:
        return False, "The process-control library is unavailable. Close Serenum manually, then retry the update."
    all_processes = {}
    for proc in processes:
        try:
            all_processes[proc.pid] = proc
            for child in proc.children(recursive=True):
                all_processes[child.pid] = child
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    items = list(all_processes.values())
    for proc in items:
        try:
            proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    _gone, alive = psutil.wait_procs(items, timeout=7)
    for proc in alive:
        try:
            proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    _gone2, alive2 = psutil.wait_procs(alive, timeout=4)
    if alive2:
        return False, "Serenum is still running. Close it manually and click Update Serenum again."
    return True, "Previous Serenum session closed safely."


class UpdaterWindow:
    BG = "#07111F"
    PANEL = "#0D1B2D"
    BORDER = "#245276"
    TEXT = "#EAF5FF"
    MUTED = "#9BB4C9"
    CYAN = "#29C9F5"
    GREEN = "#31D58A"
    RED = "#FF6C83"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.events: queue.Queue = queue.Queue()
        self.latest: Path | None = None
        self.scanning = False
        self.installing = False
        self.root.title("Serenum • Update Center")
        self.root.configure(bg=self.BG)
        self.root.geometry("660x470")
        self.root.resizable(False, False)
        self._center()
        self._build()
        self.root.after(100, self._poll)
        self.root.after(250, self.scan)

    def _center(self):
        self.root.update_idletasks()
        w, h = 660, 470
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=24, pady=22)
        head = tk.Frame(outer, bg=self.BG)
        head.pack(fill="x")
        tk.Label(head, text="S", bg="#073A5B", fg=self.CYAN, font=("Segoe UI", 25, "bold"), width=2).pack(side="left", padx=(0, 12))
        titlebox = tk.Frame(head, bg=self.BG)
        titlebox.pack(side="left")
        tk.Label(titlebox, text="UPDATE SERENUM", bg=self.BG, fg=self.TEXT, font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(titlebox, text="DESKTOP APPLICATION INSTALLER", bg=self.BG, fg=self.MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        panel = tk.Frame(outer, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        panel.pack(fill="both", expand=True, pady=(22, 15))
        self.status = tk.Label(panel, text="SEARCHING DOWNLOADS", bg=self.PANEL, fg=self.CYAN, font=("Segoe UI", 11, "bold"))
        self.status.pack(anchor="w", padx=20, pady=(20, 8))
        self.message = tk.Label(panel, text="Looking for the newest extracted Serenum folder. ZIP files are ignored.", bg=self.PANEL, fg=self.TEXT, font=("Segoe UI", 10), wraplength=570, justify="left")
        self.message.pack(anchor="w", padx=20, pady=(0, 14))
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Updater.Horizontal.TProgressbar", troughcolor="#173049", background=self.GREEN, bordercolor="#173049", thickness=12)
        self.progress = ttk.Progressbar(panel, style="Updater.Horizontal.TProgressbar", mode="determinate", maximum=100)
        self.progress.pack(fill="x", padx=20, pady=(0, 9))
        self.detail = tk.Label(panel, text="", bg=self.PANEL, fg=self.MUTED, font=("Segoe UI", 9), wraplength=570, justify="left")
        self.detail.pack(anchor="w", padx=20)
        self.folder_label = tk.Label(panel, text="", bg=self.PANEL, fg=self.CYAN, font=("Segoe UI", 10, "bold"), wraplength=570, justify="left")
        self.folder_label.pack(anchor="w", padx=20, pady=(13, 0))
        foot = tk.Frame(outer, bg=self.BG)
        foot.pack(fill="x")
        self.cancel_button = tk.Button(foot, text="CANCEL", command=self.root.destroy, bg="#1A2A3D", fg=self.MUTED, activebackground="#263D55", activeforeground=self.TEXT, relief="flat", padx=18, pady=11, font=("Segoe UI", 9, "bold"), cursor="hand2")
        self.cancel_button.pack(side="right")
        self.update_button = tk.Button(foot, text="SEARCHING…", command=self.confirm_update, state="disabled", bg="#0A704A", fg="white", activebackground="#0D8A5D", relief="flat", padx=20, pady=11, font=("Segoe UI", 9, "bold"), cursor="hand2")
        self.update_button.pack(side="right", padx=(0, 10))

    def scan(self):
        if self.scanning or self.installing:
            return
        self.scanning = True
        self.status.configure(text="SEARCHING DOWNLOADS", fg=self.CYAN)
        self.message.configure(text="Searching Downloads for the newest extracted folder with “serenum” in its name and a valid serenum.py. ZIP files are ignored.")
        self.progress.configure(value=5)
        self.update_button.configure(text="SEARCHING…", state="disabled")

        def on_progress(count):
            self.events.put(("progress", count))

        def run():
            try:
                candidate, scanned = find_latest_download_script(on_progress)
                self.events.put(("scan_done", candidate, scanned, None))
            except Exception as exc:
                self.events.put(("scan_done", None, 0, f"{type(exc).__name__}: {exc}"))
        threading.Thread(target=run, daemon=True).start()

    def _scan_finished(self, candidate: Path | None, scanned: int, error: str | None):
        self.scanning = False
        self.progress.configure(value=100)
        if error:
            self.status.configure(text="SEARCH COULD NOT BE COMPLETED", fg=self.RED)
            self.message.configure(text="Serenum could not search Downloads. Check folder access, then try again.")
            self.detail.configure(text=error)
            self.update_button.configure(text="RESCAN DOWNLOADS", state="normal", command=self.scan)
            return
        if candidate is None:
            self.latest = None
            self.status.configure(text="NO SERENUM UPDATE FOUND", fg=self.RED)
            self.message.configure(text="No valid serenum.py was found in your Downloads folders. Download and extract the latest Serenum package, then click Rescan Downloads.")
            self.detail.configure(text=f"Folders checked: {scanned}")
            self.folder_label.configure(text="")
            self.update_button.configure(text="RESCAN DOWNLOADS", state="normal", command=self.scan)
            return
        self.latest = candidate
        valid, reason = is_valid_serenum_script(candidate)
        if not valid:
            self._scan_finished(None, scanned, reason)
            return
        stat = candidate.stat()
        modified = time.strftime("%d %b %Y • %H:%M", time.localtime(stat.st_mtime))
        self.status.configure(text="LATEST SERENUM UPDATE FOUND", fg=self.GREEN)
        self.message.configure(text="The newest valid Serenum application script is ready. Confirm below to replace the installed application and refresh the desktop shortcuts.")
        self.detail.configure(text=f"Source folder: {candidate.parent.name}\nScript modified: {modified} • Size: {stat.st_size / (1024 * 1024):.2f} MB")
        self.folder_label.configure(text="Your author configuration, images, and working folders will be preserved.")
        self.update_button.configure(text="INSTALL LATEST UPDATE", state="normal", command=self.confirm_update)

    def confirm_update(self):
        if not self.latest or self.installing:
            self.scan()
            return
        processes = running_serenum_processes()
        if processes:
            yes = messagebox.askyesno(
                "Close Serenum before updating?",
                "Serenum is currently open. Updating will close the application and stop any active operation. Your saved author configuration and working files will be preserved. Continue?",
                parent=self.root,
            )
            if not yes:
                return
            ok, result = stop_running_serenum(processes)
            if not ok:
                messagebox.showerror("Could not close Serenum", result, parent=self.root)
                return
        yes = messagebox.askyesno(
            "Confirm Serenum update",
            "Install the newest valid serenum.py found in Downloads?\n\nThe existing application script will be backed up and replaced. Desktop shortcuts and setup components will be refreshed. Your author configuration and working data will not be removed.",
            parent=self.root,
        )
        if not yes:
            return
        self.installing = True
        self.update_button.configure(text="INSTALLING…", state="disabled")
        self.cancel_button.configure(state="disabled")
        self.status.configure(text="PREPARING UPDATE", fg=self.GREEN)
        self.message.configure(text="Starting the Serenum installer. It will verify the Python environment and required libraries before opening the updated desktop application.")
        self.progress.configure(value=20, mode="indeterminate")
        self.progress.start(12)
        try:
            if not SETUP_SCRIPT.is_file():
                raise FileNotFoundError("The installed Serenum setup program is missing. Run Install_Serenum.vbs from the complete installer ZIP first.")
            env = os.environ.copy()
            env["SERENUM_SOURCE_SCRIPT"] = str(self.latest.resolve())
            env["SERENUM_UPDATE_MODE"] = "1"
            env["PYTHONIOENCODING"] = "utf-8"
            # sys.executable is pythonw.exe because this updater is launched quietly.
            subprocess.Popen(
                [sys.executable, "-X", "utf8", str(SETUP_SCRIPT)],
                cwd=str(INSTALL_DIR), env=env,
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                close_fds=True,
            )
            self.status.configure(text="UPDATE INSTALLER STARTED", fg=self.GREEN)
            self.message.configure(text="The update setup window is now checking and installing the selected version. This window will close.")
            self.root.after(1000, self.root.destroy)
        except Exception as exc:
            self.installing = False
            self.progress.stop()
            self.status.configure(text="UPDATE COULD NOT START", fg=self.RED)
            self.message.configure(text="The update installer could not be opened. Review the detail below and retry.")
            self.detail.configure(text=f"{type(exc).__name__}: {exc}")
            self.update_button.configure(text="RETRY UPDATE", state="normal", command=self.confirm_update)
            self.cancel_button.configure(state="normal")

    def _poll(self):
        try:
            while True:
                item = self.events.get_nowait()
                if item[0] == "progress":
                    count = item[1]
                    self.message.configure(text=f"Searching Downloads… checked {count} folders so far.")
                elif item[0] == "scan_done":
                    _, candidate, scanned, error = item
                    self._scan_finished(candidate, scanned, error)
        except queue.Empty:
            pass
        if self.root.winfo_exists():
            self.root.after(120, self._poll)


def main():
    if sys.platform != "win32":
        raise SystemExit("The Serenum desktop updater is designed for Windows.")
    root = tk.Tk()
    UpdaterWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
