import customtkinter as ctk #libreria para el gui

#establece los colores de la interfaz
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#crea la ventana de la interfaz
app = ctk.CTk()
app.geometry("900x600")
app.title("Control de gastos personales")

#creamos una caja de encabezado
header_frame = ctk.CTkFrame(app)
header_frame.pack(
    fill="x",
    pady=10
)

#titulo y formato de la ventana
titulo = ctk.CTkLabel(
    app,
    text="Control de gastos personales",
    font=("Arial", 30)
)
titulo.pack(pady=20)

#aca va el guardado del registro de ingresos, gastos y saldo actual
label_ingreso = ctk.CTkLabel(
    app,
    text="Ingresos: $0",
    font=("Arial",24)
)
label_ingreso.pack(pady=10)
#gasto
label_gastos = ctk.CTkLabel(
    app,
    text="Gastos: $0",
    font=("Arial",24)
)
label_gastos.pack(pady=10)
#saldo actual
label_saldo = ctk.CTkLabel(
    app,
    text="Saldo Actual: $0",
    font=("Arial", 24)
)
label_saldo.pack(pady=10)

#ComboBox nos sirve para elegir entre varias opciones sin tener que teclearlo, aca solo daremos opcion de ingreso o gasto
combo_tipo = ctk.CTkComboBox(
    app,
    values=["Ingreso", "Gasto"],
    width=300
)
combo_tipo.pack(pady=10)

#agragamos una categoria para que el usuario tenga un conocimiento de en donde gasta su dinero
entry_categoria = ctk.CTkEntry(
    app,
    placeholder_text="Categoría",
    width=300
)
entry_categoria.pack(pady=10)

#espacio para que el usuario ingrese su gasto o su ingreso
entry_monto = ctk.CTkEntry(
    app,
    placeholder_text="Monto",
    width=300
)
entry_monto.pack(pady=10)

#aca el usuario puede dar una descripcion de lo que ingreso o gasto
entry_descripcion = ctk.CTkEntry(
    app,
    placeholder_text="Descripción",
    width=300
)
entry_descripcion.pack(pady=10)

#guarda la información de los movimientos
btn_guardar = ctk.CTkButton(
    app,
    text="Guardar movimiento"
)
btn_guardar.pack(pady=15)

label_historial = ctk.CTkLabel(
    app,
    text="Historial",
    font=("Arial",15)
)
label_historial.pack(pady=5)

#le da al usuario un historial de todo lo que lleva
textbox = ctk.CTkTextbox(
    app,
    width=700,
    height=200
)
textbox.pack(pady=10)

#ejecuta la ventana
app.mainloop()