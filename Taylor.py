import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def ejecutar_taylor():
    def Derivadas(F, N, x):
        Derivadas = []
        F = sp.sympify(F, locals={"sin": sp.sin, "cos": sp.cos, "exp": sp.exp, "log": sp.log, "tan": sp.tan})
        Derivadas.append(F)
        for i in range(1, N+1):
            Derivadas.append(sp.diff(Derivadas[i-1], x))
        return Derivadas

    def Taylor(F, N, X0):
        x = sp.Symbol('x')
        derivadas = Derivadas(F, N, x)
        taylor_series = sum((derivadas[i].subs(x, X0) * (x - X0)**i) / sp.factorial(i) for i in range(N + 1))
        return taylor_series.expand(), str(taylor_series.expand())

    def calcular_taylor():
        """ Obtiene los datos ingresados y muestra la serie de Taylor. """
        try:
            F = funcion_entry.get()
            X0 = float(expansion_entry.get())
            N = int(terminos_entry.get())
            
            taylor_series, taylor_str = Taylor(F, N, X0)
            resultado_label.config(text=f"Serie de Taylor:\n{taylor_str}")
            graficar(F, taylor_series, X0)
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error:\n{e}")

    def graficar(F, taylor_series, X0):
        """ Grafica la función original y su serie de Taylor dentro de Tkinter. """
        x = sp.Symbol('x')
        f_lambdified = sp.lambdify(x, sp.sympify(F), 'numpy')
        taylor_lambdified = sp.lambdify(x, taylor_series, 'numpy')
        
        X = np.linspace(X0 - 2, X0 + 2, 400)
        Y_f = f_lambdified(X)
        Y_taylor = taylor_lambdified(X)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(X, Y_f, label="Función original", color="blue")
        ax.plot(X, Y_taylor, label=f"Taylor ({X0})", linestyle="dashed", color="red")
        ax.axvline(X0, color="gray", linestyle="dotted")
        ax.legend()
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Aproximación con Serie de Taylor")
        ax.grid()

        # Limpiar canvas anterior si existe
        for widget in frame_grafica.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # Crear ventana
    root = tk.Tk()
    root.title("Serie de Taylor")
    root.config(bg="peach puff")
    root.geometry("700x700")

    frame_controles = tk.Frame(root, bg="peach puff")
    frame_controles.pack(pady=10)

    tk.Label(frame_controles, text="Función f(x):", bg="peach puff", font=("Roboto", 12)).grid(row=0, column=0, sticky="w", pady=5)
    funcion_entry = tk.Entry(frame_controles, width=30, bg="peach puff", font=("Roboto", 12))
    funcion_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame_controles, text="Punto de expansión x0:", bg="peach puff", font=("Roboto", 12)).grid(row=1, column=0, sticky="w", pady=5)
    expansion_entry = tk.Entry(frame_controles, width=20, bg="peach puff", font=("Roboto", 12))
    expansion_entry.grid(row=1, column=1, pady=5)

    tk.Label(frame_controles, text="Número de términos:", bg="peach puff", font=("Roboto", 12)).grid(row=2, column=0, sticky="w", pady=5)
    terminos_entry = tk.Entry(frame_controles, width=20, bg="peach puff", font=("Roboto", 12))
    terminos_entry.grid(row=2, column=1, pady=5)

    calcular_btn = tk.Button(frame_controles, text="Calcular Serie de Taylor", font=("Roboto", 12), command=calcular_taylor, bg="#D2B48C", relief="raised", padx=10, pady=5)
    calcular_btn.grid(row=3, column=0, columnspan=2, pady=15)

    resultado_label = tk.Label(root, text="Serie de Taylor aparecerá aquí", wraplength=600, justify="center", bg="peach puff", font=("Roboto", 12))
    resultado_label.pack(pady=10)

    frame_grafica = tk.Frame(root)
    frame_grafica.pack(pady=10)

    root.mainloop()
