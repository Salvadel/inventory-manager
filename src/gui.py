import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from auth import login_user
import inventory
import database
"""
gui.py purpose:
Contains all code related to the main menu graphical user interface of the application.
"""

COLS   = ("ID", "Name", "Qty", "Date Added", "Expiration", "Location", "Category", "Vendor")
WIDTHS = (40, 160, 50, 100, 100, 100, 100, 110)


def show_inventory_screen():
    """Displays inventory management interface."""
    root = tk.Tk()
    root.title("Composite Inventory Manager")
    root.geometry("1000x600")

    # Search Bar
    top = tk.Frame(root)
    top.pack(fill="x", padx=10, pady=6)

    tk.Label(top, text="Search:").pack(side="left")
    search_var = tk.StringVar()
    search_entry = tk.Entry(top, textvariable=search_var, width=30)
    search_entry.pack(side="left", padx=4)

    tk.Label(top, text="  Sort by:").pack(side="left")
    sort_var = tk.StringVar(value="ID")
    ttk.Combobox(top, textvariable=sort_var,
        values=["ID","Name","Qty","Date Added","Expiration","Location","Category","Vendor"],
                state="readonly", width=12).pack(side="left", padx=4)

    tk.Label(top, text="  Category:").pack(side="left")
    filter_var = tk.StringVar(value="All")
    filter_cb = ttk.Combobox(top, textvariable=filter_var, state="readonly", width=14)
    filter_cb.pack(side="left", padx=4)

    def refresh_category_dropdown():
        cats = ["All"] + [row[0] for row in database.get_categories()]
        filter_cb["values"] = cats
        if filter_var.get() not in cats:
            filter_var.set("All")

    refresh_category_dropdown()

    # Table
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

    def load_items(items):
        tree.delete(*tree.get_children())
        for row in (items or []):
            tree.insert("", "end", values=tuple("" if v is None else v for v in row))

    def do_search(*_):
        query = search_var.get().strip()
        if query:
            try:
                results = inventory.search_inventory(query)
                load_items(results)
            except Exception as e:
                messagebox.showerror("Search Error", str(e))
        else:
            items, _ = inventory.view_inventory()
            load_items(items)

    inventory.startup()
    items, _ = inventory.view_inventory()
    load_items(items)

    def do_reset():
        search_var.set("")
        sort_var.set("ID")
        filter_var.set("All")
        items, _ = inventory.view_inventory()
        load_items(items)

    tk.Button(top, text="Search", command=do_search).pack(side="left", padx=2)
    tk.Button(top, text="Reset", command=do_reset).pack(side="left", padx=2)
    search_entry.bind("<Return>", do_search)

    vsb.pack(side="right",  fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # Buttons
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
