import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import datetime
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

# Simulate user data
user_data = {
    "admin": "admin123",
    "user": "password",
}

# List to hold accident reports
accident_reports = []


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Road Safety App")
        self.geometry("400x400")
        self.current_user = None

        self.login_frame = LoginFrame(self)
        self.home_frame = HomeFrame(self)

        self.show_frame("login")

    def show_frame(self, frame_name):
        if frame_name == "login":
            self.login_frame.tkraise()
        elif frame_name == "home":
            self.home_frame.tkraise()


class LoginFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Login Page", font=("Arial", 14))
        label.pack(pady=20)

        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.insert(0, "Username")
        self.username_entry.pack(pady=10)

        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.insert(0, "Password")
        self.password_entry.pack(pady=10)

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in user_data and user_data[username] == password:
            self.parent.current_user = username
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            self.parent.show_frame("home")
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")


class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Home Page", font=("Arial", 14))
        label.pack(pady=20)

        add_accident_button = tk.Button(self, text="Add Accident", command=self.add_accident)
        add_accident_button.pack(pady=10)

        logout_button = tk.Button(self, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

        show_reports_button = tk.Button(self, text="Show Accident Reports", command=self.show_reports)
        show_reports_button.pack(pady=10)

        show_on_map_button = tk.Button(self, text="Show Accidents on Map", command=self.show_on_map)
        show_on_map_button.pack(pady=10)

    def add_accident(self):
        location = simpledialog.askstring("Add Accident", "Enter the location of the accident:")
        severity = simpledialog.askstring("Add Accident", "Enter the severity (low/medium/high):")
        description = simpledialog.askstring("Add Accident", "Enter a brief description:")

        if location and severity and description:
            report = {
                "report_id": random.randint(1000, 9999),
                "timestamp": datetime.datetime.now().isoformat(),
                "location": location,
                "severity": severity,
                "description": description,
                "reported_by": self.parent.current_user,
            }
            accident_reports.append(report)
            messagebox.showinfo("Success", "Accident reported successfully!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def show_reports(self):
        if not accident_reports:
            messagebox.showinfo("No Reports", "No accident reports available.")
        else:
            reports_window = tk.Toplevel(self)
            reports_window.title("Accident Reports")
            reports_window.geometry("300x300")

            for report in accident_reports:
                report_label = tk.Label(
                    reports_window,
                    text=f"ID: {report['report_id']}\nTimestamp: {report['timestamp']}\nLocation: {report['location']}\nSeverity: {report['severity']}\nDescription: {report['description']}\nReported by: {report['reported_by']}\n"
                )
                report_label.pack(pady=10)

    def show_on_map(self):
        if not accident_reports:
            messagebox.showinfo("No Reports", "No accident reports available.")
        else:
            maps_window = tk.Toplevel(self)
            maps_window.title("Accidents on Map")
            maps_window.geometry("600x400")

            maps_frame = MapsFrame(maps_window, accident_reports)
            maps_frame.pack(expand=True, fill=tk.BOTH)

    def logout(self):
        self.parent.current_user = None
        self.parent.show_frame("login")


class MapsFrame(tk.Frame):
    def __init__(self, parent, accident_reports):
        super().__init__(parent)
        self.parent = parent

        # Set up the Qt environment for embedding Google Maps
        self.qt_app = QtWidgets.QApplication.instance()
        if self.qt_app is None:
            self.qt_app = QtWidgets.QApplication(sys.argv)

        # Create the Google Maps URL with markers for each accident
        gmaps_url = self.create_maps_url(accident_reports)

        print("Google Maps URL:", gmaps_url)  # Debug output

        # Create the QWebEngineView widget
        self.web_engine_view = QtWebEngineWidgets.QWebEngineView()

        # Load the URL into the web view
        self.web_engine_view.load(QtCore.QUrl(gmaps_url))

        # Display the Qt widget within the Tkinter frame
        self.web_engine_view.setGeometry(0,0,self.winfo_width(), self.winfo_height())
        self.web_engine_view.setParent(self)  # Set the parent correctly
        self.update()

    def create_maps_url(self, accident_reports):
        # Google Maps base URL
        base_url = "https://www.google.com/maps/embed/v1/place?key="YOUR API KEY"

        # Construct the 'q' parameter with the locations of accidents
        locations = "|".join(report["location"].replace(" ", "+") for report in accident_reports)
        q_parameter = "&q=" + locations

        # Construct the complete URL
        complete_url = base_url + q_parameter

        return complete_url




if __name__ == "__main__":
    app = App()
    app.mainloop()
