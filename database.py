import sqlite3 #importa la libreria para usar sql

conexion = sqlite3.connect("gastos.db") #se conecta a la base de datos llamada gastos

cursor = conexion.cursor()
#le dice a sql que si no existe la tabla movimientos que la cree
cursor.execute("""
CREATE TABLE IF NOT EXISTS movimientos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    tipo TEXT,

    categoria TEXT,

    monto REAL,

    descripcion TEXT
)
""")

conexion.commit()

# =========================
# FUNCIÓN PARA GUARDAR
# =========================

def guardar_movimiento(tipo, categoria, monto, descripcion):

    cursor.execute("""

    INSERT INTO movimientos
    (tipo, categoria, monto, descripcion)

    VALUES (?, ?, ?, ?)

    """, (tipo, categoria, monto, descripcion))

    conexion.commit()

# =========================
# FUNCIÓN PARA OBTENER DATOS
# =========================

def obtener_movimientos():

    cursor.execute("""

    SELECT * FROM movimientos

    """)

    return cursor.fetchall()

# ==========================================
# OBTENER LOS TOTALES (INGRESOS, GASTOS Y SALDO)
# ==========================================
def obtener_totales():
    # Usamos 'with' para abrir y cerrar la conexión de forma segura
    with sqlite3.connect("gastos.db") as conexion:
        cursor = conexion.cursor()
        
        # Sumamos todos los montos donde el tipo sea 'Ingreso'
        cursor.execute("SELECT SUM(monto) FROM movimientos WHERE tipo='Ingreso'")
        # Si la suma da None (porque no hay ingresos aún), le asignamos 0.0
        total_ingresos = cursor.fetchone()[0] or 0.0 
        
        # Sumamos todos los montos donde el tipo sea 'Gasto'
        cursor.execute("SELECT SUM(monto) FROM movimientos WHERE tipo='Gasto'")
        total_gastos = cursor.fetchone()[0] or 0.0
        
        # Calculamos el saldo final
        saldo_actual = total_ingresos - total_gastos
        
        # Devolvemos los 3 valores para que tu main.py los use
        return total_ingresos, total_gastos, saldo_actual