import customtkinter as ctk #libreria para el gui
from tkinter import messagebox # Importamos las ventanas de alerta
import database
import debug

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

#ComboBox para tipo
combo_tipo = ctk.CTkComboBox(
    form_frame,
    values=["Ingreso", "Gasto"],
    width=300
)
combo_tipo.pack(pady=10)

#ComboBox para categoria
lista_categorias = [
    "Comida y bebidas", "Supermercado", "Transporte", "Comisiones y cargos", 
    "Créditos y financiación", "Cuentas y servicios", "Deportes", "Donaciones", 
    "Educación", "Electrónica", "Entretenimiento", "Hogar", "Impuestos", 
    "Inversiones", "Mascotas", "Retiros en efectivo", "Ropa", 
    "Salud y cuidado personal", "Servicios profesionales", "Shopping", 
    "Suscripciones", "Tarjeta de crédito", "Transferencias a cuentas propias", 
    "Viajes", "Otro"
]

combo_categoria = ctk.CTkComboBox(
    form_frame,
    values=lista_categorias,
    width=300
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

# ==========================================
# FUNCIÓN DE VALIDACIÓN ACTUALIZADA
# ==========================================
def validar_y_guardar():
    tipo = combo_tipo.get()
    categoria = combo_categoria.get()
    monto_texto = entry_monto.get()
    descripcion = entry_descripcion.get()

    # 1. Validamos la categoría SOLO si es un Gasto
    if tipo == "Gasto":
        if categoria == "Selecciona una categoría" or categoria == "":
            messagebox.showwarning("Faltan datos", "Por favor, selecciona una categoría para el gasto.")
            return
    else:
        # Si es un Ingreso y dejaron el texto por defecto, lo limpiamos
        if categoria == "Selecciona una categoría":
            categoria = "Sin categoría" # O puedes dejarlo como "" (vacío) si lo prefieres

    # 2. Validamos que el monto no esté vacío
    if monto_texto == "":
        messagebox.showwarning("Faltan datos", "Por favor, ingresa un monto.")
        return

    # 3. Validamos que el monto sea un número válido
    try:
        monto_numerico = float(monto_texto)
        if monto_numerico <= 0:
            messagebox.showerror("Error", "El monto debe ser mayor a cero.")
            return
    except ValueError:
        messagebox.showerror("Error de formato", "El monto debe ser un número válido. (Ej. 150 o 150.50)")
        return

    # 4. Si los datos son válidos, los guardamos en la base de datos
    try:
        # Llamamos a la función del archivo database.py
        database.guardar_movimiento(tipo, categoria, monto_numerico, descripcion)
        
        # Avisamos al usuario que se guardó con éxito
        messagebox.showinfo("Éxito", "¡Movimiento guardado correctamente!")
        
        # OPCIONAL: Limpiar los campos para que el usuario pueda ingresar otro movimiento
        entry_monto.delete(0, 'end')
        entry_descripcion.delete(0, 'end')
        combo_categoria.set("Selecciona una categoría")
        
    except Exception as e:
        # Por si ocurre algún error inesperado con el archivo o la BD
        messagebox.showerror("Error de Base de Datos", f"No se pudo guardar el movimiento: {e}")

# ==========================================


# Botón para guardar
btn_guardar = ctk.CTkButton(
    form_frame,
    text="Guardar movimiento",
    command=validar_y_guardar
)
btn_guardar.pack(pady=15)

# Botón temporal para ver la BD (conectado al nuevo módulo)
btn_ver_bd = ctk.CTkButton(
    form_frame,
    text="Ver Base de Datos (Debug)",
    # Usamos lambda para poder pasarle la variable 'app' sin que se ejecute al instante
    command=lambda: debug.mostrar_ventana(app), 
    fg_color="gray", 
    hover_color="darkgray"
)
btn_ver_bd.pack(pady=5)

# Ejecuta la ventana
app.mainloop()