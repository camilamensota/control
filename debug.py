import customtkinter as ctk
import database # Importamos la base de datos

# Le agregamos un parámetro (app_principal) para que reciba la ventana desde el main
def mostrar_ventana(app_principal):
    # 1. Creamos la ventana secundaria
    ventana_bd = ctk.CTkToplevel(app_principal)
    ventana_bd.title("Registros en la Base de Datos")
    ventana_bd.geometry("600x400")
    ventana_bd.attributes('-topmost', True)

    #Caja de texto
    caja_texto = ctk.CTkTextbox(ventana_bd, width=550, height=350)
    caja_texto.pack(pady=20)

    #Leer base de datos
    try:
        registros = database.obtener_movimientos()
        
        if len(registros) == 0:
            caja_texto.insert("0.0", "La base de datos está vacía en este momento.")
        else:
            for fila in registros:
                texto_fila = f"ID: {fila[0]} | {fila[1]} | {fila[2]} | ${fila[3]} | Desc: {fila[4]}\n"
                caja_texto.insert("end", texto_fila)
                caja_texto.insert("end", "-" * 70 + "\n")
                
    except Exception as e:
        caja_texto.insert("0.0", f"Error al leer la base de datos:\n{e}")