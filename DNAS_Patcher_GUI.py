import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import ctypes
import sys
import threading
import os
import queue
import webbrowser

# =========================
# UAC
# =========================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    params = f'"{sys.argv[0]}" --elevated'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

if not is_admin() and "--elevated" not in sys.argv:
    relaunch_as_admin()
    sys.exit(0)

# =========================
# Texts (English only)
# =========================
def t(key):
    TEXTS = {
        "title": "DNAS-net Patcher GUI",
        "exe": "DNAS_PATCHER executable",
        "target": "eeMemory.bin or ISO file",
        "browse": "Browse",
        "mode": "Operation Mode",
        "run": "Run",
        "log": "Execution log",
        "err_select": "Select executable and BIN/ISO file",
        "started": "=== DNAS-net Patcher started ===",
        "finished": "=== Execution finished ===",
        "log_saved": "Log saved at",
        "confirm_title": "Confirmation",
        "confirm_msg_1": "Mode 1 may modify memory. Continue?",
        "confirm_msg_3": "Mode 3 applies a patch. Continue?",
        "confirm_msg_4": "Mode 4 modifies status. Continue?",
    }
    return TEXTS.get(key, key)

# =========================
# Modes
# =========================
MODE_DESC = {
    "1": "sceDNAS2GetStatus injection → fake deinit, error 0, status 5",
    "2": "sceDNAS2GetStatus injection → status 5",
    "3": "SetStatus patch → status 5 (semi-forcing)",
    "4": "SetStatus patch → status 5 instead of 6",
    "5": "Scan only — no patching"
}

MODE_WARN_KEYS = {
    "1": "confirm_msg_1",
    "3": "confirm_msg_3",
    "4": "confirm_msg_4"
}

# =========================
# Log
# =========================
log_queue = queue.Queue()

def process_log_queue():
    try:
        while True:
            msg = log_queue.get_nowait()
            log_text.config(state="normal")  
            log_text.insert(tk.END, msg + "\n")
            log_text.see(tk.END)
            log_text.config(state="disabled")  
    except queue.Empty:
        pass
    root.after(40, process_log_queue)

# =========================
# Patcher thread
# =========================
def patcher_thread(exe, target, mode):
    btn_run.config(state="disabled")

    out_dir = os.path.dirname(target)
    name = os.path.splitext(os.path.basename(target))[0]
    log_file = os.path.join(out_dir, f"{name} DNAS Patcher Code.txt")

    log_queue.put(t("started"))
    lines = []

    try:
        p = subprocess.Popen(
            [exe, target, mode],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        for line in p.stdout:
            line = line.rstrip()
            lines.append(line + "\n")
            log_queue.put(line)

        p.wait()

        with open(log_file, "w", encoding="utf-8") as f:
            f.writelines(lines)

        log_queue.put(t("finished"))
        log_queue.put(f"{t('log_saved')}: {log_file}")

    except Exception as e:
        log_queue.put(str(e))

    btn_run.config(state="normal")

# =========================
# Run
# =========================
def run_patcher():
    if not exe_path.get() or not target_path.get():
        messagebox.showerror(t("err_select"), t("err_select"))
        return

    warn = MODE_WARN_KEYS.get(mode_var.get())
    if warn and not messagebox.askyesno(t("confirm_title"), t(warn)):
        return

    log_text.config(state="normal")
    log_text.delete("1.0", tk.END)
    log_text.config(state="disabled")
    threading.Thread(
        target=patcher_thread,
        args=(exe_path.get(), target_path.get(), mode_var.get()),
        daemon=True
    ).start()

# =========================
# About window
# =========================
def open_link(url):
    webbrowser.open_new(url)

def show_about():
    win = tk.Toplevel(root)
    win.title("About")
    win.resizable(False, False)
    win.grab_set()
    frame = ttk.Frame(win, padding=20)
    frame.pack()

    ttk.Label(frame, text="DNAS-net Patcher GUI", font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
    ttk.Label(frame, text="Created by davbrasan using ChatGPT 🤖").pack()

    link_github = tk.Label(frame, text="https://github.com/davbrasan/DNAS-Patcher-GUI",
                           fg="#0066cc", cursor="hand2")
    link_github.pack(pady=(5, 10))
    link_github.bind("<Button-1>", lambda e: open_link("https://github.com/davbrasan/DNAS-Patcher-GUI"))

    ttk.Separator(frame).pack(fill="x", pady=10)
    ttk.Label(frame, text="Original DNAS Patcher by krHACKen").pack()

    link_psx = tk.Label(frame, text="https://www.psx-place.com/resources/ps2-dnas-net-patcher.792/",
                        fg="#0066cc", cursor="hand2")
    link_psx.pack(pady=5)
    link_psx.bind("<Button-1>", lambda e: open_link(
        "https://www.psx-place.com/resources/ps2-dnas-net-patcher.792/"
    ))

    ttk.Button(frame, text="Close", command=win.destroy).pack(pady=15)

# =========================
# GUI
# =========================
root = tk.Tk()
root.title(t("title"))

# Tamanho fixo
fixed_width = 480
fixed_height = 600
root.geometry(f"{fixed_width}x{fixed_height}")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f5f5f5")
style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill="both")
main_frame.columnconfigure(0, weight=1)

# ===== LEFT PANEL =====
left_panel = ttk.Frame(main_frame)
left_panel.pack(expand=True, fill="both")

lbl_exe = ttk.Label(left_panel, text=t("exe"))
lbl_exe.pack(anchor="center")
exe_path = tk.StringVar()
ttk.Entry(left_panel, textvariable=exe_path, width=40).pack(fill="x")
ttk.Button(left_panel, text=t("browse"), command=lambda: exe_path.set(filedialog.askopenfilename())).pack(fill="x", pady=8)

lbl_target = ttk.Label(left_panel, text=t("target"))
lbl_target.pack(anchor="center")
target_path = tk.StringVar()
ttk.Entry(left_panel, textvariable=target_path, width=40).pack(fill="x")
ttk.Button(left_panel, text=t("browse"), command=lambda: target_path.set(filedialog.askopenfilename())).pack(fill="x", pady=8)

lbl_mode = ttk.Label(left_panel, text=t("mode"))
lbl_mode.pack(anchor="center")
mode_var = tk.StringVar(value="5")
ttk.OptionMenu(left_panel, mode_var, mode_var.get(), *MODE_DESC.keys()).pack(fill="x")

lbl_mode_desc = ttk.Label(left_panel, wraplength=350, foreground="#555")
lbl_mode_desc.pack(pady=6)

def update_mode_desc(*_):
    lbl_mode_desc.config(text=MODE_DESC.get(mode_var.get(), ""))

mode_var.trace_add("write", update_mode_desc)
update_mode_desc()

btn_run = ttk.Button(left_panel, text=t("run"), command=run_patcher)
btn_run.pack(fill="x", pady=(5, 5))

btn_about = ttk.Button(left_panel, text="About", command=show_about)
btn_about.pack(fill="x", pady=(0, 15))

# ===== LOG =====
lbl_log = ttk.Label(left_panel, text=t("log"))
lbl_log.pack(anchor="w")
log_text = scrolledtext.ScrolledText(left_panel, font=("Consolas", 10), height=15)
log_text.pack(expand=True, fill="both")
log_text.config(state="disabled")  

# =========================
root.after(40, process_log_queue)
root.mainloop()


