import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import time

filename = None
file_content = None

def run_script(method):
    global filename, file_content
    if filename:
        # Convert the absolute file path to a relative file path
        filename = os.path.relpath(filename)
        # Replace forward slashes with backslashes
        filename = filename.replace("/", "\\")

        # Save the edited content to a temporary file
        with open("temp.txt", "w") as f:
            f.write(file_content)

        start_time = time.time()
        try:
            result = subprocess.check_output(f"python main.py {method} temp.txt", shell=True).decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            result = e.output.decode("utf-8").strip()
        end_time = time.time()
        elapsed_time = end_time - start_time

        #messagebox.showinfo("Result", f"Result: {result}\nTime taken: {elapsed_time:.2f} seconds")
        performance_text.insert(tk.END, f"Method: {method.upper()}\nResult: {result}\n Time taken: {elapsed_time:.2f} seconds\n\n")

def import_test_file():
    global filename, file_content
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, "r") as f:
            file_content = f.read()
        test_file_text.delete("1.0", tk.END)
        test_file_text.insert(tk.END, file_content)
        filename = os.path.relpath(filename)
        test_file_text.insert(tk.END, f"\n\nFilename: {filename}")

def clear_performance():
    performance_text.delete("1.0", tk.END)
    test_file_text.delete("1.0", tk.END)

def delete_algorithm():
    text = performance_text.get("1.0", tk.END).strip()
    lines = text.split("\n")
    if len(lines) >= 3:
        lines = lines[:-3]
        text = "\n".join(lines)
        performance_text.delete("1.0", tk.END)
        performance_text.insert(tk.END, text)

def save_edits():
    global file_content
    file_content = test_file_text.get("1.0", tk.END).strip()

root = tk.Tk()
root.title("Inference Engine GUI Tool")
root.geometry("800x600")

frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)

tt_button = tk.Button(frame1, text="Truth Table", command=lambda: run_script("tt"))
fc_button = tk.Button(frame1, text="Forward Chaining", command=lambda: run_script("fc"))
bc_button = tk.Button(frame1, text="Backward Chaining", command=lambda: run_script("bc"))
rt_button = tk.Button(frame1, text="Rete", command=lambda: run_script("rt"))
ws_button = tk.Button(frame1, text="WalkSAT", command=lambda: run_script("ws"))
rs_button = tk.Button(frame1, text="Resolution", command=lambda: run_script("rs"))

import_button = tk.Button(frame2, text="Import Test File", command=import_test_file)
clear_button = tk.Button(frame3, text="Clear All", command=clear_performance)
delete_button = tk.Button(frame3, text="Delete Algorithm", command=delete_algorithm)
save_button = tk.Button(frame3, text="Save Edits", command=save_edits)

test_file_text = tk.Text(frame2, height=5, width=3)
performance_text = tk.Text(frame2, height=5, width=3)

tt_button.pack(side=tk.LEFT)
fc_button.pack(side=tk.LEFT)
bc_button.pack(side=tk.LEFT)
rt_button.pack(side=tk.LEFT)
ws_button.pack(side=tk.LEFT)
rs_button.pack(side=tk.LEFT)

import_button.pack()
test_file_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
performance_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

clear_button.pack(side=tk.LEFT)
delete_button.pack(side=tk.LEFT)
save_button.pack(side=tk.LEFT)

frame1.pack(fill=tk.X)
frame2.pack(fill=tk.BOTH, expand=True)
frame3.pack(fill=tk.X)

root.mainloop()
