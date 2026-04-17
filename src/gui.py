import tkinter as tk
from tkinter import ttk, simpledialog
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

    # Custom messagebox that always centers on the application window
    class _CenteredMessageBox:
        def _build(self, title, msg, parent=None):
            anchor = parent or root
            d = tk.Toplevel(anchor)
            d.title(title)
            d.resizable(False, False)
            d.transient(anchor)
            d.grab_set()
            tk.Label(d, text=msg, wraplength=260, justify="left",
                     padx=16, pady=12).pack()
            return d, anchor

        def _show(self, d, anchor):
            d.update_idletasks()
            w = max(d.winfo_reqwidth(), 300)
            h = d.winfo_reqheight()
            x = anchor.winfo_x() + (anchor.winfo_width()  - w) // 2
            y = anchor.winfo_y() + (anchor.winfo_height() - h) // 2
            d.geometry(f"{w}x{h}+{x}+{y}")
            d.wait_window()

        def showerror(self, title, msg, parent=None):
            d, anchor = self._build(title, msg, parent)
            tk.Button(d, text="OK", command=d.destroy, width=8).pack(pady=(0, 10))
            self._show(d, anchor)

        def showwarning(self, title, msg, parent=None):
            d, anchor = self._build(title, msg, parent)
            tk.Button(d, text="OK", command=d.destroy, width=8).pack(pady=(0, 10))
            self._show(d, anchor)

        def showinfo(self, title, msg, parent=None):
            d, anchor = self._build(title, msg, parent)
            tk.Button(d, text="OK", command=d.destroy, width=8).pack(pady=(0, 10))
            self._show(d, anchor)

        def askyesno(self, title, msg, parent=None):
            result = [False]
            d, anchor = self._build(title, msg, parent)
            btn_f = tk.Frame(d)
            btn_f.pack(pady=(0, 10))
            tk.Button(btn_f, text="Yes", width=8,
                      command=lambda: (result.__setitem__(0, True), d.destroy())).pack(side="left", padx=6)
            tk.Button(btn_f, text="No", width=8,
                      command=d.destroy).pack(side="left", padx=6)
            self._show(d, anchor)
            return result[0]

    messagebox = _CenteredMessageBox()

    # Row 1: Search + Sort
    top = tk.Frame(root)
    top.pack(fill="x", padx=10, pady=(6, 2))

    tk.Label(top, text="Search:").pack(side="left")
    search_var = tk.StringVar()
    search_entry = tk.Entry(top, textvariable=search_var, width=30)
    search_entry.pack(side="left", padx=4)

    tk.Button(top, text="Search", command=lambda: apply_filters()).pack(side="left", padx=2)
    tk.Button(top, text="Reset",  command=lambda: do_reset()).pack(side="left", padx=2)

    # Row 2: Filters + Sort
    top2 = tk.Frame(root)
    top2.pack(fill="x", padx=10, pady=(0, 4))

    tk.Label(top2, text="Sort by:").pack(side="left")
    sort_var = tk.StringVar(value="ID")
    sort_cb = ttk.Combobox(top2, textvariable=sort_var,
        values=["ID","Name","Qty","Date Added","Expiration","Location","Category","Vendor"],
                state="readonly", width=12)
    sort_cb.pack(side="left", padx=4)

    sort_asc = [True]
    asc_btn = tk.Button(top2, text="↑ Asc", width=6)
    asc_btn.pack(side="left", padx=2)

    tk.Label(top2, text="  Category:").pack(side="left")
    filter_var = tk.StringVar(value="All")
    filter_cb = ttk.Combobox(top2, textvariable=filter_var, state="readonly", width=14)
    filter_cb.pack(side="left", padx=4)

    tk.Label(top2, text="  Vendor:").pack(side="left")
    vendor_filter_var = tk.StringVar(value="All")
    vendor_filter_cb = ttk.Combobox(top2, textvariable=vendor_filter_var, state="readonly", width=14)
    vendor_filter_cb.pack(side="left", padx=4)

    tk.Label(top2, text="  Location:").pack(side="left")
    location_filter_var = tk.StringVar(value="All")
    location_filter_cb = ttk.Combobox(top2, textvariable=location_filter_var, state="readonly", width=14)
    location_filter_cb.pack(side="left", padx=4)

    def refresh_category_dropdown():
        cats = ["All"] + [row[0] for row in database.get_categories()]
        filter_cb["values"] = cats
        if filter_var.get() not in cats:
            filter_var.set("All")

    def refresh_vendor_dropdown():
        vendors = ["All"] + inventory.get_all_vendor_names()
        vendor_filter_cb["values"] = vendors
        if vendor_filter_var.get() not in vendors:
            vendor_filter_var.set("All")

    def refresh_location_dropdown():
        locations = ["All"] + inventory.get_all_locations()
        location_filter_cb["values"] = locations
        if location_filter_var.get() not in locations:
            location_filter_var.set("All")

    refresh_category_dropdown()
    refresh_vendor_dropdown()
    refresh_location_dropdown()

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
        vendor = vendor_filter_var.get()
        location = location_filter_var.get()

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
        if vendor != "All":
            items = [row for row in items if (row[7] or "") == vendor]
        if location != "All":
            items = [row for row in items if (row[5] or "") == location]

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
    vendor_filter_cb.bind("<<ComboboxSelected>>", apply_filters)
    location_filter_cb.bind("<<ComboboxSelected>>", apply_filters)

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
        vendor_filter_var.set("All")
        location_filter_var.set("All")
        apply_filters()

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
        center_on_parent(dialog, 380, 280)

        plain_fields = [
            ("Name *", ""),
            ("Quantity *", ""),
            ("Date Added (YYYY-MM-DD)", date.today().strftime("%Y-%m-%d")),
            ("Expiration (YYYY-MM-DD)", ""),
        ]

        entries = {}
        for i, (label, default) in enumerate(plain_fields):
            tk.Label(dialog, text=label, anchor="w").grid(row=i, column=0, padx=10, pady=4, sticky="w")
            var = tk.StringVar(value=default)
            tk.Entry(dialog, textvariable=var, width=25).grid(row=i, column=1, padx=10, pady=4)
            entries[label] = var

        def make_combobox_with_new(parent_row, label, default, get_all_fn, add_fn, refresh_fn):
            """Creates a combobox + New button row; returns (StringVar, Combobox)."""
            row_var = tk.StringVar(value=default)
            tk.Label(dialog, text=label, anchor="w").grid(row=parent_row, column=0, padx=10, pady=4, sticky="w")
            frame = tk.Frame(dialog)
            frame.grid(row=parent_row, column=1, padx=10, pady=4, sticky="w")
            cb = ttk.Combobox(frame, textvariable=row_var,
                              values=[default] + get_all_fn(),
                              state="readonly", width=15)
            cb.pack(side="left")

            def open_new():
                add_dialog = tk.Toplevel(dialog)
                add_dialog.title(f"Add {label}")
                add_dialog.resizable(False, False)
                add_dialog.grab_set()
                center_on_parent(add_dialog, 280, 110)

                tk.Label(add_dialog, text=f"{label} Name:").grid(row=0, column=0, padx=10, pady=12, sticky="w")
                name_var = tk.StringVar()
                tk.Entry(add_dialog, textvariable=name_var, width=20).grid(row=0, column=1, padx=10, pady=12)

                def submit_new():
                    name = name_var.get().strip()
                    if not name:
                        messagebox.showerror("Error", "Name cannot be empty.", parent=add_dialog)
                        return
                    try:
                        add_fn(name)
                        add_dialog.destroy()
                        cb["values"] = [default] + get_all_fn()
                        row_var.set(name)
                        refresh_fn()
                    except Exception as e:
                        messagebox.showerror("Error", str(e), parent=add_dialog)

                btn_f = tk.Frame(add_dialog)
                btn_f.grid(row=1, column=0, columnspan=2, pady=4)
                tk.Button(btn_f, text="Add", command=submit_new, width=8,
                          bg="#5cb85c", fg="white").pack(side="left", padx=6)
                tk.Button(btn_f, text="Cancel", command=add_dialog.destroy, width=8).pack(side="left", padx=6)

            tk.Button(frame, text="New", command=open_new, width=5).pack(side="left", padx=(6, 0))
            return row_var, cb

        loc_row = len(plain_fields)
        loc_var, _ = make_combobox_with_new(loc_row, "Location", "Unknown",
                                            inventory.get_all_location_names,
                                            inventory.new_location,
                                            refresh_location_dropdown)

        cat_row = loc_row + 1
        cat_var, _ = make_combobox_with_new(cat_row, "Category", "General",
                                            inventory.get_all_categories,
                                            inventory.new_category,
                                            refresh_category_dropdown)

        vendor_row = cat_row + 1
        vendor_var, _ = make_combobox_with_new(vendor_row, "Vendor", "Unknown",
                                               inventory.get_all_vendor_names,
                                               inventory.new_vendor_name,
                                               refresh_vendor_dropdown)

        def submit():
            name = entries["Name *"].get().strip()
            qty_str = entries["Quantity *"].get().strip()
            date_added = entries["Date Added (YYYY-MM-DD)"].get().strip() or None
            date_expired = entries["Expiration (YYYY-MM-DD)"].get().strip() or None
            location = loc_var.get() or "Unknown"
            category = cat_var.get() or "General"
            vendor = vendor_var.get() or "Unknown"

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
                refresh_vendor_dropdown()
                refresh_location_dropdown()
                apply_filters()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        btn_row = vendor_row + 1
        tk.Button(dialog, text="Add", command=submit, width=10, bg="#5cb85c", fg="white").grid(row=btn_row, column=0, pady=10, padx=10)
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

        plain_fields = [
            ("Name *",                   row_vals[1]),
            ("Quantity *",               row_vals[2]),
            ("Date Added (YYYY-MM-DD)",  row_vals[3]),
            ("Expiration (YYYY-MM-DD)",  row_vals[4]),
            ("Location",                 row_vals[5]),
        ]

        entries = {}
        for i, (label, default) in enumerate(plain_fields):
            tk.Label(dialog, text=label, anchor="w").grid(row=i, column=0, padx=10, pady=4, sticky="w")
            var = tk.StringVar(value=default)
            tk.Entry(dialog, textvariable=var, width=25).grid(row=i, column=1, padx=10, pady=4)
            entries[label] = var

        cat_row = len(plain_fields)
        tk.Label(dialog, text="Category", anchor="w").grid(row=cat_row, column=0, padx=10, pady=4, sticky="w")
        cat_var = tk.StringVar(value=row_vals[6] or "General")
        cat_options = ["General"] + inventory.get_all_categories()
        ttk.Combobox(dialog, textvariable=cat_var, values=cat_options,
                     state="readonly", width=23).grid(row=cat_row, column=1, padx=10, pady=4)

        vendor_row = cat_row + 1
        tk.Label(dialog, text="Vendor", anchor="w").grid(row=vendor_row, column=0, padx=10, pady=4, sticky="w")
        vendor_var = tk.StringVar(value=row_vals[7] or "Unknown")
        vendor_options = ["Unknown"] + inventory.get_all_vendor_names()
        ttk.Combobox(dialog, textvariable=vendor_var, values=vendor_options,
                     state="readonly", width=23).grid(row=vendor_row, column=1, padx=10, pady=4)

        def submit():
            name = entries["Name *"].get().strip()
            qty_str = entries["Quantity *"].get().strip()
            date_added = entries["Date Added (YYYY-MM-DD)"].get().strip() or None
            date_expired = entries["Expiration (YYYY-MM-DD)"].get().strip() or None
            location = entries["Location"].get().strip() or "Unknown"
            category = cat_var.get() or "General"
            vendor = vendor_var.get() or "Unknown"

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
                refresh_vendor_dropdown()
                refresh_location_dropdown()
                apply_filters()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        btn_row = vendor_row + 1
        tk.Button(dialog, text="Save", command=submit, width=10, bg="#5cb85c", fg="white").grid(row=btn_row, column=0, pady=10, padx=10)
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

    def open_manage_list_dialog(singular, get_all_fn, add_fn, rename_fn, delete_fn, delete_msg, refresh_fn=None):
        """Generic dialog for managing a named list (categories, vendors, locations)."""
        dialog = tk.Toplevel(root)
        dialog.title(f"Manage {singular}s")
        dialog.resizable(False, False)
        dialog.grab_set()
        center_on_parent(dialog, 320, 380)

        tk.Label(dialog, text=f"{singular}s", font=("", 10, "bold")).pack(pady=(12, 4))

        list_frame = tk.Frame(dialog)
        list_frame.pack(fill="both", expand=True, padx=16)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                             selectmode="single", height=12, width=30)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.pack(side="left", fill="both", expand=True)

        def refresh_list():
            listbox.delete(0, "end")
            for item in get_all_fn():
                listbox.insert("end", item)

        refresh_list()

        def do_add():
            add_dialog = tk.Toplevel(dialog)
            add_dialog.title(f"Add {singular}")
            add_dialog.resizable(False, False)
            add_dialog.grab_set()
            center_on_parent(add_dialog, 280, 110)

            tk.Label(add_dialog, text=f"{singular} Name:").grid(row=0, column=0, padx=10, pady=12, sticky="w")
            name_var = tk.StringVar()
            tk.Entry(add_dialog, textvariable=name_var, width=20).grid(row=0, column=1, padx=10, pady=12)

            def submit():
                name = name_var.get().strip()
                if not name:
                    messagebox.showerror("Error", "Name cannot be empty.", parent=add_dialog)
                    return
                try:
                    add_fn(name)
                    add_dialog.destroy()
                    refresh_list()
                    if refresh_fn:
                        refresh_fn()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=add_dialog)

            btn_frame = tk.Frame(add_dialog)
            btn_frame.grid(row=1, column=0, columnspan=2, pady=4)
            tk.Button(btn_frame, text="Add", command=submit, width=8).pack(side="left", padx=6)
            tk.Button(btn_frame, text="Cancel", command=add_dialog.destroy, width=8).pack(side="left", padx=6)

        def do_edit():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("No Selection", f"Please select a {singular.lower()} to edit.", parent=dialog)
                return
            old_name = listbox.get(sel[0])

            edit_dialog = tk.Toplevel(dialog)
            edit_dialog.title(f"Edit {singular}")
            edit_dialog.resizable(False, False)
            edit_dialog.grab_set()
            center_on_parent(edit_dialog, 280, 110)

            tk.Label(edit_dialog, text="New Name:").grid(row=0, column=0, padx=10, pady=12, sticky="w")
            name_var = tk.StringVar(value=old_name)
            tk.Entry(edit_dialog, textvariable=name_var, width=20).grid(row=0, column=1, padx=10, pady=12)

            def submit():
                new_name = name_var.get().strip()
                if not new_name:
                    messagebox.showerror("Error", "Name cannot be empty.", parent=edit_dialog)
                    return
                try:
                    rename_fn(old_name, new_name)
                    edit_dialog.destroy()
                    refresh_list()
                    if refresh_fn:
                        refresh_fn()
                    apply_filters()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=edit_dialog)

            btn_frame = tk.Frame(edit_dialog)
            btn_frame.grid(row=1, column=0, columnspan=2, pady=4)
            tk.Button(btn_frame, text="Save", command=submit, width=8).pack(side="left", padx=6)
            tk.Button(btn_frame, text="Cancel", command=edit_dialog.destroy, width=8).pack(side="left", padx=6)

        def do_delete():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("No Selection", f"Please select a {singular.lower()} to delete.", parent=dialog)
                return
            name = listbox.get(sel[0])
            if not messagebox.askyesno("Confirm Delete", delete_msg(name), parent=dialog):
                return
            try:
                delete_fn(name)
                refresh_list()
                if refresh_fn:
                    refresh_fn()
                apply_filters()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        btn_row = tk.Frame(dialog)
        btn_row.pack(pady=10)
        tk.Button(btn_row, text="Add",    command=do_add,    width=9, bg="#5cb85c", fg="white").pack(side="left", padx=5)
        tk.Button(btn_row, text="Edit",   command=do_edit,   width=9, bg="#337ab7", fg="white").pack(side="left", padx=5)
        tk.Button(btn_row, text="Delete", command=do_delete, width=9,
                  bg="#d9534f", fg="white").pack(side="left", padx=5)
        tk.Button(btn_row, text="Close",  command=dialog.destroy, width=9).pack(side="left", padx=5)

    def _delete_with_reset(del_fn, col, fallback):
        """Returns a delete callable that removes the registry entry and resets items."""
        def fn(name):
            del_fn(name)
            with database.get_connection() as conn:
                conn.cursor().execute(
                    f"UPDATE inventory SET {col} = ? WHERE {col} = ?", (fallback, name))
        return fn

    def open_manage_categories_dialog():
        open_manage_list_dialog(
            "Category",
            inventory.get_all_categories,
            inventory.new_category,
            inventory.rename_category,
            _delete_with_reset(inventory.delete_category, "category", "General"),
            lambda name: f"Delete category '{name}'?\n\nItems in this category will be set to 'General'.",
            refresh_fn=refresh_category_dropdown,
        )

    def open_manage_locations_dialog():
        open_manage_list_dialog(
            "Location",
            inventory.get_all_location_names,
            inventory.new_location,
            inventory.rename_location,
            _delete_with_reset(inventory.delete_location, "location", "Unknown"),
            lambda name: f"Delete location '{name}'?\n\nItems in this location will be set to 'Unknown'.",
            refresh_fn=refresh_location_dropdown,
        )

    def open_manage_vendors_dialog():
        open_manage_list_dialog(
            "Vendor",
            inventory.get_all_vendor_names,
            inventory.new_vendor_name,
            inventory.rename_vendor_name,
            _delete_with_reset(inventory.delete_vendor_name, "vendor", "Unknown"),
            lambda name: f"Delete vendor '{name}'?\n\nItems with this vendor will be set to 'Unknown'.",
            refresh_fn=refresh_vendor_dropdown,
        )

    def add_to_tobuy_list():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item to add to the To-Buy List.")
            return

        row_vals = tree.item(selected[0], "values")
        item_id = int(row_vals[0])
        item_name = row_vals[1]

        dialog = tk.Toplevel(root)
        dialog.title("Add to To-Buy List")
        dialog.resizable(False, False)
        dialog.grab_set()
        center_on_parent(dialog, 300, 120)

        tk.Label(dialog, text=f"Item: {item_name}", anchor="w").grid(row=0, column=0, columnspan=2, padx=14, pady=(12, 4), sticky="w")
        tk.Label(dialog, text="Qty to Buy:", anchor="w").grid(row=1, column=0, padx=14, pady=6, sticky="w")
        qty_var = tk.StringVar(value="1")
        tk.Entry(dialog, textvariable=qty_var, width=10).grid(row=1, column=1, padx=14, pady=6, sticky="w")

        def submit():
            try:
                qty = int(qty_var.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a whole number.", parent=dialog)
                return
            try:
                inventory.add_item_to_buy_list(item_id, qty)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="Add", command=submit, width=9).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy, width=9).pack(side="left", padx=6)

    def open_view_tobuy_dialog():
        dialog = tk.Toplevel(root)
        dialog.title("To-Buy List")
        dialog.resizable(False, False)
        dialog.grab_set()
        center_on_parent(dialog, 480, 380)

        # Button row packed first so it anchors to the bottom
        btn_row = tk.Frame(dialog)
        btn_row.pack(side="bottom", pady=10)

        # Tree area fills the rest
        tree_frame = tk.Frame(dialog)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        cols = ("ID", "Name", "In Stock", "Need to Buy")
        tree_buy = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse", height=12)
        for col, w in zip(cols, (40, 200, 80, 100)):
            tree_buy.heading(col, text=col)
            tree_buy.column(col, width=w, anchor="center" if col != "Name" else "w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_buy.yview)
        tree_buy.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree_buy.pack(fill="both", expand=True)

        def refresh():
            tree_buy.delete(*tree_buy.get_children())
            for row in (inventory.view_to_buy_list() or []):
                # row: (item_id, name, in_stock_qty, quantity_needed)
                tree_buy.insert("", "end", values=row)

        refresh()

        def remove_item():
            sel = tree_buy.selection()
            if not sel:
                messagebox.showwarning("No Selection", "Please select an item to delete.", parent=dialog)
                return
            item_id = int(tree_buy.item(sel[0], "values")[0])
            try:
                inventory.remove_item_from_to_buy_list(item_id)
                refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        def edit_quantity():
            sel = tree_buy.selection()
            if not sel:
                messagebox.showwarning("No Selection", "Please select an item to edit.", parent=dialog)
                return
            vals = tree_buy.item(sel[0], "values")
            item_id = int(vals[0])
            item_name = vals[1]
            current_qty = vals[3]

            eq_dialog = tk.Toplevel(dialog)
            eq_dialog.title("Edit Quantity")
            eq_dialog.resizable(False, False)
            eq_dialog.grab_set()
            center_on_parent(eq_dialog, 280, 110)

            tk.Label(eq_dialog, text=f"Item: {item_name}", anchor="w").grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 2), sticky="w")
            tk.Label(eq_dialog, text="Need to Buy:").grid(row=1, column=0, padx=10, pady=6, sticky="w")
            qty_var = tk.StringVar(value=current_qty)
            tk.Entry(eq_dialog, textvariable=qty_var, width=10).grid(row=1, column=1, padx=10, pady=6, sticky="w")

            def submit():
                try:
                    qty = int(qty_var.get().strip())
                except ValueError:
                    messagebox.showerror("Error", "Quantity must be a whole number.", parent=eq_dialog)
                    return
                try:
                    inventory.update_to_buy_quantity(item_id, qty)
                    eq_dialog.destroy()
                    refresh()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=eq_dialog)

            btn_f = tk.Frame(eq_dialog)
            btn_f.grid(row=2, column=0, columnspan=2, pady=6)
            tk.Button(btn_f, text="Save", command=submit, width=8).pack(side="left", padx=6)
            tk.Button(btn_f, text="Cancel", command=eq_dialog.destroy, width=8).pack(side="left", padx=6)

        def export_pdf():
            items = inventory.view_to_buy_list()
            if not items:
                messagebox.showinfo("Empty", "The To-Buy List is empty.", parent=dialog)
                return
            filename = simpledialog.askstring("Export PDF", "Enter filename (without extension):", parent=dialog)
            if not filename:
                return
            try:
                inventory.export_to_buy_list(filename)
                messagebox.showinfo("Exported", f"Saved as '{filename}.pdf'.", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        tk.Button(btn_row, text="Edit", command=edit_quantity, width=10).pack(side="left", padx=5)
        tk.Button(btn_row, text="Delete", command=remove_item, width=10,
                  bg="#d9534f", fg="white").pack(side="left", padx=5)
        tk.Button(btn_row, text="Export PDF", command=export_pdf, width=10).pack(side="left", padx=5)
        tk.Button(btn_row, text="Close", command=dialog.destroy, width=10).pack(side="left", padx=5)

    button_commands = {
        "Add Item": open_add_item_dialog,
        "Edit Item": open_edit_item_dialog,
        "Delete Item": open_delete_item_dialog,
        "Manage Categories": open_manage_categories_dialog,
        "Manage Vendors": open_manage_vendors_dialog,
        "Manage Locations": open_manage_locations_dialog,
        "View To-Buy List": open_view_tobuy_dialog,
        "Add to To-Buy List": add_to_tobuy_list,
        "Logout": root.destroy,
    }

    for label in ["Add Item", "Edit Item", "Delete Item",
                "Manage Categories", "Manage Vendors", "Manage Locations",
                "View To-Buy List", "Add to To-Buy List", "Logout"]:
        tk.Button(bot, text=label, width=14, command=button_commands.get(label)).pack(side="left", padx=3)

    # Size window after all widgets are packed so winfo_reqwidth is accurate
    root.update_idletasks()
    root.geometry(f"{max(root.winfo_reqwidth(), 900)}x600")

    root.mainloop()


def show_login_screen():
    """Displays login interface."""
    pass


def start_gui():
    """Creates and launches main application window."""
    show_inventory_screen()


if __name__ == "__main__":
    start_gui()
