import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def optimize_tasks():
    try:
        total_tasks = int(entry_tasks.get())
    except ValueError:
        show_error("Por favor, ingrese un número válido de tareas.")
        return

    # Parámetros del problema
    tasks_per_hour_A = 20
    tasks_per_hour_B = 30
    max_hours_A = 10
    max_hours_B = 8
    storage_per_task_A = 10
    storage_per_task_B = 15
    total_storage = 500

    # Cálculo de las restricciones
    max_tasks_A = tasks_per_hour_A * max_hours_A
    max_tasks_B = tasks_per_hour_B * max_hours_B
    max_storage_A = total_storage // storage_per_task_A
    max_storage_B = total_storage // storage_per_task_B

    # Verificar si se excede el límite de memoria
    max_possible_tasks = min(max_storage_A + max_storage_B, max_tasks_A + max_tasks_B)
    if total_tasks > max_possible_tasks:
        show_error(f"El número de tareas excede el límite de memoria o tiempo. Máximo posible: {max_possible_tasks} tareas.")
        memory_error_label.config(text="EXCEDITE EL LIMITE DE MEMORIA", foreground="red")
        return
    else:
        memory_error_label.config(text="")  # Limpiar el mensaje si no hay error de memoria

    # Limpiar mensaje de error si no hay problemas
    error_label.config(text="")

    # Optimización
    tasks_A = min(max_tasks_A, max_storage_A)
    tasks_B = min(max_tasks_B, max_storage_B)
    
    # Ajuste si el total de tareas es menor que la suma de las capacidades máximas
    if total_tasks < tasks_A + tasks_B:
        ratio_A = tasks_per_hour_A / (tasks_per_hour_A + tasks_per_hour_B)
        tasks_A = min(int(total_tasks * ratio_A), tasks_A)
        tasks_B = min(total_tasks - tasks_A, tasks_B)

    # Cálculo del almacenamiento utilizado y restante
    storage_used = tasks_A * storage_per_task_A + tasks_B * storage_per_task_B
    storage_remaining = total_storage - storage_used

    # Actualizar los resultados en la interfaz
    result_label.config(text=f"Tareas en Servidor A: {tasks_A}\n"
                             f"Tareas en Servidor B: {tasks_B}\n"
                             f"Total de tareas completadas: {tasks_A + tasks_B}\n"
                             f"Almacenamiento utilizado: {storage_used} GB\n"
                             f"Almacenamiento restante: {storage_remaining} GB")

    # Crear gráfico
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gráfico de tareas
    servers = ['Servidor A', 'Servidor B']
    tasks = [tasks_A, tasks_B]
    ax1.bar(servers, tasks)
    ax1.set_ylabel('Número de tareas')
    ax1.set_title('Distribución de tareas por servidor')
    for i, v in enumerate(tasks):
        ax1.text(i, v, str(v), ha='center', va='bottom')

    # Gráfico de almacenamiento
    storage = [storage_used, storage_remaining]
    labels = 'Utilizado', 'Restante'
    ax2.pie(storage, labels=labels, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    ax2.set_title('Uso del almacenamiento')

    # Ajustar el espaciado entre subplots
    plt.tight_layout()

    # Mostrar gráfico en la interfaz
    for widget in window.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

def show_error(message):
    error_label.config(text=message, foreground="red")
    result_label.config(text="")
    memory_error_label.config(text="")  # Limpiar el mensaje de error de memoria
    # Limpiar gráficos si existen
    for widget in window.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()

# Crear la ventana principal
window = tk.Tk()
window.title("Optimización de tareas")

# Crear y posicionar los widgets
label_tasks = ttk.Label(window, text="Número total de tareas:")
label_tasks.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_tasks = ttk.Entry(window)
entry_tasks.grid(row=0, column=1, padx=5, pady=5)

optimize_button = ttk.Button(window, text="Optimizar", command=optimize_tasks)
optimize_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

error_label = ttk.Label(window, text="", foreground="red")
error_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

result_label = ttk.Label(window, text="")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Etiqueta para el error de memoria
memory_error_label = ttk.Label(window, text="", foreground="red")
memory_error_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Iniciar el bucle principal
window.mainloop()
