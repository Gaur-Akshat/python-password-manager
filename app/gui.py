# app/gui.py
import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap import Style
from app.manager import create_password_entry, get_all_entries, get_password_by_id, delete_password_entry

class PasswordManagerApp(ttk.Window):
    SERVICE_NAME = "Service Name"
    USERNAME = "Username"
    ENCRYPTED_PASSWORD = "Encrypted Password"
    ID = "ID"

    def __init__(self):
        super().__init__(themename="minty")
        self.title("Password Manager")
        self.geometry("620x680")
        self.center_window()
        self.resizable(False, False)

        title_label = ttk.Label(self, text="Password Manager", font=("Helvetica", 18, "bold"), anchor="center")
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="n")

        ttk.Label(self, text=self.SERVICE_NAME, font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.service_entry = ttk.Entry(self, width=35, bootstyle="primary")
        self.service_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(self, text=self.USERNAME, font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.username_entry = ttk.Entry(self, width=35, bootstyle="primary")
        self.username_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(self, text="Password", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.password_entry = ttk.Entry(self, width=35, show="*", bootstyle="primary")
        self.password_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        add_button = ttk.Button(self, text="Add Password", command=self.add_password, bootstyle="success-outline", width=25)
        add_button.grid(row=4, column=0, columnspan=2, pady=15)
        add_button.bind("<Enter>", lambda e: add_button.config(bootstyle="success"))
        add_button.bind("<Leave>", lambda e: add_button.config(bootstyle="success-outline"))

        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.map("Treeview", background=[("selected", "#c4e17f")])

        # Adjust the padx to make the table aligned to the center
        self.tree = ttk.Treeview(self, columns=(self.ID, self.SERVICE_NAME, self.USERNAME, self.ENCRYPTED_PASSWORD), show='headings', height=8)
        self.tree.grid(row=5, column=0, columnspan=2, padx=60, pady=10)  # Increased padx for better centering
        self.tree.heading(self.ID, text=self.ID)
        self.tree.heading(self.SERVICE_NAME, text=self.SERVICE_NAME)
        self.tree.heading(self.USERNAME, text=self.USERNAME)
        self.tree.heading(self.ENCRYPTED_PASSWORD, text=self.ENCRYPTED_PASSWORD)
        self.tree.column(self.ID, width=0, stretch=False)
        self.tree.column(self.SERVICE_NAME, anchor="center", width=130)
        self.tree.column(self.USERNAME, anchor="center", width=130)
        self.tree.column(self.ENCRYPTED_PASSWORD, anchor="center", width=220)
        self.tree.tag_configure('odd', background='#f0f0f0')
        self.tree.tag_configure('even', background='#ffffff')
        self.tree.bind('<<TreeviewSelect>>', self.on_row_selected)

        self.delete_button = ttk.Button(self, text="✖", command=self.delete_entry, bootstyle="danger-link", width=2)
        self.delete_button.place_forget()  # Hide initially

        retrieve_button = ttk.Button(self, text="Retrieve Password", command=self.retrieve_password, bootstyle="info-outline", width=25)
        retrieve_button.grid(row=6, column=0, columnspan=2, pady=(5, 20))
        retrieve_button.grid_remove()
        retrieve_button.bind("<Enter>", lambda e: retrieve_button.config(bootstyle="info"))
        retrieve_button.bind("<Leave>", lambda e: retrieve_button.config(bootstyle="info-outline"))
        self.retrieve_button = retrieve_button

        self.load_entries()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def add_password(self):
        service_name = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if service_name and username and password:
            create_password_entry(service_name, username, password)
            self.load_entries()
            self.clear_fields()
            messagebox.showinfo("Success", "Password added successfully!")
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    def on_row_selected(self, event):
        if self.tree.selection():
            self.retrieve_button.grid()
            item = self.tree.selection()[0]
            bbox = self.tree.bbox(item)
            if bbox:
                x, y, width, _ = bbox
                self.delete_button.place(x=x + width + 50, y=y + self.tree.winfo_y())
        else:
            self.retrieve_button.grid_remove()
            self.delete_button.place_forget()

    def retrieve_password(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            entry_id = item['values'][0]
            password_entry = get_password_by_id(entry_id)
            if password_entry:
                _, decrypted_password, service_name, username = password_entry
                messagebox.showinfo("Password Retrieved", f"Service: {service_name}\nUsername: {username}\nPassword: {decrypted_password}")
            else:
                messagebox.showwarning("Error", "Service not found!")

    def delete_entry(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            entry_id = item['values'][0]
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this entry?")
            if confirm:
                delete_password_entry(entry_id)
                self.load_entries()
                messagebox.showinfo("Deleted", "Entry deleted successfully.")
                self.delete_button.place_forget()

    def load_entries(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        entries = get_all_entries()
        for i, entry in enumerate(entries):
            entry_id, service_name, username, encrypted_password = entry
            tag = 'odd' if i % 2 == 0 else 'even'
            self.tree.insert('', 'end', values=(entry_id, service_name, username, encrypted_password), tags=(tag,))

    def clear_fields(self):
        self.service_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

def run_app():
    app = PasswordManagerApp()
    app.mainloop()
