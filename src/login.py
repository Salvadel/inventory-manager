import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import auth 

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

# A class to manage the login screen, and password reset
class LoginApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.login_successful = False # Flag to tell app.py if we should proceed
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
            messagebox.showwarning("Missing Fields", "Please enter username and password.")
            return

        # Call your existing logic in auth.py
        ok, msg = auth.login_user(user, pwd)
        
        if ok:
            # Check if backup code exists; if not, force setup
            if auth.check_user_needs_backup(user):
                self._show_backup_setup_popup(user)
            else:
                self.login_successful = True 
                self.root.destroy()
        else:
            messagebox.showerror("Login Failed", msg)

    def _on_forgot(self, event=None):

        # 1. Get Username
        user = simpledialog.askstring("Reset Password", "Enter your username:")
        if not user: return
        
        # 2. Get Backup Code
        backup = simpledialog.askstring("Reset Password", "Enter your backup code:", show="*")
        if not backup: return
        
        # 3. Get New Password
        new_pwd = simpledialog.askstring("Reset Password", "Enter new password:", show="*")
        if not new_pwd: return
        
        # Call the logic in auth.py
        success, message = auth.reset_password_with_backup(user, backup, new_pwd)
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def _show_backup_setup_popup(self, username):
            code = simpledialog.askstring("Security Setup", "Set a backup code for password recovery:", show="*")
            if code:
                ok, msg = auth.setup_backup_code(username, code)
                if ok:
                    messagebox.showinfo("Success", "Backup code set! Do not forget it!")
                    self.login_successful = True
                    self.root.destroy()
                else:
                    messagebox.showerror("Error", msg)

# Run Main
if __name__ == "__main__":
    root = tk.Tk()
    app  = LoginApp(root)
    root.mainloop()