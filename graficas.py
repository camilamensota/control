import customtkinter as ctk
import database
# Importaciones especiales para incrustar Matplotlib en Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def mostrar_graficas(app_principal):
    # 1. Crear ventana secundaria (Toplevel)
    ventana_graficas = ctk.CTkToplevel(app_principal)
    ventana_graficas.title("Estadísticas y Gráficas")
    ventana_graficas.geometry("850x550")
    ventana_graficas.attributes("-topmost", True)  # La mantiene al frente inicialmente

    # 2. Obtener los datos desde la base de datos
    try:
        registros = database.obtener_movimientos()
    except Exception as e:
        lbl_err = ctk.CTkLabel(
            ventana_graficas, text=f"Error al cargar base de datos: {e}"
        )
        lbl_err.pack(pady=20)
        return

    # Si no hay datos, mostrar un aviso y no renderizar gráficos vacíos
    if not registros:
        lbl_vacio = ctk.CTkLabel(
            ventana_graficas,
            text="No hay registros suficientes para generar gráficas.",
            font=("Arial", 16),
        )
        lbl_vacio.pack(pady=100)
        return

    # 3. Procesar los datos de la BD
    total_ingresos = 0.0
    total_gastos = 0.0
    gastos_por_categoria = {}

    for fila in registros:
        # fila[1] = tipo, fila[2] = categoria, fila[3] = monto
        tipo = fila[1]
        categoria = fila[2]
        monto = fila[3]

        if tipo == "Ingreso":
            total_ingresos += monto
        elif tipo == "Gasto":
            total_gastos += monto
            # Sumamos al acumulado de esa categoría específica
            gastos_por_categoria[categoria] = (
                gastos_por_categoria.get(categoria, 0) + monto
            )

    # 4. Configurar el diseño de las gráficas con Matplotlib
    # Creamos 1 fila con 2 columnas de gráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Estilo oscuro para que combine con CustomTkinter (Fondo #242424)
    fig.patch.set_facecolor("#242424")

    # --- GRÁFICA 1: BALANCE GENERAL (Barras) ---
    ejes_x = ["Ingresos", "Gastos"]
    valores_y = [total_ingresos, total_gastos]
    colores_barras = ["#1f6aa5", "#bd3a3a"]  # Azul ctk y Rojo para gastos

    ax1.bar(ejes_x, valores_y, color=colores_barras, width=0.5)
    ax1.set_title(
        "Balance General ($)", color="white", fontsize=14, fontweight="bold"
    )
    ax1.set_facecolor("#2b2b2b")
    ax1.tick_params(colors="white", labelsize=11)
    ax1.grid(True, linestyle="--", alpha=0.2, color="white")

    # --- GRÁFICA 2: GASTOS POR CATEGORÍA (Pastel) ---
    if gastos_por_categoria:
        categorias = list(gastos_por_categoria.keys())
        montos_categorias = list(gastos_por_categoria.values())

        # Dibujar gráfico de pastel
        wedges, texts, autotexts = ax2.pie(
            montos_categorias,
            labels=categorias,
            autopct="%1.1f%%",
            startangle=90,
            textprops=dict(color="white"),
        )
        ax2.set_title(
            "Distribución de Gastos",
            color="white",
            fontsize=14,
            fontweight="bold",
        )

        # Hacer los textos internos legibles
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(10)
    else:
        # Si hay ingresos pero 0 gastos
        ax2.text(
            0.5,
            0.5,
            "Sin gastos registrados",
            color="white",
            ha="center",
            va="center",
            fontsize=12,
        )
        ax2.axis("off")

    plt.tight_layout()

    # 5. Dibujar e Incrustar la gráfica en la ventana de CustomTkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

    # Limpieza de memoria al cerrar la ventana secundaria
    def al_cerrar():
        plt.close(fig)  # Cierra la figura de matplotlib en segundo plano
        ventana_graficas.destroy()

    ventana_graficas.protocol("WM_DELETE_WINDOW", al_cerrar)