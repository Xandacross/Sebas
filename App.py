#!/usr/bin/env python3

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from plyer import notification
import re

class App:
    def __init__(self, master):
        self.master = master
        master.title("Automate Recon")

        # Create and grid the main widgets
        self.target_label = tk.Label(master, text="Target Domain:")
        self.target_label.grid(row=0, column=0, sticky="w")

        self.target_entry = tk.Entry(master, width=30)
        self.target_entry.grid(row=0, column=1)

        self.browse_button = tk.Button(master, text="Select Output Directory", command=self.browse)
        self.browse_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.run_button = tk.Button(master, text="Run Recon", command=self.run)
        self.run_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.output_dir = ""

    def browse(self):
        selected_dir = filedialog.askdirectory(initialdir=os.getcwd())
        if selected_dir:
            self.output_dir = selected_dir
            self.browse_button.configure(text=selected_dir)
        else:
            self.browse_button.configure(text="Select Output Directory")

    def run(self):
        target = self.target_entry.get().strip()

        # Validate the target input
        if not target:
            messagebox.showerror("Error", "Please enter a valid target domain or IP address")
            return

        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
            # Target is an IP address
            pass
        elif not re.match(r"^[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$", target):
            messagebox.showerror("Error", "Invalid target domain or IP address")
            return

        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return

        # Execute the Bash script and wait for it to complete
        recon_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recon.sh")
        process = subprocess.Popen([recon_script, target], cwd=self.output_dir)
        process.wait()

        # Show a desktop notification when the recon is complete
        notification.notify(
            title="Recon Complete",
            message=f"The recon for {target} is complete.",
            app_name="Automate Recon"
        )

root = tk.Tk()
app = App(root)
root.mainloop()