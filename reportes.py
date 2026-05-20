import customtkinter as ctk
import database # Importamos la base de datos
from tkinter import messagebox

def mostrar_ventana_reportes(app_principal):
    # Esconde la ventana del menú principal
    app_principal.withdraw()

    # 2. Creamos la ventana de reportes
    ventana_reportes = ctk.CTkToplevel(app_principal)
    ventana_reportes.title("Reportes Financieros")
    ventana_reportes.geometry("800x650")
    
    # Aseguramos que la ventana aparezca al frente
    ventana_reportes.attributes('-topmost', True)

    # Función para cerrar esta ventana y regresar
    def volver_al_menu():
        ventana_reportes.destroy()
        app_principal.deiconify()

    ventana_reportes.protocol("WM_DELETE_WINDOW", volver_al_menu)

    # Título
    titulo = ctk.CTkLabel(ventana_reportes, text="Dashboard de Reportes", font=("Arial", 24, "bold"))
    titulo.pack(pady=15)

    # Obtener datos de base de datos
    try:
        total_ingresos, total_gastos, _ = database.obtener_totales()
    except Exception as e:
        total_ingresos, total_gastos = 0.0, 0.0
        messagebox.showerror("Error", f"No se pudieron cargar los totales: {e}")


    # Contenedor invisible para meter las dos tarjetas de lado a lado
    frame_tarjetas = ctk.CTkFrame(ventana_reportes, fg_color="transparent")
    frame_tarjetas.pack(pady=15)

    # Funciones que se activarán al presionar cada cuadro
    def consultar_grafica_ingresos():
        messagebox.showinfo("Próximamente", "Aquí se desplegará la gráfica analítica de INGRESOS.")

    def consultar_grafica_gastos():
        messagebox.showinfo("Próximamente", "Aquí se desplegará la gráfica analítica de GASTOS (Estilo Mercado Pago).")

    # Botón de Ingresos
    btn_tarjeta_ingresos = ctk.CTkButton(
        frame_tarjetas,
        text=f"Total Ingresos\n\n${total_ingresos:.2f}",
        font=("Arial", 16, "bold"),
        width=250,
        height=100,
        fg_color="#1b5e20", 
        hover_color="#2e7d32",
        command=consultar_grafica_ingresos
    )
     
    btn_tarjeta_ingresos.pack(side="left", padx=20)

    # Botón de Gastos
    btn_tarjeta_gastos = ctk.CTkButton(
        frame_tarjetas,
        text=f"Total Gastos\n\n${total_gastos:.2f}",
        font=("Arial", 16, "bold"),
        width=250,
        height=100,
        fg_color="#b71c1c", # Rojo oscuro
        hover_color="#c62828",
        command=consultar_grafica_gastos
    )
    
    btn_tarjeta_gastos.pack(side="left", padx=20)



    # LISTA DE MOVIMIENTOS (PARTE INFERIOR)

    lbl_historial = ctk.CTkLabel(ventana_reportes, text="Historial Completo de Movimientos", font=("Arial", 16, "bold"))
    lbl_historial.pack(pady=(25, 5))

    # Frame con barra de desplazamiento integrada
    frame_lista = ctk.CTkScrollableFrame(ventana_reportes, width=600, height=300)
    frame_lista.pack(pady=10)

    try:
        registros = database.obtener_movimientos()
        
        if not registros:
            lbl_vacio = ctk.CTkLabel(frame_lista, text="No hay transacciones registradas aún.", font=("Arial", 14, "italic"))
            lbl_vacio.pack(pady=60)
        else:
            # Recorremos la lista al revés para que los movimientos más recientes salgan arriba
            for fila in reversed(registros):
                # Desempaquetamos la tupla de la BD: (id, tipo, categoria, monto, descripcion)
                id_mov, tipo, categoria, monto, descripcion = fila
                
                # Configuramos el diseño visual del renglón según el tipo
                if tipo == "Ingreso":
                    color_monto = "#4caf50" # Verde brillante para dinero entrante
                    detalles_texto = f"Ingreso directo" if categoria == "Sin categoría" else f"Ingreso ({categoria})"
                else:
                    color_monto = "#f44336" # Rojo brillante para dinero saliente
                    detalles_texto = f"Gasto en: {categoria}"

                # Si el usuario puso una descripción, la sumamos al texto
                if descripcion:
                    detalles_texto += f" —  \"{descripcion}\""

                # Mini caja contenedora para cada fila individual del historial
                fila_frame = ctk.CTkFrame(frame_lista, fg_color="transparent")
                fila_frame.pack(fill="x", pady=6, padx=10)

                # Texto descriptivo alineado a la izquierda
                lbl_info = ctk.CTkLabel(fila_frame, text=detalles_texto, font=("Arial", 13))
                lbl_info.pack(side="left")

                # Monto monetario alineado a la derecha
                lbl_precio = ctk.CTkLabel(
                    fila_frame, 
                    text=f"${monto:.2f}", 
                    font=("Arial", 13, "bold"),
                    text_color=color_monto
                )
                lbl_precio.pack(side="right")
                
                # Una sutil línea punteada para separar visualmente los renglones
                separador = ctk.CTkLabel(frame_lista, text="-" * 90, text_color="#333333")
                separador.pack()

    except Exception as e:
        lbl_error = ctk.CTkLabel(frame_lista, text=f"Error al conectar con el historial: {e}", text_color="red")
        lbl_error.pack(pady=20)


    
    # BOTÓN DE RETORNO
    
    btn_volver = ctk.CTkButton(
        ventana_reportes, 
        text="Volver al Menú Principal", 
        command=volver_al_menu,
        fg_color="#333333",
        hover_color="#555555"
    )
    btn_volver.pack(pady=20)