import tkinter as tk
from login import LoginApp
from gui import show_inventory_screen

"""
app.py purpose:
The engine that manages the transition between UI states (Login -> Main GUI).
"""

def run_app() -> None:
    # 1. Create the main TK instance for the Login phase
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()

    # 2. Check the success flag from the login window
    # If the user logged in successfully, login_app.login_successful will be True
    if getattr(login_app, 'login_successful', False):
        # This function is in your gui.py and starts the main dashboard
        show_inventory_screen()

if __name__ == "__main__":
    run_app()