import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import time
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def ejecutar_No_Rest():
    def f(x):
        return x**4 - 3*x**3 + 2

    def grad_f(x):
        return 4*x**3 - 9*x**2

    def hess_f(x):
        return 12*x**2 - 18*x

    def gradient_descent(f, grad_f, x0, lr=0.01, tol=1e-6, max_iter=1000):
        x = x0
        history = [x]
        start_time = time.time()
        for i in range(max_iter):
            grad = grad_f(x)
            x = x - lr * grad
            history.append(x)
            if abs(grad) < tol:
                break
        end_time = time.time()
        return x, f(x), i+1, end_time - start_time, history

    def newton_method(f, grad_f, hess_f, x0, tol=1e-6, max_iter=100):
        x = x0
        history = [x]
        start_time = time.time()
        for i in range(max_iter):
            grad = grad_f(x)
            hess = hess_f(x)
            if abs(hess) < 1e-6:
                break
            x = x - grad / hess
            history.append(x)
            if abs(grad) < tol:
                break
        end_time = time.time()
        return x, f(x), i+1, end_time - start_time, history

    def bfgs_method(f, grad_f, x0):
        history = []
        
        def callback(xk):
            history.append(xk[0])
        
        start_time = time.time()
        res = minimize(f, x0, method='BFGS', jac=grad_f, tol=1e-6, callback=callback)
        end_time = time.time()
        return res.x[0], res.fun, res.nit, end_time - start_time, history

    def plot_optimization_path(method_name, history):
        for widget in frame_grafica.winfo_children():
            widget.destroy()

        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.plot(x_vals, y_vals, label='Función f(x)', color='blue')
        ax.scatter(history, [f(x) for x in history], color='orange', marker='o', label='Iteraciones')
        ax.plot(history, [f(x) for x in history], color='orange', linestyle='-', alpha=0.7)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'Optimización - {method_name}')
        ax.legend()
        ax.grid()
        ax.set_ylim(-10, 10)  # Limitar eje Y entre -10 y 10

        canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def run_optimization():
        x0 = float(entry_x0.get())
        lr = float(entry_lr.get())
        method = method_var.get()
        
        if method == 'Gradiente Descendente':
            x_opt, f_opt, iters, exec_time, history = gradient_descent(f, grad_f, x0, lr)
        elif method == 'Newton-Raphson':
            x_opt, f_opt, iters, exec_time, history = newton_method(f, grad_f, hess_f, x0)
        elif method == 'BFGS':
            x_opt, f_opt, iters, exec_time, history = bfgs_method(f, grad_f, x0)
        else:
            return
        
        result_label.config(text=f"{method}: x = {x_opt:.6f}, f(x) = {f_opt:.6f}, iteraciones = {iters}, tiempo = {exec_time:.6f} s")
        plot_optimization_path(method, history)

    root = tk.Tk()
    root.title("Optimización sin Restricciones")
    root.geometry("700x700")
    root.config(bg="peach puff")

    frame_controles = tk.Frame(root, bg="peach puff")
    frame_controles.pack(pady=10)

    tk.Label(frame_controles, text="Punto inicial (x0):", bg="peach puff", font=("Roboto", 12)).grid(row=0, column=0, sticky="w", pady=5)
    entry_x0 = tk.Entry(frame_controles, width=15, bg="peach puff", font=("Roboto", 12))
    entry_x0.grid(row=0, column=1, pady=5)
    entry_x0.insert(0, "2.0")

    tk.Label(frame_controles, text="Tasa de aprendizaje:", bg="peach puff", font=("Roboto", 12)).grid(row=1, column=0, sticky="w", pady=5)
    entry_lr = tk.Entry(frame_controles, width=15, bg="peach puff", font=("Roboto", 12))
    entry_lr.grid(row=1, column=1, pady=5)
    entry_lr.insert(0, "0.01")

    tk.Label(frame_controles, text="Método de optimización:", bg="peach puff", font=("Roboto", 12)).grid(row=2, column=0, sticky="w", pady=5)
    method_var = ttk.Combobox(frame_controles, values=["Gradiente Descendente", "Newton-Raphson", "BFGS"], font=("Roboto", 12))
    method_var.grid(row=2, column=1, pady=5)
    method_var.set("Gradiente Descendente")

    btn_run = tk.Button(root, text="Ejecutar", command=run_optimization, font=("Roboto", 12), bg="#D2B48C", relief="raised", padx=10, pady=5)
    btn_run.pack(pady=10)

    result_label = tk.Label(root, text="Resultados aquí", wraplength=500, justify="center", bg="peach puff", font=("Roboto", 12))
    result_label.pack(pady=5)

    frame_grafica = tk.Frame(root, bg="peach puff", width=500, height=250)
    frame_grafica.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()
