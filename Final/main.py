import tkinter as tk
from tkinter import messagebox
import tambahkurang

def launch_tambahkurang():
    if password_entry.get().casefold() == "dhaniganteng":
        tambahkurang.run()
    else:
        messagebox.showerror("Error", "Password salah!")

def launch_sistem_kasir():
    if password_entry.get().casefold() == "dhaniganteng":
        try:
            import kasir
            import importlib
            importlib.reload(kasir) 
        except Exception as e:
            messagebox.showerror("Error", "Failed to launch kasir.py: " + str(e))
    else:
        messagebox.showerror("Error", "Password salah!")

launcher_window = tk.Tk()
launcher_window.title("Launcher Aplikasi")
launcher_window.geometry("300x150")

tk.Label(launcher_window, text="Masukkan Password:").pack()
password_entry = tk.Entry(launcher_window, show="*")
password_entry.pack()

tk.Button(launcher_window, text="Buka tambah barang gui", command=launch_tambahkurang).pack()
tk.Button(launcher_window, text="Buka Sistem Kasir", command=launch_sistem_kasir).pack()

launcher_window.mainloop()
