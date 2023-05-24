import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import time

def run_script(method):
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        # Convert the absolute file path to a relative file path
        filename = os.path.relpath(filename)
        # Replace forward slashes with backslashes
        filename = filename.replace("/", "\\")
        start_time = time.time()
        result = subprocess.check_output(f"python main.py {method} {filename}", shell=True).decode("utf-8").strip()
        end_time = time.time()
        elapsed_time = end_time - start_time
        #messagebox.showinfo("Result", f"Result: {result}\nTime taken: {elapsed_time:.2f} seconds")
        #performance_text.insert(tk.END, f"Method: {method.upper()}\nFilename: {filename}\nTime taken: {elapsed_time:.2f} seconds\n\n")
        performance_text.insert(tk.END, f"Method: {method.upper()}\nResult: {result}\n\n")
        #counter += 1

def import_test_file():
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, "r") as f:
            content = f.read()
            test_file_text.delete("1.0", tk.END)
            test_file_text.insert(tk.END, content)
    test_file_text.insert(tk.END, f"\n\nFilename: {filename}")
            

def clear_performance():
    performance_text.delete("1.0", tk.END)
    test_file_text.delete("1.0", tk.END)
    #counter = 0

root = tk.Tk()
root.title("Inference Engine GUI Tool")

frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)

tt_button = tk.Button(frame1, text="Truth Table", command=lambda: run_script("tt"))
fc_button = tk.Button(frame1, text="Forward Chaining", command=lambda: run_script("fc"))
bc_button = tk.Button(frame1, text="Backward Chaining", command=lambda: run_script("bc"))
rt_button = tk.Button(frame1, text="Rete", command=lambda: run_script("rt"))
ws_button = tk.Button(frame1, text="WalkSAT", command=lambda: run_script("ws"))
import_button = tk.Button(frame2, text="Test File Visualiser", command=import_test_file)
clear_button = tk.Button(frame3, text="Clear All", command=clear_performance)

test_file_text = tk.Text(frame2, height=5)
performance_text = tk.Text(frame2, height=5)

tt_button.pack(side=tk.LEFT)
fc_button.pack(side=tk.LEFT)
bc_button.pack(side=tk.LEFT)
rt_button.pack(side=tk.LEFT)
ws_button.pack(side=tk.LEFT)

import_button.pack()
test_file_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

performance_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
clear_button.pack()

frame1.pack(fill=tk.X)
frame2.pack(fill=tk.BOTH, expand=True)
frame3.pack(fill=tk.X)

root.mainloop()
