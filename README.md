
# 🖥️ Simulador de Planificación de Procesos

Este proyecto es una aplicación de escritorio desarrollada con `Tkinter` que permite simular y visualizar diferentes **algoritmos de planificación de procesos** utilizados en sistemas operativos. A través de una interfaz gráfica intuitiva, el usuario puede agregar procesos, elegir un algoritmo de planificación y visualizar el resultado tanto en tabla como en un diagrama de Gantt.

---

## 📌 Características

- Soporte para los algoritmos:
  - **FCFS** (First Come, First Served)
  - **SJF** (Shortest Job First, no expropiativo)
  - **Round Robin** (con quantum configurable)
- Interfaz gráfica amigable y responsiva con `Tkinter`.
- Visualización de los resultados en:
  - Tabla detallada de tiempos.
  - Diagrama de Gantt (con `matplotlib`).
- Validación para evitar procesos duplicados.
- Botón para limpiar todos los datos y reiniciar la simulación.

---

## 🧠 Algoritmos implementados

### 🔹 FCFS (First Come, First Served)
Planifica los procesos en el orden de llegada. No prioriza tiempo de ejecución.

### 🔹 SJF (Shortest Job First)
Selecciona el proceso más corto entre los disponibles en el tiempo actual. No expropiativo.

### 🔹 Round Robin
Cada proceso se ejecuta por un quantum fijo en orden de llegada, de forma cíclica (expropiativo).

---

## 🧰 Requisitos

- Python 3.7+
- Librerías:
  - `tkinter` (viene incluida en la mayoría de instalaciones de Python)
  - `matplotlib`

Instala matplotlib si no lo tienes:

```bash
pip install matplotlib
```

---

## ▶️ Cómo ejecutar

1. Descarga el archivo Python (por ejemplo: `simulador.py`).
2. Ejecuta el script:

```bash
python simulador.py
```

3. Aparecerá la ventana gráfica donde puedes:
   - Agregar procesos (nombre, tiempo de llegada y tiempo de servicio).
   - Seleccionar el algoritmo deseado.
   - (Opcional) Ingresar el quantum para Round Robin.
   - Iniciar la simulación y ver resultados.
   - Limpiar datos para una nueva simulación.

---

## 📷 Capturas de pantalla

> Puedes agregar aquí capturas de tu interfaz en uso:
> - Tabla de procesos
> - Resultado con diagrama de Gantt
> - Ejemplo con Round Robin

---

## 🛠️ Estructura del Código

- `fcfs()`, `sjf()`, `round_robin()`: funciones principales para los algoritmos.
- `agregar_proceso()`, `iniciar_simulacion()`, `limpiar_datos()`: funciones GUI.
- `graficar_gantt()` y `graficar_gantt_rr()`: visualización de los resultados.
- `Tkinter`: interfaz gráfica principal.

---

## 📄 Licencia

Este proyecto es de uso educativo y libre para modificaciones personales.

---

## ✍️ Autor

Desarrollado por Sergio Alejandro

---
