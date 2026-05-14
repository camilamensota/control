import customtkinter as ctk # importamos la librería para la interfaz de usuario

#Comenzaremos a realizar la interfaz de usuario
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#crearemos la ventana para la interfaz que sera de 800*500
app = ctk.CTk()
app.geometry("2500*2500")
app.title("Control de gastos personales")

#creamos el titulo
titulo = ctk.CTkLabel(
    app,
    text="Control de gastos personales",
    font=("Arial", 28)
)

titulo.pack(pady=20)

#primero se pregunta los ingresos
entry_fecha_ingreso = ctk.CTkL

#aca haremos el campo para que el ususario ingrese el salario diario
entry_salario = ctk.CTkEntry(
    app,
    placeholder_text="Salario diario"
)

entry_salario.pack(pady=10)

#creamos el boton para calcular
boton = ctk.CTkButton(
    app,
    text="Calcular"
)

boton.pack(pady=10)

#se ejecuta la ventana
app.mainloop()



