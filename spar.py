import tkinter as tk
from tkinter import ttk, messagebox
import random
import numpy as np
import scipy.sparse as sp
import time

def ejecutar_sparce():
    class matrizCSR:
        def __init__(self, data, columns, saltoDeFila, n, m):
            self.data = data
            self.columns = columns
            self.saltoDeFila = saltoDeFila
            self.cantFilas = n
            self.cantColumns = m
        
        def producto_por_vector(self, vector):
            resultado = [0] * self.cantFilas
            for i in range(self.cantFilas):
                inicio = self.saltoDeFila[i]
                fin = self.saltoDeFila[i + 1]
                for j in range(inicio, fin):  
                    resultado[i] += self.data[j] * vector[self.columns[j]]
            return resultado

    def generar_matriz(n, m, densidad):
        matriz = [[0] * m for _ in range(n)]
        cantidad = int(n * m * densidad)
        for _ in range(cantidad):
            while True:
                row, col = random.randint(0, n-1), random.randint(0, m-1)
                if matriz[row][col] == 0:
                    matriz[row][col] = random.randint(-1000, 1000)
                    break
        return matriz

    def generar_vector(m):
        return [random.randint(-100, 100) for _ in range(m)]

    def convertir_a_CSR(matriz, n, m):
        data, columns, inicioDeFila = [], [], [0] * (n + 1)
        index = 0
        for i in range(n):
            inicioDeFila[i] = index
            for j in range(m):
                if matriz[i][j] != 0:
                    data.append(matriz[i][j])
                    columns.append(j)
                    index += 1
        inicioDeFila[n] = index
        return matrizCSR(data, columns, inicioDeFila, n, m)

    def comparar_formatos(opcion, n, m, densidad):
        A = generar_matriz(n, m, densidad)
        B = generar_matriz(n, m, densidad)
        
        # Operaciones con matrices densas
        A_np = np.array(A)
        B_np = np.array(B)
        
        # Suma y multiplicación de matrices densas
        inicio_denso_suma = time.perf_counter()
        suma_densa = A_np + B_np
        fin_denso_suma = time.perf_counter()
        
        inicio_denso_mult = time.perf_counter()
        mult_densa = np.dot(A_np, B_np.T)
        fin_denso_mult = time.perf_counter()
        
        if opcion == 1:  # CSR
            A_sparse = sp.csr_matrix(A)
            B_sparse = sp.csr_matrix(B)
            
            inicio_csr_suma = time.perf_counter()
            suma_csr = A_sparse + B_sparse
            fin_csr_suma = time.perf_counter()
            
            inicio_csr_mult = time.perf_counter()
            mult_csr = A_sparse @ B_sparse.T
            fin_csr_mult = time.perf_counter()
            
            return {
                "Densa Suma": fin_denso_suma - inicio_denso_suma,
                "CSR Suma": fin_csr_suma - inicio_csr_suma,
                "Densa Multiplicación": fin_denso_mult - inicio_denso_mult,
                "CSR Multiplicación": fin_csr_mult - inicio_csr_mult
            }
        
        elif opcion == 2:  # COO
            A_sparse = sp.coo_matrix(A)
            B_sparse = sp.coo_matrix(B)
            
            inicio_coo_suma = time.perf_counter()
            suma_coo = A_sparse + B_sparse
            fin_coo_suma = time.perf_counter()
            
            inicio_coo_mult = time.perf_counter()
            mult_coo = A_sparse @ B_sparse.T
            fin_coo_mult = time.perf_counter()
            
            return {
                "Densa Suma": fin_denso_suma - inicio_denso_suma,
                "COO Suma": fin_coo_suma - inicio_coo_suma,
                "Densa Multiplicación": fin_denso_mult - inicio_denso_mult,
                "COO Multiplicación": fin_coo_mult - inicio_coo_mult
            }
        
        elif opcion == 3:  # LIL
            A_sparse = sp.lil_matrix(A)
            B_sparse = sp.lil_matrix(B)
            
            inicio_lil_suma = time.perf_counter()
            suma_lil = A_sparse + B_sparse
            fin_lil_suma = time.perf_counter()
            
            inicio_lil_mult = time.perf_counter()
            mult_lil = A_sparse @ B_sparse.T
            fin_lil_mult = time.perf_counter()
            
            return {
                "Densa Suma": fin_denso_suma - inicio_denso_suma,
                "LIL Suma": fin_lil_suma - inicio_lil_suma,
                "Densa Multiplicación": fin_denso_mult - inicio_denso_mult,
                "LIL Multiplicación": fin_lil_mult - inicio_lil_mult
            }
        
        else:
            return "Opción inválida. Elija 1 para CSR, 2 para COO o 3 para LIL."

    def ejecutar():
        try:
            n, m = int(filas_entry.get()), int(columnas_entry.get())
            d = float(densidad_entry.get())
            opcion = int(metodo_entry.get())
            if not (0.01 <= d <= 0.5):
                raise ValueError("Densidad fuera de rango")
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos")
            return
        
        matriz = generar_matriz(n, m, d)
        csr = convertir_a_CSR(matriz, n, m)
        vector = generar_vector(m)
        
        inicio = time.perf_counter()
        resultado_csr = csr.producto_por_vector(vector)
        tiempo_csr = time.perf_counter() - inicio
        
        inicio = time.perf_counter()
        resultado_densa = [sum(matriz[i][j] * vector[j] for j in range(m)) for i in range(n)]
        tiempo_densa = time.perf_counter() - inicio
        
        matriz_csr_python = sp.csr_matrix(matriz)
        inicio = time.perf_counter()
        resultado_python = matriz_csr_python.dot(vector)
        tiempo_python = time.perf_counter() - inicio
        
        # Compara y muestra los tiempos de ejecución
        resultados_comparacion = comparar_formatos(opcion, n, m, d)
        
        resultado_texto = f"Matriz Generada:\n" + "\n".join([" ".join(map(str, fila)) for fila in matriz]) 
        resultado_texto += f"\n\nResultado de multiplicación CSR:\n{resultado_csr}"
        resultado_texto += f"\n\nTiempo de multiplicación CSR:\n{tiempo_csr:.9f}s"
        resultado_texto += f"\n\nTiempo de multiplicación normal:\n{tiempo_densa:.9f}s"
        resultado_texto += f"\n\nTiempo de multiplicación de CSR con Python:\n{tiempo_python:.9f}s"
        
        # Agregamos un salto de línea antes de las comparaciones
        resultado_texto += "\n\n"  # Espaciado
        
        # Mostrar los resultados comparados
        if isinstance(resultados_comparacion, dict):
            for key, value in resultados_comparacion.items():
                resultado_texto += f"\n{key}: {value:.9f}s"
        
        resultado_label.config(text=resultado_texto)

    root = tk.Tk()
    root.title("Multiplicación CSR")

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky="nsew")

    # Ajuste de las posiciones en la interfaz
    ttk.Label(frame, text="Filas:").grid(row=0, column=0, sticky="w", padx=5)
    filas_entry = ttk.Entry(frame, width=10)
    filas_entry.grid(row=0, column=1, padx=5)

    ttk.Label(frame, text="Columnas:").grid(row=1, column=0, sticky="w", padx=5)
    columnas_entry = ttk.Entry(frame, width=10)
    columnas_entry.grid(row=1, column=1, padx=5)

    ttk.Label(frame, text="Densidad (0.01 - 0.5):").grid(row=2, column=0, sticky="w", padx=5)
    densidad_entry = ttk.Entry(frame, width=10)
    densidad_entry.grid(row=2, column=1, padx=5)

    ttk.Label(frame, text="Método (1=CSR, 2=COO, 3=LIL):").grid(row=3, column=0, sticky="w", padx=5)
    metodo_entry = ttk.Entry(frame, width=10)
    metodo_entry.grid(row=3, column=1, padx=5)

    # Botón ajustado a una fila más abajo
    ejecutar_btn = ttk.Button(frame, text="Ejecutar", command=ejecutar)
    ejecutar_btn.grid(row=4, column=0, columnspan=2, pady=10)

    # Etiqueta de resultados
    resultado_label = ttk.Label(frame, text="", justify="left")
    resultado_label.grid(row=5, column=0, columnspan=2, pady=5)

    root.mainloop()