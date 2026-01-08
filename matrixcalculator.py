import tkinter as tk
from tkinter import messagebox
import numpy as np

class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Matrix Lab - Section A122")
        self.root.geometry("650x780")
        self.root.configure(bg="#f8f9fa")

        # Matrix Storage
        self.entries_a = []
        self.entries_b = []

        # --- Header Section (Philip, Seth, Psyrylle) ---
        header = tk.Frame(root, bg="#2c3e50", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="MATRIX OPERATIONS PROJECT", fg="white", bg="#2c3e50", font=("Arial", 16, "bold")).pack()
        tk.Label(header, text="Section: A122 | Members: Philip Luminarias, Seth Leyson, Psyrylle Javier", 
                 fg="#bdc3c7", bg="#2c3e50", font=("Arial", 10)).pack()

        main_frame = tk.Frame(root, padx=20, pady=10)
        main_frame.pack()

        # --- Grid Settings ---
        dim_frame = tk.LabelFrame(main_frame, text="Grid Settings", padx=10, pady=10)
        dim_frame.pack(pady=10)
        
        tk.Label(dim_frame, text="Rows:").grid(row=0, column=0)
        self.rows_entry = tk.Entry(dim_frame, width=5)
        self.rows_entry.insert(0, "3")
        self.rows_entry.grid(row=0, column=1, padx=5)

        tk.Label(dim_frame, text="Cols:").grid(row=0, column=2)
        self.cols_entry = tk.Entry(dim_frame, width=5)
        self.cols_entry.insert(0, "3")
        self.cols_entry.grid(row=0, column=3, padx=5)

        tk.Button(dim_frame, text="Rebuild Grids", bg="#3498db", fg="white", relief="flat",
                  command=self.create_grids).grid(row=0, column=4, padx=10)

        # Matrix Entry Frames
        self.matrix_container = tk.Frame(main_frame)
        self.matrix_container.pack(pady=15)

        # --- Operation Buttons ---
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=5)
        
        btn_config = {"width": 14, "pady": 5, "font": ("Arial", 9, "bold")}
        
        tk.Button(btn_frame, text="Add (A+B)", **btn_config, command=lambda: self.operate("add")).grid(row=0, column=0, padx=3)
        tk.Button(btn_frame, text="Subtract (A-B)", **btn_config, command=lambda: self.operate("sub")).grid(row=0, column=1, padx=3)
        tk.Button(btn_frame, text="Multiply (A*B)", **btn_config, command=lambda: self.operate("mul")).grid(row=0, column=2, padx=3)
        
        tk.Button(btn_frame, text="Transpose A", **btn_config, command=self.transpose_a).grid(row=1, column=0, padx=3, pady=10)
        tk.Button(btn_frame, text="Randomize", **btn_config, bg="#27ae60", fg="white", command=self.fill_random).grid(row=1, column=1, padx=3)
        tk.Button(btn_frame, text="Clear All", **btn_config, bg="#e74c3c", fg="white", command=self.clear_all).grid(row=1, column=2, padx=3)

        # --- Result Display ---
        tk.Label(main_frame, text="Calculated Result:", font=("Arial", 11, "bold")).pack(pady=(10, 0))
        self.result_text = tk.Text(main_frame, height=10, width=65, state='disabled', bg="white", font=("Courier New", 11))
        self.result_text.pack(pady=10)

        self.create_grids()

    def create_grids(self):
        for widget in self.matrix_container.winfo_children():
            widget.destroy()
        try:
            r, c = int(self.rows_entry.get()), int(self.cols_entry.get())
            self.entries_a = self.build_grid(self.matrix_container, "Matrix A", 0, r, c)
            self.entries_b = self.build_grid(self.matrix_container, "Matrix B", 1, r, c)
        except:
            messagebox.showerror("Error", "Invalid Row/Col dimensions.")

    def build_grid(self, parent, title, col_offset, r, c):
        frame = tk.LabelFrame(parent, text=title, padx=10, pady=10)
        frame.grid(row=0, column=col_offset, padx=15)
        entries = [[tk.Entry(frame, width=6) for _ in range(c)] for _ in range(r)]
        for i, row in enumerate(entries):
            for j, entry in enumerate(row):
                entry.grid(row=i, column=j, padx=2, pady=2)
        return entries

    def get_data(self, entries):
        try:
            # Filters out empty boxes so we only count boxes with actual numbers
            data = []
            for row in entries:
                row_vals = [float(e.get()) for e in row if e.get().strip() != ""]
                if row_vals: data.append(row_vals)
            return np.array(data)
        except ValueError:
            messagebox.showerror("Input Error", "All active cells must contain numbers.")
            return None

    def display(self, message):
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state='disabled')

    def operate(self, mode):
        a = self.get_data(self.entries_a)
        b = self.get_data(self.entries_b)
        
        if a is None or b is None: return

        try:
            if mode in ["add", "sub"]:
                if a.shape != b.shape:
                    msg = f"OPERATION NOT POSSIBLE\nReason: Dimensions mismatch.\nMatrix A is {a.shape}, Matrix B is {b.shape}."
                    messagebox.showwarning("Error", msg)
                    self.display(msg)
                    return
                res = a + b if mode == "add" else a - b
            
            elif mode == "mul":
                if a.shape[1] != b.shape[0]:
                    msg = f"OPERATION NOT POSSIBLE\nReason: Inner dimensions must match.\nCols of A ({a.shape[1]}) must equal Rows of B ({b.shape[0]})."
                    messagebox.showwarning("Error", msg)
                    self.display(msg)
                    return
                res = np.dot(a, b)

            self.display(str(res))
        except Exception as e:
            self.display(f"Error: {str(e)}")

    def transpose_a(self):
        a = self.get_data(self.entries_a)
        if a is not None: self.display(str(a.T))

    def fill_random(self):
        for grid in [self.entries_a, self.entries_b]:
            for row in grid:
                for e in row:
                    e.delete(0, tk.END); e.insert(0, str(np.random.randint(-5, 10)))

    def clear_all(self):
        for grid in [self.entries_a, self.entries_b]:
            for row in grid:
                for e in row: e.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixApp(root)
    root.mainloop()