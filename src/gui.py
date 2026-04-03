import tkinter as tk
from tkinter import ttk
from auth import login_user
import inventory
"""
gui.py purpose:
Handles graphical user interface.

***
Used Claude to help code the GUI, but not design the GUI.
***

Key features:
- Display login screen
- Display inventory interface
- Capture user input
- Trigger inventory actions


def start_gui() -> None:
    input: None
    output: None
    use: Creates and launches main application window
    pass


def show_login_screen() -> None:
    input: None
    output: None
    use: Displays login interface
    pass


def show_inventory_screen() -> None:
    input: None
    output: None
    use: Displays inventory management interface
    pass
"""

COLS   = ("ID", "Name", "Qty", "Date Added", "Expiration", "Location", "Category", "Vendor")
WIDTHS = (40, 160, 50, 100, 100, 100, 100, 110)


def show_inventory_screen():
    """Displays inventory management interface."""
    root = tk.Tk()
    root.title("Composite Inventory Manager")
    root.geometry("1000x600")

    # ── Search bar ────────────────────────────────────────────────────────────
    top = tk.Frame(root)
    top.pack(fill="x", padx=10, pady=6)

    tk.Label(top, text="Search:").pack(side="left")
    search_var = tk.StringVar()
    tk.Entry(top, textvariable=search_var, width=30).pack(side="left", padx=4)

    tk.Label(top, text="  Sort by:").pack(side="left")
    sort_var = tk.StringVar(value="ID")
    ttk.Combobox(top, textvariable=sort_var,
                 values=["ID","Name","Qty","Date Added","Expiration","Location","Category","Vendor"],
                 state="readonly", width=12).pack(side="left", padx=4)

    tk.Label(top, text="  Category:").pack(side="left")
    filter_var = tk.StringVar(value="All")
    ttk.Combobox(top, textvariable=filter_var,
                 values=["All","Raw Materials","Resins","Consumables","Abrasives"],
                 state="readonly", width=14).pack(side="left", padx=4)

    # ── Table ─────────────────────────────────────────────────────────────────
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=4)

    vsb = ttk.Scrollbar(frame, orient="vertical")
    hsb = ttk.Scrollbar(frame, orient="horizontal")
    tree = ttk.Treeview(frame, columns=COLS, show="headings", selectmode="browse",
                        yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    for col, w in zip(COLS, WIDTHS):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center" if col in ("ID","Qty") else "w")

    inventory.startup()
    items, _ = inventory.view_inventory()
    for row in (items or []):
        tree.insert("", "end", values=tuple("" if v is None else v for v in row))

    vsb.pack(side="right",  fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # ── Buttons ───────────────────────────────────────────────────────────────
    bot = tk.Frame(root)
    bot.pack(fill="x", padx=10, pady=6)

    for label in ["Add Item", "Edit Item", "Delete Item", "Add to To-Buy List",
                  "Manage Categories", "Manage Vendors", "View To-Buy List", "Change Password", "Logout"]:
        tk.Button(bot, text=label, width=14).pack(side="left", padx=3)

    root.mainloop()


def show_login_screen():
    """Displays login interface."""
    pass


def start_gui():
    """Creates and launches main application window."""
    show_inventory_screen()


if __name__ == "__main__":
    start_gui()
