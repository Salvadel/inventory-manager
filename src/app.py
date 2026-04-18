import tkinter as tk
from login import LoginApp
from gui import show_inventory_screen

"""
app.py purpose:
The engine that manages the transition between UI states (Login -> Main GUI).
"""
# Runs the application by first showing the login screen, then transitioning to the main inventory screen upon successful login
def run_app() -> None:
    
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()

    # If Login was sucessful, show the inventory screen
    if getattr(login_app, 'login_successful', False):
        # Start the main inventory screen
        show_inventory_screen()

# Run Main
if __name__ == "__main__":
    run_app()