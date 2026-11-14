SERENUM — COMPLETE AUTOMATIC INSTALL / UPDATE PACKAGE
======================================================

Included files
--------------
serenum.py                 Main Serenum application
serenum_setup.pyw          Installer and environment verifier
serenum_updater.pyw        Downloads scanner and updater
Install_Serenum.vbs        Installer launcher
Start_Serenum.vbs          Main application launcher
Update_Serenum.vbs         Updater launcher
Start_Serenum.bat          Diagnostic command-prompt launcher
serenum.bat                Legacy command-prompt launcher

Install / update behavior
-------------------------
1. Extract the complete ZIP into a folder.
2. Run Install_Serenum.vbs for installation or repair.
3. Run Update_Serenum.vbs for an update.
4. Both actions look in the user's Downloads folder for the newest extracted
   folder whose name contains “serenum” and which contains a valid serenum.py.
5. ZIP files are not opened or treated as extracted folders.
6. The complete contents of the selected extracted folder are copied into:
   C:\xampp\htdocs\AI automation\serenum
   Existing files with matching names are overwritten. Python cache and Git
   metadata folders are skipped; other files and subfolders are copied.
7. The previous installed serenum.py is backed up before it is replaced.

UI behavior
-----------
- Installer and main Serenum retain normal Windows minimize, maximize, and close
  controls. Their native title bars are requested in the same dark colors as
  their respective window surfaces.
- Main Serenum's COMMAND DECK scrolls vertically. Configuration remains pinned
  at the top of that panel.
- The main console and JSON editor use non-white Serenum-themed scrollbars.
- The JSON editor keeps both vertical and horizontal scrolling so long lines
  remain accessible; the Command Deck itself has vertical scrolling only.
- Configuration and live console continue to display inside the main window.
  Their BACK TO HOME buttons return to the Serenum cover.

Requirements / notes
--------------------
- Windows with Python 3.10, 3.11, or 3.12 and Tcl/Tk.
- Setup installs/verifies the Python imports required by serenum.py.
- Native Windows title-bar colors depend on Windows DWM support. On unsupported
  Windows builds the program falls back to the system title-bar rendering.
- Python syntax checks and ZIP integrity tests are performed on this package.
  A full Windows GUI and dependency-install test cannot be performed in this
  non-Windows environment.
