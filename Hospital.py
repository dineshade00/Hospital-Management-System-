import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime

# Constants for styling & files
COLOR_PRIMARY = "#007bff"
COLOR_SUCCESS = "#28a745"
COLOR_WARNING = "#ffc107"
COLOR_DANGER = "#dc3545"
COLOR_LIGHT = "#f8f9fa"
COLOR_DARK = "#343a40"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 11, "bold")

# Data file paths
DATA_PATHS = {
    "patients": "patients.json",
    "doctors": "doctors.json",
    "staff": "staff.json",
    "medicines": "medicines.json",
    "lab_tests": "lab_tests.json",
    "appointments": "appointments.json",
    "machinery": "machinery.json",
    "billing": "billing.json",
}

# Utility functions to load/save JSON
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

# Main Application Class
class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management System")
        self.geometry("1200x750")
        self.minsize(1100, 650)
        self.configure(bg=COLOR_LIGHT)

        # Style
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure("Treeview.Heading", font=FONT_BOLD, background=COLOR_PRIMARY, foreground="white")
        self.style.configure("Treeview", font=FONT, rowheight=25)
        self.style.map("Treeview", background=[('selected', COLOR_PRIMARY)])

        # Login system state
        self.current_user = None

        # Frames
        self.login_frame = LoginPage(self, self)
        self.login_frame.pack(fill="both", expand=True)

        self.main_frame = tk.Frame(self, bg=COLOR_LIGHT)
        # Sidebar & Content area
        self.sidebar = Sidebar(self.main_frame, self)
        self.sidebar.pack(side="left", fill="y")

        self.content_area = tk.Frame(self.main_frame, bg=COLOR_LIGHT)
        self.content_area.pack(side="right", fill="both", expand=True)

        # All Pages
        self.frames = {}
        for F in (DashboardPage, PatientManagementPage, DoctorManagementPage, StaffManagementPage,
                  MedicineManagementPage, LabTestManagementPage, AppointmentBookingPage,
                  MachineryManagementPage, BillingPage):
            page = F(self.content_area, self)
            self.frames[F] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.main_frame.pack_forget()

    def login_success(self):
        self.login_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.show_frame(DashboardPage)
        self.sidebar.activate_button("Dashboard")

    def logout(self):
        self.main_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)
        self.current_user = None

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()

# Login Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_LIGHT)
        self.controller = controller

        box = tk.Frame(self, bg="white", bd=2, relief="groove")
        box.place(relx=0.5, rely=0.5, anchor="center", width=350, height=280)

        tk.Label(box, text="Hospital Management Login", font=("Segoe UI", 16, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=20)

        tk.Label(box, text="Username", font=FONT, bg="white").pack(pady=(10,0))
        self.username_entry = tk.Entry(box, font=FONT)
        self.username_entry.pack(ipady=5, fill="x", padx=30)

        tk.Label(box, text="Password", font=FONT, bg="white").pack(pady=(10,0))
        self.password_entry = tk.Entry(box, font=FONT, show="*")
        self.password_entry.pack(ipady=5, fill="x", padx=30)

        login_btn = tk.Button(box, text="Login", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="white",
                              activebackground="#0056b3", activeforeground="white", bd=0,
                              command=self.check_login)
        login_btn.pack(pady=25, ipadx=10, ipady=5)

    def check_login(self):
        # Very basic user/password for demo; extend with real users
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin123":
            self.controller.current_user = username
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.controller.login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Sidebar with navigation buttons
class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_DARK, width=220)
        self.controller = controller
        self.pack_propagate(False)

        self.buttons = {}

        title = tk.Label(self, text="Admin Panel", font=("Segoe UI", 16, "bold"),
                         bg=COLOR_DARK, fg="white", pady=20)
        title.pack()

        # Modules Buttons
        self.add_button("Dashboard", lambda: self.on_button_click(DashboardPage, "Dashboard"))
        self.add_button("Patients", lambda: self.on_button_click(PatientManagementPage, "Patients"))
        self.add_button("Doctors", lambda: self.on_button_click(DoctorManagementPage, "Doctors"))
        self.add_button("Staff", lambda: self.on_button_click(StaffManagementPage, "Staff"))
        self.add_button("Medicines", lambda: self.on_button_click(MedicineManagementPage, "Medicines"))
        self.add_button("Laboratory", lambda: self.on_button_click(LabTestManagementPage, "Laboratory"))
        self.add_button("Appointments", lambda: self.on_button_click(AppointmentBookingPage, "Appointments"))
        self.add_button("Machinery", lambda: self.on_button_click(MachineryManagementPage, "Machinery"))
        self.add_button("Billing", lambda: self.on_button_click(BillingPage, "Billing"))
        self.add_button("Logout", self.controller.logout)

    def add_button(self, text, command):
        btn = tk.Button(self, text=text, font=FONT_BOLD, bg=COLOR_DARK, fg="white",
                        activebackground=COLOR_PRIMARY, activeforeground="white",
                        bd=0, relief="flat", pady=12, command=command)
        btn.pack(fill="x", padx=10, pady=5)
        self.buttons[text] = btn

    def on_button_click(self, page, name):
        self.controller.show_frame(page)
        self.activate_button(name)

    def activate_button(self, name):
        for btn_name, btn in self.buttons.items():
            if btn_name == name:
                btn.configure(bg=COLOR_PRIMARY)
            else:
                btn.configure(bg=COLOR_DARK)

# Dashboard with summary cards and live time
class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_LIGHT)
        self.controller = controller

        header = tk.Label(self, text="Dashboard", font=("Segoe UI", 20, "bold"), bg=COLOR_LIGHT)
        header.pack(pady=15)

        self.cards_frame = tk.Frame(self, bg=COLOR_LIGHT)
        self.cards_frame.pack(pady=20, padx=20, fill="x")

        # Create summary cards dynamically
        self.cards = {}
        card_infos = [
            ("Patients", COLOR_PRIMARY),
            ("Doctors", COLOR_SUCCESS),
            ("Staff", COLOR_WARNING),
            ("Medicines", COLOR_DANGER),
            ("Appointments", "#17a2b8"),  # info color
            ("Available Beds", "#6c757d"),
            ("Machinery", "#fd7e14"),
        ]

        for i, (title, color) in enumerate(card_infos):
            card = tk.Frame(self.cards_frame, bg=color, width=160, height=100, bd=0, relief="ridge")
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            card.pack_propagate(False)

            label_title = tk.Label(card, text=title, font=FONT_BOLD, bg=color, fg="white")
            label_title.pack(pady=(10, 0))

            label_value = tk.Label(card, text="0", font=("Segoe UI", 28, "bold"), bg=color, fg="white")
            label_value.pack(expand=True)

            self.cards[title] = label_value

        # Live clock
        self.clock_label = tk.Label(self, font=("Segoe UI", 14, "bold"), bg=COLOR_LIGHT, fg=COLOR_DARK)
        self.clock_label.pack(pady=10)
        self.update_clock()

        self.update_stats()

    def update_stats(self):
        self.cards["Patients"].config(text=str(len(load_data(DATA_PATHS["patients"]))))
        self.cards["Doctors"].config(text=str(len(load_data(DATA_PATHS["doctors"]))))
        self.cards["Staff"].config(text=str(len(load_data(DATA_PATHS["staff"]))))
        self.cards["Medicines"].config(text=str(len(load_data(DATA_PATHS["medicines"]))))
        self.cards["Appointments"].config(text=str(len(load_data(DATA_PATHS["appointments"]))))
        self.cards["Machinery"].config(text=str(len(load_data(DATA_PATHS["machinery"]))))
        # Beds static for demo
        self.cards["Available Beds"].config(text="15")

    def update_clock(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=f"Current Date & Time: {now}")
        self.after(1000, self.update_clock)

    def refresh(self):
        self.update_stats()

# Base management page template for Patients, Doctors, Staff, Medicines, Lab Tests, Machinery
class BaseManagementPage(tk.Frame):
    def __init__(self, parent, controller, title, fields, data_key):
        super().__init__(parent, bg=COLOR_LIGHT)
        self.controller = controller
        self.title_text = title
        self.fields = fields  # List of (field_label, field_width)
        self.data_key = data_key

        header = tk.Label(self, text=title, font=("Segoe UI", 20, "bold"), bg=COLOR_LIGHT)
        header.pack(pady=15)

        content = tk.Frame(self, bg=COLOR_LIGHT)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: Form
        form_frame = tk.Frame(content, bg="white", bd=1, relief="solid")
        form_frame.pack(side="left", fill="y", padx=(0, 15), ipadx=10, ipady=10)

        tk.Label(form_frame, text=f"Add New {title[:-1]}", font=FONT_BOLD, bg="white").grid(row=0, column=0, columnspan=2, pady=10)

        self.entries = {}
        for i, (field, width) in enumerate(fields):
            tk.Label(form_frame, text=f"{field}:", bg="white").grid(row=i+1, column=0, sticky="e", pady=5, padx=5)
            entry = tk.Entry(form_frame, font=FONT, width=width)
            entry.grid(row=i+1, column=1, pady=5, padx=5)
            self.entries[field.lower()] = entry

        add_btn = tk.Button(form_frame, text=f"Add {title[:-1]}", bg=COLOR_PRIMARY, fg="white", font=FONT_BOLD,
                            bd=0, padx=10, pady=5, command=self.add_record)
        add_btn.grid(row=len(fields)+1, column=0, columnspan=2, pady=15)

        # Right: Table
        table_frame = tk.Frame(content, bg="white", bd=1, relief="solid")
        table_frame.pack(side="right", fill="both", expand=True)

        cols = [f[0] for f in fields]
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Delete button
        del_btn = tk.Button(self, text=f"Delete Selected {title[:-1]}", bg=COLOR_DANGER, fg="white",
                            font=FONT_BOLD, bd=0, padx=10, pady=5, command=self.delete_record)
        del_btn.pack(pady=10)

        self.load_records()

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = load_data(DATA_PATHS[self.data_key])
        for rec in records:
            values = [rec.get(f.lower(), "") for f, _ in self.fields]
            self.tree.insert("", "end", values=values)

    def add_record(self):
        # Validate inputs
        record = {}
        for field, _ in self.fields:
            val = self.entries[field.lower()].get().strip()
            if not val:
                messagebox.showerror("Error", f"{field} is required")
                return
            record[field.lower()] = val

        # Example: age and numeric fields check (you can customize per field)
        if "age" in record and not record["age"].isdigit():
            messagebox.showerror("Error", "Age must be a number")
            return
        if "quantity" in record and not record["quantity"].isdigit():
            messagebox.showerror("Error", "Quantity must be a number")
            return
        if "price" in record and not self.is_float(record["price"]):
            messagebox.showerror("Error", "Price must be a number")
            return

        # Save
        records = load_data(DATA_PATHS[self.data_key])
        records.append(record)
        save_data(DATA_PATHS[self.data_key], records)
        self.load_records()

        for e in self.entries.values():
            e.delete(0, tk.END)
        messagebox.showinfo("Success", f"{self.title_text[:-1]} added successfully")

    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", f"No {self.title_text[:-1]} selected")
            return
        values = self.tree.item(selected[0], "values")
        records = load_data(DATA_PATHS[self.data_key])
        # Filter out matching record
        def match(r): 
            return all(str(r.get(f.lower(), "")) == v for f, v in zip(self.fields, values))
        new_records = []
        for r in records:
            if any(str(r.get(f[0].lower(), "")) != val for f, val in zip(self.fields, values)):
                new_records.append(r)
        save_data(DATA_PATHS[self.data_key], new_records)
        self.load_records()
        messagebox.showinfo("Success", f"{self.title_text[:-1]} deleted successfully")

    def is_float(self, value):
        try:
            float(value)
            return True
        except:
            return False

    def refresh(self):
        self.load_records()

# Specific Management Pages
class PatientManagementPage(BaseManagementPage):
    def __init__(self, parent, controller):
        fields = [("Name", 30), ("Age", 10), ("Disease", 30)]
        super().__init__(parent, controller, "Patients", fields, "patients")

class DoctorManagementPage(BaseManagementPage):
    def __init__(self, parent, controller):
        fields = [("Name", 30), ("Specialization", 30), ("Phone", 20)]
        super().__init__(parent, controller, "Doctors", fields, "doctors")

class StaffManagementPage(BaseManagementPage):
    def __init__(self, parent, controller):
        fields = [("Name", 30), ("Role", 30), ("Phone", 20)]
        super().__init__(parent, controller, "Staff", fields, "staff")

class MedicineManagementPage(BaseManagementPage):
    def __init__(self, parent, controller):
        fields = [("Name", 30), ("Quantity", 10), ("Price", 10)]
        super().__init__(parent, controller, "Medicines", fields, "medicines")

class LabTestManagementPage(BaseManagementPage):
    def __init__(self, parent, controller):
        fields = [("Test Name", 30), ("Price", 10)]
        super().__init__(parent, controller, "Lab Tests", fields, "lab_tests")

class MachineryManagementPage(BaseManagementPage):
    def __init__(self, parent, controller):
        fields = [("Machine Name", 30), ("Quantity", 10), ("Supplier", 30)]
        super().__init__(parent, controller, "Machinery", fields, "machinery")

# Appointment Booking Page
class AppointmentBookingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_LIGHT)
        self.controller = controller

        header = tk.Label(self, text="Book Doctor Appointment", font=("Segoe UI", 20, "bold"), bg=COLOR_LIGHT)
        header.pack(pady=15)

        content = tk.Frame(self, bg=COLOR_LIGHT)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        form_frame = tk.Frame(content, bg="white", bd=1, relief="solid")
        form_frame.pack(side="left", fill="y", padx=(0, 15), ipadx=10, ipady=10)

        tk.Label(form_frame, text="Patient Name:", bg="white").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.patient_name_entry = tk.Entry(form_frame, width=30)
        self.patient_name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Select Doctor:", bg="white").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.doctor_combo = ttk.Combobox(form_frame, width=28, state="readonly")
        self.doctor_combo.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="white").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.date_entry = tk.Entry(form_frame, width=30)
        self.date_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Time (HH:MM):", bg="white").grid(row=3, column=0, sticky="e", pady=5, padx=5)
        self.time_entry = tk.Entry(form_frame, width=30)
        self.time_entry.grid(row=3, column=1, pady=5, padx=5)

        book_btn = tk.Button(form_frame, text="Book Appointment", bg=COLOR_PRIMARY, fg="white", font=FONT_BOLD,
                             bd=0, padx=10, pady=5, command=self.book_appointment)
        book_btn.grid(row=4, column=0, columnspan=2, pady=15)

        # Right side - Appointments List
        list_frame = tk.Frame(content, bg="white", bd=1, relief="solid")
        list_frame.pack(side="right", fill="both", expand=True)

        columns = ("patient", "doctor", "date", "time")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        del_btn = tk.Button(self, text="Delete Selected Appointment", bg=COLOR_DANGER, fg="white",
                            font=FONT_BOLD, bd=0, padx=10, pady=5, command=self.delete_appointment)
        del_btn.pack(pady=10)

        self.refresh()

    def refresh(self):
        # Update doctor list in combobox
        doctors = load_data(DATA_PATHS["doctors"])
        self.doctor_combo['values'] = [d.get("name", "") for d in doctors]

        # Load appointments
        self.load_appointments()

    def load_appointments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        appointments = load_data(DATA_PATHS["appointments"])
        for appt in appointments:
            self.tree.insert("", "end", values=(appt.get("patient name", ""), appt.get("doctor", ""),
                                                appt.get("date", ""), appt.get("time", "")))

    def book_appointment(self):
        patient = self.patient_name_entry.get().strip()
        doctor = self.doctor_combo.get().strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()

        if not patient or not doctor or not date or not time:
            messagebox.showerror("Error", "All fields are required")
            return

        # Simple date and time format validation
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format")
            return
        try:
            datetime.datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Time must be in HH:MM format")
            return

        # Save appointment
        appointments = load_data(DATA_PATHS["appointments"])
        appointments.append({
            "patient name": patient,
            "doctor": doctor,
            "date": date,
            "time": time
        })
        save_data(DATA_PATHS["appointments"], appointments)
        messagebox.showinfo("Success", "Appointment booked successfully")
        self.patient_name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.load_appointments()

    def delete_appointment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No appointment selected")
            return
        values = self.tree.item(selected[0], "values")
        appointments = load_data(DATA_PATHS["appointments"])
        new_appointments = [a for a in appointments if not (
            a.get("patient name") == values[0] and a.get("doctor") == values[1]
            and a.get("date") == values[2] and a.get("time") == values[3]
        )]
        save_data(DATA_PATHS["appointments"], new_appointments)
        self.load_appointments()
        messagebox.showinfo("Success", "Appointment deleted successfully")

# Billing Page (simplified)
class BillingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_LIGHT)
        self.controller = controller

        header = tk.Label(self, text="Medical Billing", font=("Segoe UI", 20, "bold"), bg=COLOR_LIGHT)
        header.pack(pady=15)

        content = tk.Frame(self, bg=COLOR_LIGHT)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        form_frame = tk.Frame(content, bg="white", bd=1, relief="solid")
        form_frame.pack(side="left", fill="y", padx=(0, 15), ipadx=10, ipady=10)

        # Patient Name
        tk.Label(form_frame, text="Patient Name:", bg="white").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.patient_entry = tk.Entry(form_frame, width=30)
        self.patient_entry.grid(row=0, column=1, pady=5, padx=5)

        # Medicine selection with price display
        tk.Label(form_frame, text="Select Medicine:", bg="white").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.medicine_combo = ttk.Combobox(form_frame, width=28, state="readonly")
        self.medicine_combo.grid(row=1, column=1, pady=5, padx=5)
        self.medicine_combo.bind("<<ComboboxSelected>>", self.show_price)

        tk.Label(form_frame, text="Price:", bg="white").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.price_var = tk.StringVar()
        self.price_label = tk.Label(form_frame, textvariable=self.price_var, bg="white")
        self.price_label.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Quantity:", bg="white").grid(row=3, column=0, sticky="e", pady=5, padx=5)
        self.quantity_entry = tk.Entry(form_frame, width=30)
        self.quantity_entry.grid(row=3, column=1, pady=5, padx=5)

        bill_btn = tk.Button(form_frame, text="Generate Bill", bg=COLOR_PRIMARY, fg="white", font=FONT_BOLD,
                             bd=0, padx=10, pady=5, command=self.generate_bill)
        bill_btn.grid(row=4, column=0, columnspan=2, pady=15)

        # Billing List
        list_frame = tk.Frame(content, bg="white", bd=1, relief="solid")
        list_frame.pack(side="right", fill="both", expand=True)

        columns = ("patient", "medicine", "quantity", "price", "total")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        del_btn = tk.Button(self, text="Delete Selected Bill", bg=COLOR_DANGER, fg="white",
                            font=FONT_BOLD, bd=0, padx=10, pady=5, command=self.delete_bill)
        del_btn.pack(pady=10)

        self.load_medicines()
        self.load_bills()

    def load_medicines(self):
        medicines = load_data(DATA_PATHS["medicines"])
        self.medicine_combo['values'] = [m.get("name", "") for m in medicines]
        self.medicines_data = {m.get("name", ""): m for m in medicines}

    def show_price(self, event=None):
        med_name = self.medicine_combo.get()
        if med_name in self.medicines_data:
            self.price_var.set(self.medicines_data[med_name].get("price", "0"))
        else:
            self.price_var.set("")

    def generate_bill(self):
        patient = self.patient_entry.get().strip()
        medicine = self.medicine_combo.get().strip()
        quantity = self.quantity_entry.get().strip()
        if not patient or not medicine or not quantity:
            messagebox.showerror("Error", "All fields are required")
            return
        if not quantity.isdigit():
            messagebox.showerror("Error", "Quantity must be a number")
            return

        price = float(self.price_var.get())
        qty = int(quantity)
        total = price * qty

        bills = load_data(DATA_PATHS["billing"])
        bills.append({
            "patient": patient,
            "medicine": medicine,
            "quantity": qty,
            "price": price,
            "total": total
        })
        save_data(DATA_PATHS["billing"], bills)
        messagebox.showinfo("Success", "Bill generated successfully")

        self.patient_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.load_bills()

    def load_bills(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        bills = load_data(DATA_PATHS["billing"])
        for b in bills:
            self.tree.insert("", "end", values=(b.get("patient"), b.get("medicine"),
                                                b.get("quantity"), b.get("price"), b.get("total")))

    def delete_bill(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No bill selected")
            return
        values = self.tree.item(selected[0], "values")
        bills = load_data(DATA_PATHS["billing"])
        new_bills = [b for b in bills if not (
            b.get("patient") == values[0] and b.get("medicine") == values[1]
            and str(b.get("quantity")) == values[2] and str(b.get("price")) == values[3]
            and str(b.get("total")) == values[4]
        )]
        save_data(DATA_PATHS["billing"], new_bills)
        self.load_bills()
        messagebox.showinfo("Success", "Bill deleted successfully")

# Run application
if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()
