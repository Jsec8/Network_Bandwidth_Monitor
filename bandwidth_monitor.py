import psutil
import time
import csv
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

# Configuración para el gráfico en tiempo real
fig, ax = plt.subplots()
ax.set_xlabel('Tiempo')
ax.set_ylabel('Bytes por segundo')
ax.set_title('Monitor de Ancho de Banda')

# Deques para almacenar los datos de forma eficiente
MAX_PLOT_POINTS = 50  # Número máximo de puntos a mostrar en el gráfico
time_points = deque(maxlen=MAX_PLOT_POINTS)
sent_points = deque(maxlen=MAX_PLOT_POINTS)
recv_points = deque(maxlen=MAX_PLOT_POINTS)

# Archivo CSV para guardar los datos
CSV_FILENAME = 'bandwidth_data.csv'
csv_file = open(CSV_FILENAME, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Tiempo', 'Bytes enviados', 'Bytes recibidos'])
csv_file.close()

# Variable para controlar el estado del monitoreo
monitoring = True

# Umbrales para las alarmas (valores predeterminados altos para evitar alarmas iniciales)
sent_threshold = 1e9  # 1 GB/s
recv_threshold = 1e9  # 1 GB/s

def get_network_usage(interval=1):
    net_io = psutil.net_io_counters()
    bytes_sent, bytes_recv = net_io.bytes_sent, net_io.bytes_recv
    time.sleep(interval)
    net_io = psutil.net_io_counters()
    new_bytes_sent, new_bytes_recv = net_io.bytes_sent, net_io.bytes_recv

    sent_per_sec = (new_bytes_sent - bytes_sent) / interval
    recv_per_sec = (new_bytes_recv - bytes_recv) / interval

    return sent_per_sec, recv_per_sec

def update_plot(sent, recv):
    time_points.append(time.time())
    sent_points.append(sent)
    recv_points.append(recv)

    ax.clear()
    ax.plot(time_points, sent_points, label='Bytes enviados')
    ax.plot(time_points, recv_points, label='Bytes recibidos')
    ax.legend()
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Bytes por segundo')
    ax.set_title('Monitor de Ancho de Banda')
    fig.canvas.draw()

def save_to_csv(time_point, sent, recv):
    with open(CSV_FILENAME, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([time_point, sent, recv])

def check_thresholds(sent, recv):
    if sent > sent_threshold:
        messagebox.showwarning("Alerta de Ancho de Banda", f"El ancho de banda enviado ha superado el umbral: {sent} B/s")
    if recv > recv_threshold:
        messagebox.showwarning("Alerta de Ancho de Banda", f"El ancho de banda recibido ha superado el umbral: {recv} B/s")

def start_monitoring():
    global monitoring
    print("Monitoring network bandwidth usage...")
    try:
        while monitoring:
            sent, recv = get_network_usage()
            current_time = time.time()
            print(f"Bytes sent: {sent} B/s, Bytes received: {recv} B/s")
            update_plot(sent, recv)
            save_to_csv(current_time, sent, recv)
            check_thresholds(sent, recv)
            root.update()  # Actualiza la interfaz gráfica
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    finally:
        csv_file.close()

def stop_monitoring():
    global monitoring
    monitoring = False
    print("Monitoring stopped.")
    root.quit()

def set_thresholds():
    global sent_threshold, recv_threshold
    try:
        sent_threshold = float(sent_threshold_entry.get())
        recv_threshold = float(recv_threshold_entry.get())
        messagebox.showinfo("Umbrales establecidos", "Los umbrales se han establecido correctamente.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para los umbrales.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Monitor de Ancho de Banda")

# Área para mostrar el gráfico
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Entradas para los umbrales
threshold_frame = ttk.Frame(root)
threshold_frame.pack(pady=10)

ttk.Label(threshold_frame, text="Umbral de Bytes Enviados:").grid(row=0, column=0, padx=5)
sent_threshold_entry = ttk.Entry(threshold_frame)
sent_threshold_entry.grid(row=0, column=1, padx=5)

ttk.Label(threshold_frame, text="Umbral de Bytes Recibidos:").grid(row=1, column=0, padx=5)
recv_threshold_entry = ttk.Entry(threshold_frame)
recv_threshold_entry.grid(row=1, column=1, padx=5)

set_thresholds_button = ttk.Button(threshold_frame, text="Establecer Umbrales", command=set_thresholds)
set_thresholds_button.grid(row=2, column=0, columnspan=2, pady=5)

# Botón para detener el monitoreo
stop_button = ttk.Button(root, text="Detener Monitoreo", command=stop_monitoring)
stop_button.pack(pady=10)

# Inicia el monitoreo inmediatamente
root.after(1000, start_monitoring)

# Ejecuta el loop principal de la interfaz gráfica
root.mainloop()






