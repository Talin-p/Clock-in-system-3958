import tkinter as tk
from tkinter import ttk, colorchooser
import requests
import csv
from io import StringIO
from datetime import datetime
from threading import Timer

GOOGLE_SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTo0Oy7yuI3NFADTcVTMnqYlXPf584j6tJmGeRCDRRD4Df3_-iRvRXu-qS9sFoGx-j7QHIAOCNl1Q-H/pub?gid=0&single=true&output=csv'

entries = {}
paused_people = set()
global_paused = False
bar_colors = {}

MAX_BAR_WIDTH = 350

root = tk.Tk()
root.title("Live Bar Graph")
root.geometry("800x600")
root.configure(bg="#fafafa")

# Top frame with buttons and clock
top_frame = tk.Frame(root, bg="#e2e8f0")
top_frame.pack(fill='x', padx=10, pady=5)

def format_time(seconds):
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}h {m}m {s}s" if h>0 else (f"{m}m {s}s" if m>0 else f"{s}s")

clock_label = tk.Label(top_frame, text="", font=("Segoe UI", 14), bg="#e2e8f0")
clock_label.pack(side='right', padx=10)

def update_clock():
    clock_label.config(text=datetime.now().strftime("%H:%M:%S"))
    root.after(1000, update_clock)

update_clock()

container = tk.Frame(root, bg="#ffffff")
container.pack(fill='both', expand=True, padx=20, pady=20)

rows = {}

# Functions
def fetch_data():
    global entries
    try:
        response = requests.get(GOOGLE_SHEET_CSV_URL)
        response.raise_for_status()
        f = StringIO(response.text)
        reader = csv.DictReader(f)
        new_entries = {}
        for row in reader:
            name = row.get("Name", "").strip()
            time_sec = int(row.get("TimeSeconds", 0))
            new_entries[name] = time_sec
            if name not in bar_colors:
                bar_colors[name] = "#87ceeb"
        entries = new_entries
        init_rows()
    except Exception as e:
        print("Error fetching sheet:", e)

def init_rows():
    for widget in container.winfo_children():
        widget.destroy()
    rows.clear()
    for name, time_sec in entries.items():
        row_frame = tk.Frame(container, bg="#ffffff")
        row_frame.pack(fill='x', pady=5)
        tk.Label(row_frame, text=name, width=15, anchor='w', font=("Segoe UI", 12)).pack(side='left')
        bar_frame = tk.Frame(row_frame, bg="#ffffff")
        bar_frame.pack(side='left', fill='x', expand=True)
        bar = tk.Frame(bar_frame, bg=bar_colors.get(name, "#87ceeb"), height=25, width=1)
        bar.pack(side='left', fill='y')
        time_label = tk.Label(bar_frame, text=format_time(time_sec), font=("Segoe UI", 10), bg="#ffffff")
        time_label.pack(side='left', padx=5)
        # Pause/Resume buttons
        btn_frame = tk.Frame(row_frame, bg="#ffffff")
        btn_frame.pack(side='right', padx=5)
        pause_btn = tk.Button(btn_frame, text="Pause", command=lambda n=name: paused_people.add(n))
        pause_btn.pack(side='left')
        resume_btn = tk.Button(btn_frame, text="Resume", command=lambda n=name: paused_people.discard(n))
        resume_btn.pack(side='left')
        rows[name] = {"bar": bar, "time_label": time_label}

def update_bars():
    if not global_paused:
        for name in entries:
            if name not in paused_people:
                entries[name] += 1
    max_time = max(entries.values() or [1])
    for name, data in rows.items():
        width = max(10, int((entries[name]/max_time)*MAX_BAR_WIDTH))
        data["bar"].config(width=width, bg=bar_colors.get(name, "#87ceeb"))
        data["time_label"].config(text=format_time(entries[name]))
    root.after(1000, update_bars)

# Buttons
btn_frame = tk.Frame(top_frame, bg="#e2e8f0")
btn_frame.pack(side='left', padx=10)

def pause_all():
    global global_paused
    global_paused = True

def resume_all():
    global global_paused
    global_paused = False

def change_bar_color():
    color = colorchooser.askcolor()[1]
    if color:
        for name in bar_colors:
            bar_colors[name] = color

tk.Button(btn_frame, text="Pause All", command=pause_all).pack(side='left', padx=5)
tk.Button(btn_frame, text="Resume All", command=resume_all).pack(side='left', padx=5)
tk.Button(btn_frame, text="Change Bar Color", command=change_bar_color).pack(side='left', padx=5)
tk.Button(btn_frame, text="Fetch Sheet", command=fetch_data).pack(side='left', padx=5)

fetch_data()
update_bars()
root.mainloop()
