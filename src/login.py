import tkinter as tk
from tkinter import messagebox
import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SEC_PATH = os.path.join(_HERE, "security.py")
 
if os.path.exists(_SEC_PATH):
    spec = importlib.util.spec_from_file_location("security", _SEC_PATH)
    security = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(security)
else:
    security = None
 
 
BG        = "#f0f0f0"
TITLE_BG  = "#d0d0d0"
TITLE_FG  = "#000000"
TEXT      = "#000000"
SUBTEXT   = "#444444"
ENTRY_BG  = "#ffffff"
BTN_BG    = "#e0e0e0"
BTN_HOVER = "#c8c8c8"
LINK      = "#000080"
SEP       = "#a0a0a0"
 
 
class ForgotPasswordDialog(tk.Toplevel):
    def __init__(self, parent, username: str):
        super().__init__(parent)
        self.username = username
        self.title("Reset Password")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.grab_set()
 
        self._build_titlebar()
        tk.Frame(self, bg=SEP, height=1).pack(fill="x")
 
        inner = tk.Frame(self, bg=BG)
        inner.pack(padx=20, pady=16, fill="both", expand=True)
 
        tk.Label(inner, text=f"Resetting password for '{username}'",
                 font=("Trebuchet MS", 9), fg=SUBTEXT,
                 bg=BG).pack(anchor="w", pady=(0, 12))
 
        tk.Label(inner, text="Security PIN:",
                 font=("Trebuchet MS", 9), fg=TEXT,
                 bg=BG).pack(anchor="w")
        self.pin_var = tk.StringVar()
        tk.Entry(inner, textvariable=self.pin_var, show="*",
                 font=("Trebuchet MS", 10), fg=TEXT, bg=ENTRY_BG,
                 relief="sunken", bd=2, width=28).pack(fill="x", pady=(2, 10))
 
        tk.Label(inner, text="New Password:",
                 font=("Trebuchet MS", 9), fg=TEXT,
                 bg=BG).pack(anchor="w")
        self.new_pw_var = tk.StringVar()
        tk.Entry(inner, textvariable=self.new_pw_var, show="*",
                 font=("Trebuchet MS", 10), fg=TEXT, bg=ENTRY_BG,
                 relief="sunken", bd=2, width=28).pack(fill="x", pady=(2, 18))
 
        btn_row = tk.Frame(inner, bg=BG)
        btn_row.pack(anchor="e")
 
        for text, cmd in [("Confirm", self._on_confirm), ("Cancel", self.destroy)]:
            b = tk.Button(btn_row, text=text,
                          font=("Trebuchet MS", 10),
                          fg=TEXT, bg=BTN_BG,
                          relief="raised", bd=1,
                          padx=20, pady=6,
                          cursor="hand2", command=cmd)
            b.pack(side="left", padx=(0, 6))
            b.bind("<Enter>", lambda e, btn=b: btn.configure(bg=BTN_HOVER))
            b.bind("<Leave>", lambda e, btn=b: btn.configure(bg=BTN_BG))
 
        self._center(330, 240)
 
    def _build_titlebar(self):
        bar = tk.Frame(self, bg=TITLE_BG, height=30)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        tk.Label(bar, text="Reset Password",
                 font=("Trebuchet MS", 9, "bold"),
                 fg=TITLE_FG, bg=TITLE_BG).pack(side="left", padx=10, pady=4)
 
    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
 
    def _on_confirm(self):
        pin    = self.pin_var.get().strip()
        new_pw = self.new_pw_var.get().strip()
 
        if not pin or not new_pw:
            messagebox.showwarning("Missing Fields",
                                   "Please fill in both fields.", parent=self)
            return
 
        if security is None:
            messagebox.showerror("Error", "security.py not found.", parent=self)
            return
 
        ok, msg = security.check_pin(self.username, pin)
        if not ok:
            messagebox.showerror("Wrong PIN", msg, parent=self)
            return
 
        ok, msg = security.update_password(self.username, new_pw)
        if not ok:
            messagebox.showwarning("Invalid Password", msg, parent=self)
            return
 
        messagebox.showinfo("Success",
                            "Password updated. Please log in again.",
                            parent=self)
        self.destroy()
 
 
class LoginApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Composites Inventory Manager")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
 
        self._build_ui()
        self._center(400, 300)
 
    def _center(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
 
    def _build_ui(self):
        # Title bar
        title_bar = tk.Frame(self.root, bg=TITLE_BG, height=34)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="Composites Inventory Manager",
                 font=("Trebuchet MS", 10, "bold"),
                 fg=TITLE_FG, bg=TITLE_BG).pack(side="left", padx=10, pady=6)
 
        tk.Frame(self.root, bg=SEP, height=1).pack(fill="x")
 
        # Body
        body = tk.Frame(self.root, bg=BG)
        body.pack(padx=28, pady=22, fill="both", expand=True)
 
        tk.Label(body, text="Please log in to continue",
                 font=("Trebuchet MS", 10), fg=SUBTEXT,
                 bg=BG).pack(anchor="w", pady=(0, 16))
 
        # Username
        tk.Label(body, text="Username:",
                 font=("Trebuchet MS", 9), fg=TEXT,
                 bg=BG).pack(anchor="w")
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(body, textvariable=self.username_var,
                                       font=("Trebuchet MS", 10),
                                       fg=TEXT, bg=ENTRY_BG,
                                       relief="sunken", bd=2)
        self.username_entry.pack(fill="x", pady=(2, 12))
        self.username_entry.focus_set()
 
        # Password
        tk.Label(body, text="Password:",
                 font=("Trebuchet MS", 9), fg=TEXT,
                 bg=BG).pack(anchor="w")
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(body, textvariable=self.password_var,
                                        show="*",
                                        font=("Trebuchet MS", 10),
                                        fg=TEXT, bg=ENTRY_BG,
                                        relief="sunken", bd=2)
        self.password_entry.pack(fill="x", pady=(2, 6))
        self.password_entry.bind("<Return>", lambda e: self._on_login())
 
        # Forgot password
        forgot = tk.Label(body, text="Forgot password?",
                          font=("Trebuchet MS", 8, "underline"),
                          fg=LINK, bg=BG, cursor="hand2")
        forgot.pack(anchor="e", pady=(0, 18))
        forgot.bind("<Button-1>", self._on_forgot)
        forgot.bind("<Enter>", lambda e: forgot.configure(fg="#0000cc"))
        forgot.bind("<Leave>", lambda e: forgot.configure(fg=LINK))
 
        # Buttons
        btn_row = tk.Frame(body, bg=BG)
        btn_row.pack(anchor="e")
 
        for text, cmd in [("Log In", self._on_login), ("Cancel", self.root.destroy)]:
            b = tk.Button(btn_row, text=text,
                          font=("Trebuchet MS", 10),
                          fg=TEXT, bg=BTN_BG,
                          relief="raised", bd=1,
                          padx=22, pady=7,
                          cursor="hand2", command=cmd)
            b.pack(side="left", padx=(0, 8))
            b.bind("<Enter>", lambda e, btn=b: btn.configure(bg=BTN_HOVER))
            b.bind("<Leave>", lambda e, btn=b: btn.configure(bg=BTN_BG))
 
    def _on_login(self):
        user = self.username_var.get().strip()
        pwd  = self.password_var.get().strip()
 
        if not user or not pwd:
            messagebox.showwarning("Missing Fields",
                                   "Please enter both username and password.")
            return
 
        if security is None:
            messagebox.showerror("Error",
                                 "security.py not found.\nPlace it alongside login.py.")
            return
 
        ok, msg = security.check_login(user, pwd)
        if not ok:
            messagebox.showerror("Login Failed", msg)
            return
 
        self.root.destroy()
 
        gui_path = os.path.join(_HERE, "gui.py")
        if os.path.exists(gui_path):
            spec = importlib.util.spec_from_file_location("gui", gui_path)
            gui  = importlib.util.module_from_spec(spec)
            sys.modules["gui"] = gui
            spec.loader.exec_module(gui)
        else:
            new_root = tk.Tk()
            new_root.title("Composites Inventory Manager")
            new_root.configure(bg=BG)
            tk.Label(new_root,
                     text=f"Logged in as '{user}'\n\ngui.py not found — place it in:\n{_HERE}",
                     font=("Trebuchet MS", 11), fg=TEXT, bg=BG,
                     justify="center").pack(expand=True, padx=40, pady=40)
            new_root.mainloop()
 
    def _on_forgot(self, event=None):
        user = self.username_var.get().strip()
        if not user:
            messagebox.showwarning("Username Required",
                                   "Enter your username first, then click 'Forgot password?'.")
            return
 
        if security is None:
            messagebox.showerror("Error", "security.py not found.")
            return
 
        db = security._load_db()
        if user.lower() not in db:
            messagebox.showerror("Not Found",
                                 f"No account found for username '{user}'.")
            return
 
        ForgotPasswordDialog(self.root, user)
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app  = LoginApp(root)
    root.mainloop()
    
    #4/14 changes