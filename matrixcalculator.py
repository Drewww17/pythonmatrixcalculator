import tkinter as tk
from tkinter import messagebox
import numpy as np

class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Matrix Lab - Section A122")
        self.root.geometry("650x750")
        self.root.configure(bg="#f4f4f4")

        # Matrix Storage
        self.entries_a = []
        self.entries_b = []

        # --- Header Section (Members & Section) ---
        header_frame = tk.Frame(root, bg="#2c3e50", pady=10)
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="MATRIX OPERATIONS PROJECT", 
                 fg="white", bg="#2c3e50", font=("Arial", 14, "bold")).pack()
        
        info_text = "Section: A122\nMembers: Philip Luminarias, Seth Leyson, Psyrylle Javier"
        tk.Label(header_frame, text=info_text, 
                 fg="#ecf0f1", bg="#2c3e50", font=("Arial", 10)).pack()

        # --- Main UI Layout ---
        main_container = tk.Frame(root, padx=20, pady=10)
        main_container.pack()

        # Dimension Inputs
        dim_frame = tk.LabelFrame(main_container, text="Grid Settings", padx=10, pady=5)
        dim_frame.pack(pady=10)
        
        tk.Label(dim_frame, text="Rows:").grid(row=0, column=0)
        self.rows_entry = tk.Entry(dim_frame, width=5)
        self.rows_entry.insert(0, "3")
        self.rows_entry.grid(row=0, column=1, padx=5)

        tk.Label(dim_frame, text="Cols:").grid(row=0, column=2)
        self.cols_entry = tk.Entry(dim_frame, width=5)
        self.cols_entry.insert(0, "3")
        self.cols_entry.grid(row=0, column=3, padx=5)

        tk.Button(dim_frame, text="Rebuild Grids", bg="#3498db", fg="white", 
                  command=self.create_grids).grid(row=0, column=4, padx=10)

        # Matrix Entry Frames
        self.matrix_container = tk.Frame(main_container)
        self.matrix_container.pack(pady=15)

        # Operation Buttons
        btn_frame = tk.Frame(main_container)
        btn_frame.pack(pady=5)

        # Styling for buttons
        btn_style = {"width": 12, "pady": 5}
        
        tk.Button(btn_frame, text="Add (A+B)", **btn_style, command=lambda: self.operate("add")).grid(row=0, column=0, padx=2)
        tk.Button(btn_frame, text="Subtract (A-B)", **btn_style, command=lambda: self.operate("sub")).grid(row=0, column=1, padx=2)
        tk.Button(btn_frame, text="Multiply (A*B)", **btn_style, command=lambda: self.operate("mul")).grid(row=0, column=2, padx=2)
        
        tk.Button(btn_frame, text="Transpose A", **btn_style, command=self.transpose_a).grid(row=1, column=0, padx=2, pady=5)
        tk.Button(btn_frame, text="Randomize", **btn_style, bg="#27ae60", fg="white", command=self.fill_random).grid(row=1, column=1, padx=2, pady=5)
        tk.Button(btn_frame, text="Clear", **btn_style, bg="#e74c3c", fg="white", command=self.clear_all).grid(row=1, column=2, padx=2, pady=5)

        # Result Display
        tk.Label(main_container, text="Calculated Result:", font=("Arial", 11, "bold")).pack(pady=(10, 0))
        self.result_text = tk.Text(main_container, height=10, width=60, state='disabled', bg="#ffffff", font=("Courier", 10))
        self.result_text.pack(pady=10)

        self.create_grids()

    def create_grids(self):
        for widget in self.matrix_container.winfo_children():
            widget.destroy()

        try:
            r = int(self.rows_entry.get())
            c = int(self.cols_entry.get())
            if r > 10 or c > 10:
                messagebox.showwarning("Warning", "Keep dimensions 10x10 or smaller for display clarity.")
        except ValueError:
            messagebox.showerror("Error", "Enter valid integers.")
            return

        self.entries_a = self.build_grid(self.matrix_container, "Matrix A", 0, r, c)
        self.entries_b = self.build_grid(self.matrix_container, "Matrix B", 1, r, c)

    def build_grid(self, parent, title, col_offset, r, c):
        frame = tk.LabelFrame(parent, text=title, padx=5, pady=5)
        frame.grid(row=0, column=col_offset, padx=10)
        
        entries = []
        for i in range(r):
            row_entries = []
            for j in range(c):
                e = tk.Entry(frame, width=4)
                e.grid(row=i, column=j, padx=1, pady=1)
                row_entries.append(e)
            entries.append(row_entries)
        return entries

    def get_matrix_data(self, entries):
        try:
            return np.array([[float(e.get() or 0) for e in row] for row in entries])
        except ValueError:
            messagebox.showerror("Error", "Ensure all fields are numbers.")
            return None

    def display_result(self, matrix):
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(matrix))
        self.result_text.config(state='disabled')

    def operate(self, mode):
        a = self.get_matrix_data(self.entries_a)
        b = self.get_matrix_data(self.entries_b)
        
        if a is not None and b is not None:
            try:
                if mode == "add": res = a + b
                elif mode == "sub": res = a - b
                elif mode == "mul": res = np.matmul(a, b)
                self.display_result(res)
            except Exception as e:
                messagebox.showerror("Operation Error", str(e))

    def transpose_a(self):
        a = self.get_matrix_data(self.entries_a)
        if a is not None:
            self.display_result(a.T)

    def fill_random(self):
        for grid in [self.entries_a, self.entries_b]:
            for row in grid:
                for e in row:
                    e.delete(0, tk.END)
                    e.insert(0, str(np.random.randint(0, 10)))

    def clear_all(self):
        for grid in [self.entries_a, self.entries_b]:
            for row in grid:
                for e in row:
                    e.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixApp(root)
    root.mainloop()