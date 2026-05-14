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