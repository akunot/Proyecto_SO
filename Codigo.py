import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

procesos = []

# Algoritmos

def fcfs(procesos):
    procesos_ordenados = sorted(procesos, key=lambda x: x[1])
    tiempo_actual = 0
    resultados = []

    for nombre, llegada, servicio in procesos_ordenados:
        inicio = max(tiempo_actual, llegada)
        fin = inicio + servicio
        retorno = fin - llegada
        espera = retorno - servicio
        retorno_normalizado = round(retorno / servicio, 2)

        resultados.append((nombre, llegada, servicio, inicio, fin, retorno, espera, retorno_normalizado))
        tiempo_actual = fin

    return resultados

def sjf(procesos):
    procesos_ordenados = sorted(procesos, key=lambda x: x[1])
    tiempo_actual = 0
    resultados = []
    lista_procesos = procesos_ordenados.copy()
    terminados = []

    while lista_procesos:
        disponibles = [p for p in lista_procesos if p[1] <= tiempo_actual]
        if not disponibles:
            tiempo_actual = lista_procesos[0][1]
            disponibles = [p for p in lista_procesos if p[1] <= tiempo_actual]

        siguiente = min(disponibles, key=lambda x: x[2])
        lista_procesos.remove(siguiente)

        nombre, llegada, servicio = siguiente
        inicio = max(tiempo_actual, llegada)
        fin = inicio + servicio
        retorno = fin - llegada
        espera = retorno - servicio
        retorno_normalizado = round(retorno / servicio, 2)

        resultados.append((nombre, llegada, servicio, inicio, fin, retorno, espera, retorno_normalizado))
        tiempo_actual = fin

    return resultados

def round_robin(procesos, quantum):
    procesos_ordenados = sorted(procesos, key=lambda x: x[1])
    queue = []
    tiempo_actual = 0
    resultados = {}
    tiempos_restantes = {p[0]: p[2] for p in procesos}
    llegada_dict = {p[0]: p[1] for p in procesos}
    servicio_dict = {p[0]: p[2] for p in procesos}
    historial = []

    i = 0
    while procesos_ordenados or queue:
        while i < len(procesos_ordenados) and procesos_ordenados[i][1] <= tiempo_actual:
            queue.append(procesos_ordenados[i][0])
            i += 1

        if queue:
            proceso = queue.pop(0)
            duracion = min(quantum, tiempos_restantes[proceso])
            inicio = tiempo_actual
            tiempo_actual += duracion
            tiempos_restantes[proceso] -= duracion
            historial.append((proceso, inicio, tiempo_actual))

            while i < len(procesos_ordenados) and procesos_ordenados[i][1] <= tiempo_actual:
                queue.append(procesos_ordenados[i][0])
                i += 1

            if tiempos_restantes[proceso] > 0:
                queue.append(proceso)
            else:
                fin = tiempo_actual
                llegada = llegada_dict[proceso]
                servicio = servicio_dict[proceso]
                retorno = fin - llegada
                espera = retorno - servicio
                retorno_normalizado = round(retorno / servicio, 2)
                resultados[proceso] = (proceso, llegada, servicio, None, fin, retorno, espera, retorno_normalizado)
        else:
            if i < len(procesos_ordenados):
                tiempo_actual = procesos_ordenados[i][1]
            else:
                break


    for proceso in resultados:
        for h in historial:
            if h[0] == proceso:
                resultados[proceso] = (*resultados[proceso][:3], h[1], *resultados[proceso][4:])
                break

    return list(resultados.values()), historial

# GUI

def agregar_proceso():
    try:
        nombre = entry_nombre.get().strip()
        llegada = int(entry_llegada.get())
        servicio = int(entry_servicio.get())

        if not nombre:
            raise ValueError("Nombre vacío")

        # Verificar si ya existe un proceso igual
        if any(p[0] == nombre for p in procesos):
            messagebox.showwarning("Proceso duplicado", "Este proceso ya fue agregado.")
            return

        procesos.append((nombre, llegada, servicio))
        tree.insert("", tk.END, values=(nombre, llegada, servicio))
        entry_nombre.delete(0, tk.END)
        entry_llegada.delete(0, tk.END)
        entry_servicio.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Datos inválidos. Asegúrate de ingresar valores correctos.")


def iniciar_simulacion():
    algoritmo = combo_algoritmo.get()
    if not procesos:
        messagebox.showwarning("Advertencia", "Agrega al menos un proceso")
        return

    for widget in frame_grafico.winfo_children():
        widget.destroy()

    if algoritmo == "FCFS":
        resultados = fcfs(procesos)
        graficar_gantt(resultados)
    elif algoritmo == "SJF":
        resultados = sjf(procesos)
        graficar_gantt(resultados)
    elif algoritmo == "Round Robin":
        try:
            quantum = int(entry_quantum.get())
        except:
            messagebox.showerror("Error", "Ingresa un quantum válido para Round Robin")
            return
        resultados, historial = round_robin(procesos, quantum)
        graficar_gantt_rr(historial)
    else:
        return

    for item in tree_resultados.get_children():
        tree_resultados.delete(item)

    for r in resultados:
        tree_resultados.insert("", tk.END, values=r)

def limpiar_datos():
    global procesos
    procesos.clear()

    for item in tree.get_children():
        tree.delete(item)

    for item in tree_resultados.get_children():
        tree_resultados.delete(item)

    for widget in frame_grafico.winfo_children():
        widget.destroy()

    entry_nombre.delete(0, tk.END)
    entry_llegada.delete(0, tk.END)
    entry_servicio.delete(0, tk.END)
    entry_nombre.insert(0, "Nombre")
    entry_llegada.insert(0, "Llegada")
    entry_servicio.insert(0, "Servicio")
    entry_quantum.delete(0, tk.END)
    entry_quantum.insert(0, "Quantum")

def graficar_gantt(resultados):
    fig, gnt = plt.subplots()
    gnt.set_title('Diagrama de Gantt')
    gnt.set_xlabel('Tiempo')
    gnt.set_ylabel('Procesos')
    gnt.set_yticks([15 + i*10 for i in range(len(resultados))])
    gnt.set_yticklabels([r[0] for r in resultados])
    gnt.grid(True)

    for i, r in enumerate(resultados):
        gnt.broken_barh([(r[3], r[4]-r[3])], (10 + i*10, 9), facecolors=('tab:blue'))

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def graficar_gantt_rr(historial):
    fig, gnt = plt.subplots()
    gnt.set_title('Diagrama de Gantt RR')
    gnt.set_xlabel('Tiempo')
    gnt.set_ylabel('Procesos')
    procesos_unicos = list(dict.fromkeys([h[0] for h in historial]))
    gnt.set_yticks([15 + i*10 for i in range(len(procesos_unicos))])
    gnt.set_yticklabels(procesos_unicos)
    gnt.grid(True)

    for i, p in enumerate(procesos_unicos):
        for h in historial:
            if h[0] == p:
                gnt.broken_barh([(h[1], h[2]-h[1])], (10 + i*10, 9), facecolors='tab:green')

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Main app
root = tk.Tk()
root.title("Simulador de Planificación de Procesos")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

combo_algoritmo = ttk.Combobox(frame_input, values=["FCFS", "SJF", "Round Robin"])
combo_algoritmo.set("FCFS")
combo_algoritmo.grid(row=0, column=0, padx=5)

def toggle_quantum(*args):
    if combo_algoritmo.get() == "Round Robin":
        entry_quantum.grid(row=0, column=6, padx=5)
    else:
        entry_quantum.grid_remove()

combo_algoritmo.bind("<<ComboboxSelected>>", toggle_quantum)

entry_nombre = tk.Entry(frame_input)
entry_nombre.grid(row=0, column=1, padx=5)
entry_nombre.insert(0, "Nombre")

entry_llegada = tk.Entry(frame_input)
entry_llegada.grid(row=0, column=2, padx=5)
entry_llegada.insert(0, "Llegada")

entry_servicio = tk.Entry(frame_input)
entry_servicio.grid(row=0, column=3, padx=5)
entry_servicio.insert(0, "Servicio")

btn_agregar = tk.Button(frame_input, text="Agregar Proceso", command=agregar_proceso)
btn_agregar.grid(row=0, column=4, padx=5)

btn_simular = tk.Button(frame_input, text="Iniciar Simulación", command=iniciar_simulacion)
btn_simular.grid(row=0, column=5, padx=5)

btn_limpiar = tk.Button(frame_input, text="Limpiar Datos", command=limpiar_datos)
btn_limpiar.grid(row=0, column=7, padx=5)

entry_quantum = tk.Entry(frame_input)
entry_quantum.insert(0, "Quantum")
entry_quantum.grid(row=0, column=6, padx=5)
entry_quantum.grid_remove()

frame_tabla = tk.Frame(root)
frame_tabla.pack()

tree = ttk.Treeview(frame_tabla, columns=("Nombre", "Llegada", "Servicio"), show='headings')
for col in ("Nombre", "Llegada", "Servicio"):
    tree.heading(col, text=col)
    tree.column(col, width=80)
tree.pack()

label_resultado = tk.Label(root, text="Resultados:")
label_resultado.pack()

frame_resultados = tk.Frame(root)
frame_resultados.pack()

tree_resultados = ttk.Treeview(frame_resultados, columns=("Proceso", "Llegada", "Servicio", "Inicio", "Fin", "Retorno", "Espera", "Ret. Norm"), show='headings')
for col in ("Proceso", "Llegada", "Servicio", "Inicio", "Fin", "Retorno", "Espera", "Ret. Norm"):
    tree_resultados.heading(col, text=col)
    tree_resultados.column(col, width=80)
tree_resultados.pack()

frame_grafico = tk.Frame(root)
frame_grafico.pack(fill=tk.BOTH, expand=True)

root.mainloop()
