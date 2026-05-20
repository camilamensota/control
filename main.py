import customtkinter as ctk #libreria para el gui
from tkinter import messagebox # Importamos las ventanas de alerta
import database
import debug
import graficas
import reportes

#establece los colores de la interfaz
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#crea la ventana de la interfaz
app = ctk.CTk()
app.geometry("900x600")
app.title("Control de gastos personales")

#creamos una caja de encabezado
header_frame = ctk.CTkFrame(app)
header_frame.pack(fill="x", pady=10)

#creamos una caja para los forms
form_frame = ctk.CTkFrame(app)
form_frame.pack(fill="x", pady=10)

#titulo y formato de la ventana
titulo = ctk.CTkLabel(
    header_frame, 
    text="Control de gastos personales",
    font=("Arial", 30)
)
titulo.pack(pady=20)

#aca va el guardado del registro de ingresos, gastos y saldo actual
label_ingreso = ctk.CTkLabel(header_frame, text="Ingresos: $0", font=("Arial",24))
label_ingreso.pack(pady=10)

label_gastos = ctk.CTkLabel(header_frame, text="Gastos: $0", font=("Arial",24))
label_gastos.pack(pady=10)

label_saldo = ctk.CTkLabel(header_frame, text="Saldo Actual: $0", font=("Arial", 24))
label_saldo.pack(pady=10)


# LISTAS DE CATEGORÍAS Y FUNCIÓN DINÁMICA QUE DEPENDE DE GASTO/INGRESO

categorias_gastos = [
    "Comida y bebidas", "Supermercado", "Transporte", "Comisiones y cargos", 
    "Créditos y financiación", "Cuentas y servicios", "Deportes", "Donaciones", 
    "Educación", "Electrónica", "Entretenimiento", "Hogar", "Impuestos", 
    "Inversiones", "Mascotas", "Retiros en efectivo", "Ropa", 
    "Salud y cuidado personal", "Servicios profesionales", "Shopping", 
    "Suscripciones", "Tarjeta de crédito", "Transferencias a cuentas propias", 
    "Viajes", "Otro"
]

categorias_ingresos = [
    "Trabajo / Sueldo", "Negocio", "Inversiones", "Ventas", "Freelance", "Regalos", "Otro"
]

def cambiar_categorias_dinamicas(seleccion):
    # Cambiamos las opciones las boxes de categorías según lo elegido
    if seleccion == "Ingreso":
        combo_categoria.configure(values=categorias_ingresos)
    elif seleccion == "Gasto":
        combo_categoria.configure(values=categorias_gastos)
    
    # Reiniciamos el texto por defecto para forzar la selección
    combo_categoria.set("Selecciona una categoría")



# Tipo
combo_tipo = ctk.CTkComboBox(
    form_frame,
    values=["Ingreso", "Gasto"],
    width=300,
    state="readonly",
    command=cambiar_categorias_dinamicas # Llama a la función al cambiar
)
combo_tipo.set("Ingreso")
combo_tipo.pack(pady=10)

#Caja para categoria, iniciamos con las de ingresos por el valor por defecto
combo_categoria = ctk.CTkComboBox(
    form_frame,
    values=categorias_ingresos,
    width=300,
    state="readonly"
)
combo_categoria.set("Selecciona una categoría") 
combo_categoria.pack(pady=10)

#Monto
entry_monto = ctk.CTkEntry(
    form_frame,
    placeholder_text="Monto",
    width=300
)
entry_monto.pack(pady=10)

#Descripción
entry_descripcion = ctk.CTkEntry(
    form_frame,
    placeholder_text="Descripción",
    width=300
)
entry_descripcion.pack(pady=10)


# FUNCIÓN DE VALIDACIÓN

def validar_y_guardar():
    tipo = combo_tipo.get()
    categoria = combo_categoria.get()
    monto_texto = entry_monto.get()
    descripcion = entry_descripcion.get()

    # Validamos la categoría estricta para AMBOS (Ingreso y Gasto)
    if categoria == "Selecciona una categoría" or categoria == "":
        messagebox.showwarning("Faltan datos", f"Por favor, selecciona una categoría para el {tipo.lower()}.")
        return

    # Validamos que el monto no esté vacío
    if monto_texto == "":
        messagebox.showwarning("Faltan datos", "Por favor, ingresa un monto.")
        return

    # Validamos que el monto sea un número válido
    try:
        monto_numerico = float(monto_texto)
        if monto_numerico <= 0:
            messagebox.showerror("Error", "El monto debe ser mayor a cero.")
            return
    except ValueError:
        messagebox.showerror("Error de formato", "El monto debe ser un número válido. (Ej. 150 o 150.50)")
        return
    
    
    #Aquí evitamos gastar dinero que no tenemos
    if tipo == "Gasto":
        # Traemos los números actuales desde la base de datos
        ingresos_actuales, gastos_actuales, saldo_actual = database.obtener_totales()
        
        # Si el gasto que quieren registrar es mayor al dinero que hay en el saldo
        if monto_numerico > saldo_actual:
            messagebox.showerror("Fondos insuficientes", f"No puedes registrar este gasto.\n\nTu saldo actual es de ${saldo_actual:.2f}\nIntentas gastar: ${monto_numerico:.2f}")
            return # El return frena la función y evita que se guarde
    

    # Si los datos son válidos, los guardamos en la base de datos
    try:
        # Llamamos a la función del archivo database.py
        database.guardar_movimiento(tipo, categoria, monto_numerico, descripcion)
        
        # Avisamos al usuario que se guardó con éxito
        messagebox.showinfo("Éxito", "¡Movimiento guardado correctamente!")
        
        # Limpiar los campos para el siguiente registro
        entry_monto.delete(0, 'end')
        entry_descripcion.delete(0, 'end')
        combo_categoria.set("Selecciona una categoría")
        
        # Actualizamos la pantalla de totales
        actualizar_pantalla_totales()
        
    except Exception as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudo guardar el movimiento: {e}")



def actualizar_pantalla_totales():
    try:
        # Traemos todos los registros guardados
        registros = database.obtener_movimientos()
        
        total_ingresos = 0.0
        total_gastos = 0.0
        
        # Recorremos fila por fila para hacer las sumas
        for fila in registros:
            tipo = fila[1]
            monto = fila[3]
            
            if tipo == "Ingreso":
                total_ingresos += monto
            elif tipo == "Gasto":
                total_gastos += monto
                
        # Calculamos el saldo neto
        saldo_actual = total_ingresos - total_gastos
        
        # Modificamos el texto
        label_ingreso.configure(text=f"Ingresos: ${total_ingresos:.2f}")
        label_gastos.configure(text=f"Gastos: ${total_gastos:.2f}")
        label_saldo.configure(text=f"Saldo Actual: ${saldo_actual:.2f}")
        
    except Exception as e:
        print(f"Error al actualizar los totales: {e}")


# ZONA DE BOTONES


# Botón para guardar
btn_guardar = ctk.CTkButton(
    form_frame,
    text="Guardar movimiento",
    command=validar_y_guardar
)
btn_guardar.pack(pady=15)

# Botón de Reportes
btn_actividad = ctk.CTkButton(
    form_frame,
    text="Ver Actividad (Reportes)",
    command=lambda: reportes.mostrar_ventana_reportes(app),
    fg_color="green", 
    hover_color="darkgreen"
)
btn_actividad.pack(pady=5)

# Botón Gráficas
btn_ver_graficas = ctk.CTkButton(
    form_frame,
    text="Ver Gráficas Estadísticas",
    command=lambda: graficas.mostrar_graficas(app),
    fg_color="#2b719e",
    hover_color="#1f5070"
)
btn_ver_graficas.pack(pady=5)

# Botónpara ver la BD
btn_ver_bd = ctk.CTkButton(
    form_frame,
    text="Ver Base de Datos (Debug)",
    command=lambda: debug.mostrar_ventana(app), 
    fg_color="gray", 
    hover_color="darkgray"
)
btn_ver_bd.pack(pady=5)

# Llamamos a la función aquí para que cargue los datos guardados al abrir la app
actualizar_pantalla_totales()

# Ejecuta la ventana
app.mainloop()