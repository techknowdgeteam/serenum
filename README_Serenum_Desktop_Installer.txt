SERENUM DESKTOP INSTALLER & ONE-CLICK UPDATER
============================================

WHAT THIS INSTALLS
------------------
- A Serenum desktop shortcut that opens the application through the quiet setup checker.
- An Update Serenum desktop shortcut that searches Downloads for the newest extracted folder
  containing a valid serenum.py, asks you to confirm, then safely replaces the installed script.
- The complete Serenum desktop UI (the current serenum.py is the application).
- The setup/dependency checker, quiet VBScript launchers, cover animation and fallback cover.

FIRST INSTALLATION
------------------
1. Extract this complete ZIP package to a normal folder (Downloads is fine).
2. Double-click Install_Serenum.vbs.
3. A Serenum setup window opens. It creates the required application folders, prepares the
   cover at C:\xampp\htdocs\AI automation\ai cover\ai cover.gif, checks Python imports,
   installs missing third-party packages in the background, and validates the script.
4. When setup succeeds, Serenum opens and two shortcuts are created on the Windows Desktop:
   - Serenum
   - Update Serenum

DAILY LAUNCH
------------
Double-click the Serenum desktop shortcut. It performs the quick dependency/import verification
in a green progress window and opens the main Serenum interface when checks pass. No Command
Prompt window is opened.

UPDATING FROM DOWNLOADS
-----------------------
1. Download and extract the newest Serenum update into Downloads (or any subfolder under it).
2. Make sure the extracted folder contains a file named exactly serenum.py.
3. Double-click Update Serenum on the Desktop.
4. The updater scans Downloads recursively (skipping cache/build/virtual-environment folders),
   validates candidate serenum.py files and selects the newest matching extracted folder.
5. Confirm INSTALL LATEST UPDATE.
6. If Serenum is running, the updater asks permission to close it and stop its active operation.
7. The current installed script is backed up under the installation's _update_backups folder,
   the selected serenum.py is installed, setup/support components are refreshed when included,
   imports are verified and the desktop shortcuts are refreshed.
8. The updated Serenum window opens only after setup succeeds.

SAFE REINSTALL BEHAVIOUR
------------------------
The installed application entrypoint and launcher/setup components are replaced safely. Existing
pageandgroupauthors.json, files, jpgfolders, captions, images and other working data are preserved.
The old serenum.py is retained as a dated rollback copy under _update_backups. Python packages
are repaired/installed only as required; the updater does not uninstall Python itself.

REQUIREMENTS / LIMITATIONS
--------------------------
- Windows 10/11.
- Python 3.10, 3.11 or 3.12 for Windows, installed with Tcl/Tk support (pythonw.exe).
- Internet access is needed only when required third-party packages are missing or need repair.
- The installer does not install Python itself. If Python is absent, install Python for Windows
  with Tcl/Tk enabled, then run Install_Serenum.vbs again.
- The updater searches extracted folders in the Windows Downloads known folder. It does not
  extract ZIP archives automatically and does not search unrelated folders outside Downloads.

QUIET LAUNCH
------------
All VBS launchers start pythonw.exe and hidden setup subprocesses. They do not open Command Prompt.

USER DATA
---------
The installer does not delete or overwrite your existing author JSON, images or working folders.
