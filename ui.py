import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from logic import calculate_radec, save_to_csv
from datetime import datetime

class CelestialApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Celestial Observer")
        self.root.geometry("800x500")
        self.root.configure(bg="#2b1d0e")

        # Tree Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#3b2a1a",
            foreground="#ffe08a",
            fieldbackground="#3b2a1a",
            bordercolor="#ffd166",
            lightcolor="#2b1d0e",
            darkcolor="#2b1d0e"
        )
        style.configure(
            "Treeview.Heading",
            background="#5c3d2e",
            foreground="#ffd166",
            bordercolor="#ffd166"
        )
        style.map("Treeview",
            background=[("selected", "#ffd166")],
            foreground=[("selected", "#2b1d0e")]
        )

        # configure grid weights
        for c in range(6):
            self.root.grid_columnconfigure(c, weight=1)
        for r in range(6):
            self.root.grid_rowconfigure(r, weight=0)

        label_opts = {"bg": "#2b1d0e", "fg": "#ffd166", "anchor": "e"}
        entry_opts = {"bg": "#3b2a1a", "fg": "#ffe08a", "insertbackground": "#ffe08a", "highlightbackground": "#ffd166", "highlightcolor": "#ffd166", "highlightthickness": 1, "width": 15}

        # --- Row 0: Date + Time ---
        tk.Label(self.root, text="Date (YYYY-MM-DD):", **label_opts).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = tk.Entry(self.root, **entry_opts)
        self.date_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self.root, text="Time (HH:MM:SS):", **label_opts).grid(row=0, column=4, sticky="e", padx=5, pady=5)
        self.time_entry = tk.Entry(self.root, **entry_opts)
        self.time_entry.grid(row=0, column=5, sticky="w", padx=5, pady=5)

        # --- Row 1: Lat + Long ---
        tk.Label(self.root, text="Latitude (deg):", **label_opts).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.latitude_entry = tk.Entry(self.root, **entry_opts)
        self.latitude_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self.root, text="Longitude (deg):", **label_opts).grid(row=1, column=4, sticky="e", padx=5, pady=5)
        self.longitude_entry = tk.Entry(self.root, **entry_opts)
        self.longitude_entry.grid(row=1, column=5, sticky="w", padx=5, pady=5)

        # --- Row 2: Elevation + Altitude + Azimuth ---
        tk.Label(self.root, text="Elevation (m):", **label_opts).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.elevation_entry = tk.Entry(self.root, **entry_opts)
        self.elevation_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self.root, text="Altitude (deg):", **label_opts).grid(row=2, column=2, sticky="e", padx=5, pady=5)
        self.altitude_entry = tk.Entry(self.root, **entry_opts)
        self.altitude_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)

        tk.Label(self.root, text="Azimuth (deg):", **label_opts).grid(row=2, column=4, sticky="e", padx=5, pady=5)
        self.azimuth_entry = tk.Entry(self.root, **entry_opts)
        self.azimuth_entry.grid(row=2, column=5, sticky="w", padx=5, pady=5)

        # --- Button ---
        self.save_button = tk.Button(self.root, text="Calculate and Save", command=self.calculate, bg="#5c3d2e", fg="#ffe08a", activebackground="#ffd166", activeforeground="#2b1d0e")
        self.save_button.grid(row=3, column=2, columnspan=2, pady=10, sticky="")

        # --- CSV Display ---
        self.output_box = tk.Text(self.root, height=10, bg="#3b2a1a", fg="#ffe08a", insertbackground="#ffe08a")
        self.output_box.grid(row=4, column=0, columnspan=6, sticky="nsew", padx=15, pady=10)
        self.root.grid_rowconfigure(4, weight=1)


    def calculate(self):
        try:
            date_str = self.date_entry.get()
            time_str = self.time_entry.get()
            latitude = float(self.latitude_entry.get())
            longitude = float(self.longitude_entry.get())
            elevation = float(self.elevation_entry.get())
            altitude = float(self.altitude_entry.get())
            azimuth = float(self.azimuth_entry.get())

            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

            ra, dec = calculate_radec(dt, latitude, longitude, elevation, altitude, azimuth)

            data = [date_str, time_str, latitude, longitude, elevation, altitude, azimuth, ra, dec]

            save_to_csv(data, 'log.csv')
            messagebox.showinfo("Success", f"RA= {ra:.2f}, DEC= {dec:.2f}")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please check your input values.")

    def run(self):
        self.root.mainloop()