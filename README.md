# DNAS Patcher GUI

The **DNAS Patcher GUI** is a graphical interface for the DNAS patcher, allowing you to modify **eeMemory.bin** files or ISOs conveniently, without using the command line.

---

## 🔹 Features

- Support for multiple operating modes:

- **1**: `sceDNAS2GetStatus` injection → fake deinit, error 0, status 5

- **2**: `sceDNAS2GetStatus` injection → status 5

- **3**: SetStatus patch → status 5 (semi-forcing)

- **4**: SetStatus patch → status 5 instead of 6

- **5**: Scan only — no patching

- Background patcher execution with real-time logging.

- Automatic generation of the `DNAS Patcher Code.txt` log file.

- Requires administrator privileges (UAC) to function correctly.

---

## 🔹 Requirements

- **Windows 7 or higher** (64-bit recommended)
 
- **Python 3.10+** (only required if using the `.py` file directly)
 
- **DNAS Patcher executable** (It can be found here: https://www.psx-place.com/resources/ps2-dnas-net-patcher.792/)
 
- **PS2 Game ISO File** ou **eeMemory.bin** (It can be extracted from the PCSX2 emulator's savestate file using 7zip. To obtain the correct `eeMemory.bin` file, you must create a savestate when the `DNAS logo appears on the screen`.)

- The program requests **administrator** permission to modify protected files.

---

## 🔹 How to use

1. **Download the file** `DNAS_Patcher_GUI.py`or `DNAS_Patcher_GUI.py`.

2. Run it.

3. Locate the executable `DNAS_PATCHER21.EXE` or equivalent.

4. Locate the `ISO` or `eeMemory.bin` file.

5. Choose the Operating Mode: (I recommend number `1` to patch the **ISO** and `5` to only scan the **eeMemory.bin** file.)
6. Click RUN.
7. The application generates a log file containing the patch code.

---

## 🔹 Credits

- krHACKen (DNAS-net Patcher)
