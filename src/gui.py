import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date
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
    sort_cb = ttk.Combobox(top, textvariable=sort_var,
        values=["ID","Name","Qty","Date Added","Expiration","Location","Category","Vendor"],
                state="readonly", width=12)
    sort_cb.pack(side="left", padx=4)

    sort_asc = [True]
    asc_btn = tk.Button(top, text="↑ Asc", width=6)
    asc_btn.pack(side="left", padx=2)

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

    COL_IDX = {col: i for i, col in enumerate(COLS)}

    for col, w in zip(COLS, WIDTHS):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center" if col in ("ID","Qty") else "w")

    def load_items(items):
        tree.delete(*tree.get_children())
        for row in (items or []):
            tree.insert("", "end", values=tuple("" if v is None else v for v in row))

    def apply_filters(*_):
        query = search_var.get().strip()
        cat = filter_var.get()

        if query:
            try:
                items = inventory.search_inventory(query) or []
            except Exception as e:
                messagebox.showerror("Search Error", str(e))
                return
        else:
            raw, _ = inventory.view_inventory()
            items = raw or []

        if cat != "All":
            items = [row for row in items if (row[6] or "") == cat]

        col = sort_var.get()
        idx = COL_IDX.get(col, 0)
        reverse = not sort_asc[0]

        def sort_key(row):
            val = row[idx]
            if val is None or val == "":
                return (1, "")
            if col in ("ID", "Qty"):
                try:
                    return (0, int(val))
                except (ValueError, TypeError):
                    pass
            return (0, str(val).lower())

        items = sorted(items, key=sort_key, reverse=reverse)
        load_items(items)

        for c in COLS:
            arrow = (" ↑" if sort_asc[0] else " ↓") if c == col else ""
            tree.heading(c, text=c + arrow, command=lambda c=c: on_heading_click(c))

    def on_heading_click(col):
        if sort_var.get() == col:
            sort_asc[0] = not sort_asc[0]
        else:
            sort_var.set(col)
            sort_asc[0] = True
        asc_btn.config(text="↑ Asc" if sort_asc[0] else "↓ Desc")
        apply_filters()

    def toggle_sort_direction():
        sort_asc[0] = not sort_asc[0]
        asc_btn.config(text="↑ Asc" if sort_asc[0] else "↓ Desc")
        apply_filters()

    asc_btn.config(command=toggle_sort_direction)
    sort_cb.bind("<<ComboboxSelected>>", apply_filters)
    filter_cb.bind("<<ComboboxSelected>>", apply_filters)

    for col in COLS:
        tree.heading(col, command=lambda c=col: on_heading_click(c))

    inventory.startup()
    apply_filters()

    def do_reset():
        search_var.set("")
        sort_var.set("ID")
        sort_asc[0] = True
        asc_btn.config(text="↑ Asc")
        filter_var.set("All")
        apply_filters()

    tk.Button(top, text="Search", command=apply_filters).pack(side="left", padx=2)
    tk.Button(top, text="Reset", command=do_reset).pack(side="left", padx=2)
    search_entry.bind("<Return>", apply_filters)

    vsb.pack(side="right",  fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # Buttons
    bot = tk.Frame(root)
    bot.pack(fill="x", padx=10, pady=6)

    def center_on_parent(dialog, width, height):
        root.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() - width) // 2
        y = root.winfo_y() + (root.winfo_height() - height) // 2
        dialog.geometry(f"{width}x{height}+{x}+{y}")

    def open_add_item_dialog():
        dialog = tk.Toplevel(root)
        dialog.title("Add Item")
        dialog.resizable(False, False)
        dialog.grab_set()
        center_on_parent(dialog, 350, 280)

        fields = [
            ("Name *", ""),
            ("Quantity *", ""),
            ("Date Added (YYYY-MM-DD)", date.today().strftime("%Y-%m-%d")),
            ("Expiration (YYYY-MM-DD)", ""),
            ("Location", "Unknown"),
            ("Category", "General"),
            ("Vendor", "Unknown"),
        ]

        entries = {}
        for i, (label, default) in enumerate(fields):
            tk.Label(dialog, text=label, anchor="w").grid(row=i, column=0, padx=10, pady=4, sticky="w")
            var = tk.StringVar(value=default)
            tk.Entry(dialog, textvariable=var, width=25).grid(row=i, column=1, padx=10, pady=4)
            entries[label] = var

        def submit():
            name = entries["Name *"].get().strip()
            qty_str = entries["Quantity *"].get().strip()
            date_added = entries["Date Added (YYYY-MM-DD)"].get().strip() or None
            date_expired = entries["Expiration (YYYY-MM-DD)"].get().strip() or None
            location = entries["Location"].get().strip() or "Unknown"
            category = entries["Category"].get().strip() or "General"
            vendor = entries["Vendor"].get().strip() or "Unknown"

            if not name:
                messagebox.showerror("Error", "Name is required.", parent=dialog)
                return
            try:
                quantity = int(qty_str)
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a whole number.", parent=dialog)
                return

            try:
                inventory.add_inventory_item(name, quantity, date_added, date_expired, location, category, vendor)
                dialog.destroy()
                refresh_category_dropdown()
                apply_filters()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        btn_row = len(fields)
        tk.Button(dialog, text="Add", command=submit, width=10).grid(row=btn_row, column=0, pady=10, padx=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy, width=10).grid(row=btn_row, column=1, pady=10, padx=10)

    def open_edit_item_dialog():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item to edit.")
            return

        row_vals = tree.item(selected[0], "values")
        item_id = int(row_vals[0])

        dialog = tk.Toplevel(root)
        dialog.title("Edit Item")
        dialog.resizable(False, False)
        dialog.grab_set()
        center_on_parent(dialog, 350, 280)

        fields = [
            ("Name *",                   row_vals[1]),
            ("Quantity *",               row_vals[2]),
            ("Date Added (YYYY-MM-DD)",  row_vals[3]),
            ("Expiration (YYYY-MM-DD)",  row_vals[4]),
            ("Location",                 row_vals[5]),
            ("Category",                 row_vals[6]),
            ("Vendor",                   row_vals[7]),
        ]

        entries = {}
        for i, (label, default) in enumerate(fields):
            tk.Label(dialog, text=label, anchor="w").grid(row=i, column=0, padx=10, pady=4, sticky="w")
            var = tk.StringVar(value=default)
            tk.Entry(dialog, textvariable=var, width=25).grid(row=i, column=1, padx=10, pady=4)
            entries[label] = var

        def submit():
            name = entries["Name *"].get().strip()
            qty_str = entries["Quantity *"].get().strip()
            date_added = entries["Date Added (YYYY-MM-DD)"].get().strip() or None
            date_expired = entries["Expiration (YYYY-MM-DD)"].get().strip() or None
            location = entries["Location"].get().strip() or "Unknown"
            category = entries["Category"].get().strip() or "General"
            vendor = entries["Vendor"].get().strip() or "Unknown"

            if not name:
                messagebox.showerror("Error", "Name is required.", parent=dialog)
                return
            try:
                quantity = int(qty_str)
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a whole number.", parent=dialog)
                return

            try:
                inventory.update_inventory_item(item_id, name=name, quantity=quantity,
                                                date_added=date_added, date_expired=date_expired,
                                                location=location, category=category, vendor=vendor)
                dialog.destroy()
                refresh_category_dropdown()
                apply_filters()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        btn_row = len(fields)
        tk.Button(dialog, text="Save", command=submit, width=10).grid(row=btn_row, column=0, pady=10, padx=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy, width=10).grid(row=btn_row, column=1, pady=10, padx=10)

    def open_delete_item_dialog():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item to delete.")
            return

        row_vals = tree.item(selected[0], "values")
        item_id = int(row_vals[0])
        name, qty, date_added, expiration, location, category, vendor = row_vals[1:]

        dialog = tk.Toplevel(root)
        dialog.title("Confirm Delete")
        dialog.resizable(False, False)
        dialog.grab_set()
        center_on_parent(dialog, 360, 240)

        tk.Label(dialog, text="Are you sure you want to delete this item?",
                 font=("", 10, "bold")).pack(pady=(16, 8), padx=16)

        info = (
            f"ID:         {item_id}\n"
            f"Name:       {name}\n"
            f"Quantity:   {qty}\n"
            f"Date Added: {date_added}\n"
            f"Expiration: {expiration}\n"
            f"Location:   {location}\n"
            f"Category:   {category}\n"
            f"Vendor:     {vendor}"
        )
        tk.Label(dialog, text=info, justify="left", anchor="w",
                 bg="#f0f0f0", relief="groove", padx=8, pady=6,
                 font=("Courier", 9)).pack(fill="x", padx=16)

        def confirm():
            try:
                inventory.remove_inventory_item(item_id)
                dialog.destroy()
                apply_filters()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=12)
        tk.Button(btn_frame, text="Delete", command=confirm, width=10,
                  bg="#d9534f", fg="white").pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy, width=10).pack(side="left", padx=8)

    button_commands = {
        "Add Item": open_add_item_dialog,
        "Edit Item": open_edit_item_dialog,
        "Delete Item": open_delete_item_dialog,
        "Logout": root.destroy,
    }

    for label in ["Add Item", "Edit Item", "Delete Item", "Add to To-Buy List",
                "Manage Categories", "Manage Vendors", "View To-Buy List", "Change Password", "Logout"]:
        tk.Button(bot, text=label, width=14, command=button_commands.get(label)).pack(side="left", padx=3)

    root.mainloop()


def show_login_screen():
    """Displays login interface."""
    pass


def start_gui():
    """Creates and launches main application window."""
    show_inventory_screen()


if __name__ == "__main__":
    start_gui()
