import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class EnterpriseApp(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Enterprise Manager & Employee Portal")
        self.geometry("850x650")
        
        # Datasets
        # Users: Username -> (Password, Role)
        self.users_db = {"admin": ("admin", "Manager")}
        # Sales Data: list of dicts
        self.sales_data = []
        self.current_employee = ""
        
        # Temporary storage before consumer page submission
        self.temp_data = {}

        # Container for screens (Frames)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (RoleSelection, ManagerLogin, EmployeeLogin, ManagerDashboard, EmployeeDashboard, ConsumerData):
            page_name = F._name_
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RoleSelection")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

class RoleSelection(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller
        
        label = tk.Label(self, text="Choose your role:", font=("Arial", 22))
        label.pack(pady=50)
        
        btn_manager = tk.Button(self, text="Manager Login", font=("Arial", 14), width=18, height=2,
                                command=lambda: controller.show_frame("ManagerLogin"))
        btn_manager.pack(pady=15)
        
        btn_employee = tk.Button(self, text="Employee Login", font=("Arial", 14), width=18, height=2,
                                 command=lambda: controller.show_frame("EmployeeLogin"))
        btn_employee.pack(pady=15)

class ManagerLogin(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller
        
        tk.Label(self, text="Manager Login", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self, text="Username", font=("Arial", 12)).pack(pady=5)
        self.user_entry = tk.Entry(self, font=("Arial", 12), width=25)
        self.user_entry.pack(pady=5)
        
        tk.Label(self, text="Password", font=("Arial", 12)).pack(pady=5)
        self.pass_entry = tk.Entry(self, show="*", font=("Arial", 12), width=25)
        self.pass_entry.pack(pady=5)
        
        self.lamp = tk.Canvas(self, width=20, height=20)
        self.lamp.pack(pady=10)
        self.lamp_circle = self.lamp.create_oval(2, 2, 18, 18, fill="gray")
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Enter", font=("Arial", 12), width=10, command=self.login).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Return", font=("Arial", 12), width=10, 
                  command=lambda: controller.show_frame("RoleSelection")).pack(side="left", padx=10)

    def login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        if u in self.controller.users_db and self.controller.users_db[u] == (p, "Manager"):
            self.lamp.itemconfig(self.lamp_circle, fill="green")
            self.after(500, lambda: self.controller.show_frame("ManagerDashboard"))
        else:
            self.lamp.itemconfig(self.lamp_circle, fill="red")
            messagebox.showerror("Login Error", "Invalid Manager credentials.")

class EmployeeLogin(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller
        
        tk.Label(self, text="Employee Login / Signup", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self, text="Username", font=("Arial", 12)).pack(pady=5)
        self.user_entry = tk.Entry(self, font=("Arial", 12), width=25)
        self.user_entry.pack(pady=5)
        
        tk.Label(self, text="Password", font=("Arial", 12)).pack(pady=5)
        self.pass_entry = tk.Entry(self, show="*", font=("Arial", 12), width=25)
        self.pass_entry.pack(pady=5)
        
        self.lamp = tk.Canvas(self, width=20, height=20)
        self.lamp.pack(pady=10)
        self.lamp_circle = self.lamp.create_oval(2, 2, 18, 18, fill="gray")
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Enter", font=("Arial", 12), width=10, command=self.login).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Return", font=("Arial", 12), width=10, 
                  command=lambda: controller.show_frame("RoleSelection")).pack(side="left", padx=10)

    def login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        if not u or not p:
            messagebox.showerror("Input Error", "Username and Password cannot be empty.")
            return

        if u in self.controller.users_db:
            saved_p, role = self.controller.users_db[u]
            if saved_p == p and role == "Employee":
                self.lamp.itemconfig(self.lamp_circle, fill="green")
                self.controller.current_employee = u
                self.after(500, lambda: self.controller.show_frame("EmployeeDashboard"))
            else:
                self.lamp.itemconfig(self.lamp_circle, fill="red")
                messagebox.showerror("Login Error", "Wrong password or invalid account.")
        else:
            self.controller.users_db[u] = (p, "Employee")
            self.lamp.itemconfig(self.lamp_circle, fill="green")
            self.controller.current_employee = u
            messagebox.showinfo("Sign Up Success", "Account created and registered successfully!")
            self.controller.show_frame("EmployeeDashboard")

class ManagerDashboard(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller
        
        # Header Control Panel
        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=15, pady=15)
        
        tk.Label(top_frame, text="Employee:", font=("Arial", 12)).pack(side="left", padx=5)
        self.emp_dropdown = ttk.Combobox(top_frame, state="readonly", font=("Arial", 11), width=15)
        self.emp_dropdown.pack(side="left", padx=5)
        self.emp_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_dashboard())
        
        tk.Button(top_frame, text="Logout", font=("Arial", 11), command=self.logout).pack(side="right", padx=5)
        
        # Main Display split
        main_display = tk.Frame(self)
        main_display.pack(side="bottom", fill="both", expand=True, padx=15, pady=5)
        
        # Left Side: Treeview Table
        self.table_frame = tk.Frame(main_display)
        self.table_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        columns = ("Shamsi Date", "Product", "PR", "Status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor="center")
        self.tree.pack(fill="both", expand=True)
        
        # Right Side: Matplotlib Trend Plot
        self.plot_frame = tk.Frame(main_display)
        self.plot_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        self.fig = Figure(figsize=(4, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def on_show(self):
        employees = [u for u, (p, r) in self.controller.users_db.items() if r == "Employee"]
        if not employees:
            self.emp_dropdown["values"] = ["None"]
            self.emp_dropdown.set("None")
        else:
            self.emp_dropdown["values"] = employees
            self.emp_dropdown.set(employees[0])
        self.update_dashboard()

    def update_dashboard(self):
        selected_emp = self.emp_dropdown.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.ax.clear()
        self.canvas.draw()
        
        if selected_emp == "None" or not selected_emp:
            return
            
        emp_records = [r for r in self.controller.sales_data if r["Employee"] == selected_emp]
        for r in emp_records:
            self.tree.insert("", "end", values=(r["ShamsiDate"], r["Product"], r["PR"], r["Status"]))
            
        if not emp_records:
            return
            
        # Draw CR Trend Line
        days_data = {}
        for r in emp_records:
            try:
                day = int(r["ShamsiDate"].split("/")[2])
                if day not in days_data:
                    days_data[day] = []
                days_data[day].append(r["Status"])
            except:
                continue
                
        sorted_days = sorted(days_data.keys())
        cr_values = []
        
        for d in sorted_days:
            cumulative_statuses = []
            for cd in sorted_days:
                if cd <= d:
                    cumulative_statuses.extend(days_data[cd])
            sold_count = cumulative_statuses.count("Sold")
            lead_count = cumulative_statuses.count("Lead")
            total = sold_count + lead_count
            cr_values.append((sold_count / total * 100) if total > 0 else 0)
            
        if sorted_days:
            self.ax.plot(sorted_days, cr_values, "-o", color="#D95319", linewidth=2)
            self.ax.set_xlabel("Day of Shamsi Month")
            self.ax.set_ylabel("Conversion Rate (CR %)")
            self.ax.set_title(f"Cumulative CR Trend for {selected_emp}")
            self.ax.set_ylim(-5, 105)
            self.ax.grid(True)
            self.canvas.draw()

    def logout(self):
        self.controller.show_frame("RoleSelection")

class EmployeeDashboard(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller
        
        self.welcome_label = tk.Label(self, text="Welcome", font=("Arial", 16, "bold"))
        self.welcome_label.pack(anchor="w", padx=20, pady=15)
        
        # Shamsi Date selectors
        date_frame = tk.Frame(self)
        date_frame.pack(pady=15)
        tk.Label(date_frame, text="Date (Shamsi):", font=("Arial", 11)).pack(side="left", padx=5)
        self.year_sel = ttk.Combobox(date_frame, values=["1405", "1406", "1407", "1408"], width=6, state="readonly")
        self.year_sel.set("1405")
        self.year_sel.pack(side="left", padx=2)
        self.month_sel = ttk.Combobox(date_frame, values=[str(i) for i in range(1, 13)], width=4, state="readonly")
        self.month_sel.set("1")
        self.month_sel.pack(side="left", padx=2)
        self.day_sel = ttk.Combobox(date_frame, values=[str(i) for i in range(1, 32)], width=4, state="readonly")
        self.day_sel.set("1")
        self.day_sel.pack(side="left", padx=2)
        
        # Product selector
        prod_frame = tk.Frame(self)
        prod_frame.pack(pady=15)
        tk.Label(prod_frame, text="Product:", font=("Arial", 11)).pack(side="left", padx=5)
        self.prod_sel = ttk.Combobox(prod_frame, values=["Simazar", "Andokhte dar", "Omid", "Finora/ Zarnova"], width=20, state="readonly")
        self.prod_sel.set("Simazar")
        self.prod_sel.pack(side="left", padx=5)
        
        # Status Switch
        status_frame = tk.Frame(self)
        status_frame.pack(pady=15)
        tk.Label(status_frame, text="Status:", font=("Arial", 11)).pack(side="left", padx=5)
        self.status_var = tk.StringVar(value="Lead")
        self.switch_btn = tk.Button(status_frame, text="Sale in progress", font=("Arial", 11, "bold"), 
                                    bg="#f0f0f0", command=self.toggle_switch, width=22)
        self.switch_btn.pack(side="left", padx=5)
        
        # Investment field
        self.invest_frame = tk.Frame(self)
        self.invest_frame.pack(pady=15)
        tk.Label(self.invest_frame, text="Investment:", font=("Arial", 11)).pack(side="left", padx=5)
        self.invest_entry = tk.Entry(self.invest_frame, font=("Arial", 11), width=15, state="disabled")
        self.invest_entry.pack(side="left", padx=2)
        self.rial_lbl = tk.Label(self.invest_frame, text="ریال", font=("Arial", 12, "bold"))
        self.rial_lbl.pack(side="left", padx=5)
        
        # Navigation
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=30)
        tk.Button(btn_frame, text="Consumer Data", font=("Arial", 12, "bold"), bg="#007ACC", fg="white", 
                  width=15, height=2, command=self.go_to_consumer).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Logout", font=("Arial", 11), command=self.logout).pack(side="left", padx=15)

    def on_show(self):
        self.welcome_label.config(text=f"Welcome, {self.controller.current_employee}")
        self.invest_entry.config(state="disabled")
        self.invest_entry.delete(0, tk.END)
        self.status_var.set("Lead")
        self.switch_btn.config(text="Sale in progress", bg="#f0f0f0")

    def toggle_switch(self):
        if self.status_var.get() == "Lead":
            self.status_var.set("Sold")
            self.switch_btn.config(text="Submit Successful Sale", bg="#D4EDDA")
            self.invest_entry.config(state="normal")
        else:
            self.status_var.set("Lead")
            self.switch_btn.config(text="Sale in progress", bg="#f0f0f0")
            self.invest_entry.config(state="disabled")
            self.invest_entry.delete(0, tk.END)

    def go_to_consumer(self):
        status = self.status_var.get()
        invest_val = 0
        
        if status == "Sold":
            try:
                invest_val = float(self.invest_entry.get())
                if invest_val <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Validation Error", "Please enter a valid investment amount.")
                return
                
        # Temp save setup
        shamsi_date = f"{self.year_sel.get()}/{int(self.month_sel.get()):02d}/{int(self.day_sel.get()):02d}"
        self.controller.temp_data = {
            "ShamsiDate": shamsi_date,
            "Employee": self.controller.current_employee,
            "Product": self.prod_sel.get(),
            "Investment": invest_val,
            "Status": status
        }
        self.controller.show_frame("ConsumerData")

    def logout(self):
        self.controller.show_frame("RoleSelection")

class ConsumerData(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent)
        self.controller = controller
        
        tk.Label(self, text="Enter Customer Specifications", font=("Arial", 18, "bold")).pack(pady=25)
        
        tk.Label(self, text="Customer Name", font=("Arial", 11)).pack(pady=5)
        self.name_entry = tk.Entry(self, font=("Arial", 11), width=30)
        self.name_entry.pack(pady=5)
        
        tk.Label(self, text="Phone Number", font=("Arial", 11)).pack(pady=5)
        self.phone_entry = tk.Entry(self, font=("Arial", 11), width=30)
        self.phone_entry.pack(pady=5)
        
        tk.Label(self, text="Notes", font=("Arial", 11)).pack(pady=5)
        self.notes_text = tk.Text(self, font=("Arial", 11), width=30, height=5)
        self.notes_text.pack(pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Submit", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
                  width=10, command=self.submit).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Cancel", font=("Arial", 11), width=10, 
                  command=lambda: controller.show_frame("EmployeeDashboard")).pack(side="left", padx=15)

    def on_show(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)

    def submit(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        if not name or not phone:
            messagebox.showerror("Input Error", "Customer Name and Phone are required.")
            return
            
        temp = self.controller.temp_data
        invest = temp["Investment"]
        prod = temp["Product"]
        
        # Calculate PR Portfolio value
        if prod in ["Simazar", "Andokhte dar", "Omid"]:
            pr = invest
        elif prod in ["Finora/ Zarnova", "Finora", "Zarnova"]:
            pr = 0.40 * invest
        else:
            pr = 0
            
        new_row = {
            "ShamsiDate": temp["ShamsiDate"],
            "Employee": temp["Employee"],
            "Product": prod,
            "Investment": invest,
            "PR": pr,
            "Status": temp["Status"],
            "CustomerName": name,
            "CustomerPhone": phone,
            "CustomerNotes": notes
        }
        
        self.controller.sales_data.append(new_row)
        messagebox.showinfo("Success", "Data and Customer details registered successfully!")
        self.controller.show_frame("EmployeeDashboard")

if _name_ == "_main_":
    app = EnterpriseApp()
    app.mainloop()
