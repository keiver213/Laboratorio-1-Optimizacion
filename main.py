import tkinter as tk
from tkinter import ttk, messagebox
from Taylor import ejecutar_taylor
from Caso_Opti import ejecutar_Caso_Opti
from Opti_sin_rest import ejecutar_No_Rest
from spar import ejecutar_sparce

def abrir_taylor():
    ejecutar_taylor()

def abrir_Caso_Opti():
    ejecutar_Caso_Opti()

def abrir_No_Rest():
    ejecutar_No_Rest()

def abrir_sparce():
    ejecutar_sparce()

def mensaje_boton(numero):
    messagebox.showinfo("Mensaje", f"Botón {numero} presionado. Puedes asignarle otra función.")

# Crear la ventana principal
root = tk.Tk()
root.title("Menú Principal")
root.geometry("500x500")
root.config(bg="peach puff")

# Estilo para los botones
style = ttk.Style()
style.configure("TButton", font=("Roboto", 12), padding=10)
style.map("TButton", background=[("active", "#D2B48C")])  # Cambia color al pasar el mouse

# Crear el título
tk.Label(root, text="Seleccione una opción:", font=("Roboto", 24, "bold"), bg="peach puff").pack(pady=20)

# Crear un marco para organizar los botones
frame = tk.Frame(root, bg="peach puff")
frame.pack()

# Botones
botones = [
    ("Caso Optimización", abrir_Caso_Opti),
    ("Matriz Sparce", abrir_sparce),
    ("Serie de Taylor", abrir_taylor),
    ("Optimización sin restricciones", abrir_No_Rest),
    ("Salir", root.destroy)
]

for i, (texto, comando) in enumerate(botones):
    btn = ttk.Button(frame, text=texto, command=comando, style="TButton", width=30)
    btn.grid(row=i, column=0, pady=10)

# Ejecutar el bucle principal
root.mainloop()
