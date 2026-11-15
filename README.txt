SERENUM PYTHON RUNTIME FIX

This patch makes the setup program automatically relaunch itself under Python 3.12, 3.11, or 3.10. It prefers 3.12 and does not trust the first `python`/`pythonw` found on PATH. Python 3.14 can remain installed.

REPLACE THESE FILES IN YOUR INSTALLED SERENUM FOLDER:
- serenum_setup.pyw
- serenum_updater.pyw
- Install_Serenum.vbs
- Start_Serenum.vbs
- Update_Serenum.vbs
- Start_Serenum.bat (optional diagnostic launcher)
- serenum.bat (optional legacy launcher)

Also replace the same installer/launcher files in the extracted installer package you use for future installations, so old copies do not overwrite the fix. Keep your existing serenum.py and all data/configuration folders unchanged.

The main Serenum application currently imports `imghdr`, which was removed in Python 3.13. This patch intentionally keeps the supported runtime range at Python 3.10-3.12 rather than pretending Python 3.14 is compatible.

After replacing files, run Start_Serenum.vbs. The setup log should report Python 3.12.x (or 3.11.x/3.10.x) and show the selected executable path.
