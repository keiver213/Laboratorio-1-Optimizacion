import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def ejecutar_Caso_Opti():
    def calcular_costo():
        try:
            x = float(entry_x.get())
            y = float(entry_y.get())
            costo = (5 * x) + (3 * y)
            label_resultado.config(text=f"El costo en ({x}, {y}) es: {costo}")
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")

    def graficar_factible():
        for widget in frame_grafica.winfo_children():
            widget.destroy()

        x_vals = np.linspace(0, 10, 100)
        y1 = (8 - 1 * x_vals) / 2
        y2 = (10 - 2 * x_vals) / 1

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        ax.plot(x_vals, y1, label='1x + 2y ≤ 8', color='blue')
        ax.plot(x_vals, y2, label='2x + 1y ≤ 10', color='green')

        ax.fill_between(x_vals, np.maximum(0, np.minimum(y1, y2)), 10, color='red', alpha=0.3)
        ax.legend()
        ax.grid()
        ax.set_title("Región Factible")

        canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Crear ventana principal
    root = tk.Tk()
    root.geometry("800x800")  # Ajuste inicial, pero la ventana se adapta automáticamente
    root.config(bg="peachPuff2")
    root.title("Optimización de Costos")

    # Enunciado del problema (se ajusta automáticamente al tamaño de la pantalla)
    frame_enunciado = tk.Frame(root, bg="peachPuff2")
    frame_enunciado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    enunciado = """Supongamos que una empresa fabrica dos productos, X y Y, y quiere minimizar los costos de producción. 
La función de costo está dada por:
    C(x, y) = 5x + 3y
con las siguientes restricciones:
    x + 2y ≤ 8
    2x + y ≤ 10
    x ≥ 0, y ≥ 0
    """

    label_enunciado = tk.Label(frame_enunciado, text=enunciado, font=("Roboto", 14, "bold"), bg="peachPuff2", justify="left", wraplength=750)
    label_enunciado.pack(pady=5)

    # Formulario de entrada
    frame_inputs = tk.Frame(root, bg="peachPuff2")
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="Valor de X:", font=("Roboto", 14), bg="peachPuff2").grid(row=0, column=0, padx=5, pady=5)
    entry_x = tk.Entry(frame_inputs, width=10, font=("Roboto", 14), bg="white")
    entry_x.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_inputs, text="Valor de Y:", font=("Roboto", 14), bg="peachPuff2").grid(row=1, column=0, padx=5, pady=5)
    entry_y = tk.Entry(frame_inputs, width=10, font=("Roboto", 14), bg="white")
    entry_y.grid(row=1, column=1, padx=5, pady=5)

    # Botones y resultado
    frame_buttons = tk.Frame(root, bg="peachPuff2")
    frame_buttons.pack(pady=5)

    tk.Button(frame_buttons, text="Calcular Costo", command=calcular_costo, font=("Roboto", 12), bg="#D2B48C").grid(row=0, column=0, padx=10, pady=5)
    
    label_resultado = tk.Label(frame_buttons, text="", bg="peachPuff2", font=("Roboto", 14))
    label_resultado.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(frame_buttons, text="Mostrar Región Factible", command=graficar_factible, font=("Roboto", 12), bg="#D2B48C").grid(row=1, column=0, columnspan=2, pady=10)

    # Frame para la gráfica
    frame_grafica = tk.Frame(root, bg="peachPuff2", width=500, height=250)
    frame_grafica.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()
