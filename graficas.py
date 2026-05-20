import customtkinter as ctk
import database
# Importaciones especiales para incrustar Matplotlib en Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def mostrar_graficas(app_principal):
    #Crear ventana secundaria (Toplevel)
    ventana_graficas = ctk.CTkToplevel(app_principal)
    ventana_graficas.title("Panel de Control Estadístico")
    
    #Ancho de ventana
    ventana_graficas.geometry("1350x650")
    ventana_graficas.attributes("-topmost", True)

    # Función para cerrar y limpiar memoria
    def al_cerrar():
        plt.close('all') 
        ventana_graficas.destroy()

    # 2. Obtener los datos
    try:
        registros = database.obtener_movimientos()
    except Exception as e:
        lbl_err = ctk.CTkLabel(ventana_graficas, text=f"Error: {e}")
        lbl_err.pack(pady=20)
        ctk.CTkButton(ventana_graficas, text="Volver", command=al_cerrar).pack()
        return

    if not registros:
        lbl_vacio = ctk.CTkLabel(ventana_graficas, text="No hay registros para graficar.", font=("Arial", 16))
        lbl_vacio.pack(pady=100)
        ctk.CTkButton(ventana_graficas, text="Volver al Menú Principal", command=al_cerrar).pack()
        return

    #Procesar los datos (Ingresos y Gastos por categoría)
    total_ingresos = 0.0
    total_gastos = 0.0
    gastos_por_categoria = {}
    ingresos_por_categoria = {}

    for fila in registros:
        tipo, categoria, monto = fila[1], fila[2], fila[3]

        if tipo == "Ingreso":
            total_ingresos += monto
            ingresos_por_categoria[categoria] = ingresos_por_categoria.get(categoria, 0) + monto
        elif tipo == "Gasto":
            total_gastos += monto
            gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0) + monto

    #Configurar Matplotlib con 3 columnas para las 3 graficas
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    plt.subplots_adjust(wspace=0.4)
    fig.patch.set_facecolor("#242424")

    # GRÁFICA 1: BALANCE GENERAL (Barras)
    ax1.bar(["Ingresos", "Gastos"], [total_ingresos, total_gastos], color=["#1f6aa5", "#bd3a3a"], width=0.6)
    ax1.set_title("Balance General ($)", color="white", fontsize=12, fontweight="bold")
    ax1.set_facecolor("#2b2b2b")
    ax1.tick_params(colors="white")
    ax1.grid(True, linestyle="--", alpha=0.1, color="white")

    # GRÁFICA 2: DISTRIBUCIÓN DE INGRESOS (Pastel)
    if ingresos_por_categoria:

        wedges2, texts2, autotexts2 = ax2.pie(
            list(ingresos_por_categoria.values()),
            labels=list(ingresos_por_categoria.keys()),
            autopct="%1.1f%%",
            startangle=140,
            textprops=dict(color="white", fontsize=9)
        )
        ax2.set_title("Origen de Ingresos", color="#2ecc71", fontsize=12, fontweight="bold")
    else:
        ax2.text(0.5, 0.5, "Sin ingresos", color="white", ha="center")
        ax2.axis("off")

    # GRÁFICA 3: DISTRIBUCIÓN DE GASTOS (Pastel)
    if gastos_por_categoria:
        
        wedges3, texts3, autotexts3 = ax3.pie(
            list(gastos_por_categoria.values()),
            labels=list(gastos_por_categoria.keys()),
            autopct="%1.1f%%",
            startangle=140,
            textprops=dict(color="white", fontsize=9)
        )
        ax3.set_title("Destino de Gastos", color="#e74c3c", fontsize=12, fontweight="bold")
    else:
        ax3.text(0.5, 0.5, "Sin gastos", color="white", ha="center")
        ax3.axis("off")

    # Espacios entre gráficas
    plt.tight_layout()

    # Incrustar en CustomTkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # BOTÓN VOLVER AL MENU
    btn_volver = ctk.CTkButton(
        ventana_graficas, 
        text="Volver al Menú Principal", 
        command=al_cerrar,
        fg_color="#3d3d3d",
        hover_color="#555555",
        height=40,
        font=("Arial", 14, "bold")
    )
    btn_volver.pack(pady=15)

    ventana_graficas.protocol("WM_DELETE_WINDOW", al_cerrar)