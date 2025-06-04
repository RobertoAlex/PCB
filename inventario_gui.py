# coding: utf-8
"""Aplicación de inventario con Tkinter y SQLite.

Esta versión corrige duplicados encontrados en el código de ejemplo y
simplifica algunas operaciones de base de datos.
"""

import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = Path(
    "C:/Users/raher/.spyder-py3/Inventario_Equipo_Medico/inventario_estructura_oficial.db"
)

# Conexión global
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Tabla de registro de movimientos
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_insumo INTEGER,
        nombre_insumo TEXT,
        tipo TEXT,
        cantidad INTEGER,
        fecha_movimiento TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """
)
conn.commit()

def registrar_movimiento(id_insumo: int, nombre: str, tipo: str, cantidad: int) -> None:
    """Guarda la operación de entrada o salida."""
    cursor.execute(
        """
        INSERT INTO movimientos (id_insumo, nombre_insumo, tipo, cantidad)
        VALUES (?, ?, ?, ?)
        """,
        (id_insumo, nombre, tipo, cantidad),
    )
    conn.commit()

def obtener_datos(filtro: str = ""):
    """Devuelve registros de `insumos` aplicando un filtro opcional."""
    if filtro:
        f = f"%{filtro}%"
        query = """
            SELECT * FROM insumos WHERE
                CAST(id AS TEXT) LIKE ? OR
                grupo LIKE ? OR
                nombre_grupo LIKE ? OR
                numero_insumo LIKE ? OR
                tipo_insumo LIKE ? OR
                folio_vale LIKE ? OR
                caracteristica LIKE ? OR
                compat_marca LIKE ? OR
                compat_modelo LIKE ? OR
                tamano LIKE ?
        """
        cursor.execute(query, (f,) * 10)
    else:
        cursor.execute("SELECT * FROM insumos")
    return cursor.fetchall()

def actualizar_tabla(filtro: str = "") -> None:
    """Refresca el Treeview y resalta las filas con poco stock."""
    for row in tree.get_children():
        tree.delete(row)

    datos = obtener_datos(filtro)

    cols = [c[1] for c in cursor.execute("PRAGMA table_info(insumos)")]
    idx_exist = cols.index("existencias")
    idx_min = cols.index("stock_minimo")

    for row in datos:
        exist = int(row[idx_exist])
        mini = int(row[idx_min])
        tag = "bajo" if exist < mini else ""
        tree.insert("", tk.END, values=row, tags=(tag,))

def registrar_salida() -> None:
    sel = tree.focus()
    if not sel:
        messagebox.showwarning("Atención", "Selecciona un insumo primero.")
        return

    vals = tree.item(sel, "values")
    cols = [c[1] for c in cursor.execute("PRAGMA table_info(insumos)")]
    idx_exist = cols.index("existencias")
    idx_num = cols.index("numero_insumo")

    insumo_id = vals[0]
    nombre = vals[idx_num]
    existencias = int(vals[idx_exist])

    def confirmar():
        try:
            cant = int(entry_cant.get())
            if cant <= 0:
                raise ValueError
            if cant > existencias:
                messagebox.showerror("Error", "No hay suficiente stock.")
                return
            nueva = existencias - cant
            cursor.execute(
                "UPDATE insumos SET existencias = ?, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?",
                (nueva, insumo_id),
            )
            registrar_movimiento(insumo_id, nombre, "salida", cant)
            conn.commit()
            actualizar_tabla(entry_busqueda.get())
            win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.")

    win = tk.Toplevel()
    win.title("Registrar salida")
    tk.Label(win, text="Cantidad a retirar:").pack(padx=10, pady=5)
    entry_cant = tk.Entry(win)
    entry_cant.pack(padx=10, pady=5)
    tk.Button(win, text="Confirmar", command=confirmar).pack(pady=10)

def registrar_entrada() -> None:
    sel = tree.focus()
    if not sel:
        messagebox.showwarning("Atención", "Selecciona un insumo primero.")
        return

    vals = tree.item(sel, "values")
    cols = [c[1] for c in cursor.execute("PRAGMA table_info(insumos)")]
    idx_exist = cols.index("existencias")
    idx_num = cols.index("numero_insumo")

    insumo_id = vals[0]
    nombre = vals[idx_num]
    existencias = int(vals[idx_exist])

    def confirmar():
        try:
            cant = int(entry_cant.get())
            if cant <= 0:
                raise ValueError
            nueva = existencias + cant
            cursor.execute(
                "UPDATE insumos SET existencias = ?, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?",
                (nueva, insumo_id),
            )
            registrar_movimiento(insumo_id, nombre, "entrada", cant)
            conn.commit()
            actualizar_tabla(entry_busqueda.get())
            win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.")

    win = tk.Toplevel()
    win.title("Registrar entrada")
    tk.Label(win, text="Cantidad a ingresar:").pack(padx=10, pady=5)
    entry_cant = tk.Entry(win)
    entry_cant.pack(padx=10, pady=5)
    tk.Button(win, text="Confirmar", command=confirmar).pack(pady=10)

def mostrar_historial() -> None:
    win = tk.Toplevel()
    win.title("Historial de movimientos")
    win.geometry("700x400")

    cols = ["ID", "ID Insumo", "Nombre", "Tipo", "Cantidad", "Fecha"]
    th = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        th.heading(c, text=c)
        th.column(c, anchor=tk.CENTER, width=100)
    th.pack(expand=True, fill="both")

    cursor.execute("SELECT * FROM movimientos ORDER BY fecha_movimiento DESC")
    for r in cursor.fetchall():
        th.insert("", tk.END, values=r)

def agregar_insumo() -> None:
    def confirmar():
        try:
            datos = (
                entry_grupo.get(),
                entry_ng.get(),
                entry_num.get(),
                entry_tipo.get(),
                entry_fv.get(),
                entry_car.get(),
                entry_cm.get(),
                entry_cmo.get(),
                entry_tam.get(),
                int(entry_exi.get()),
                entry_cad.get(),
                int(entry_min.get()),
            )
            cursor.execute(
                """
                INSERT INTO insumos (
                    grupo, nombre_grupo, numero_insumo, tipo_insumo,
                    folio_vale, caracteristica, compat_marca, compat_modelo,
                    tamano, existencias, caducidad, stock_minimo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                datos,
            )
            conn.commit()
            actualizar_tabla(entry_busqueda.get())
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Verifica los datos. {e}")

    win = tk.Toplevel()
    win.title("Agregar nuevo insumo")

    campos = [
        ("Grupo:", "grupo"),
        ("Nombre grupo:", "ng"),
        ("Número insumo:", "num"),
        ("Tipo insumo:", "tipo"),
        ("Folio vale:", "fv"),
        ("Característica:", "car"),
        ("Marca comp.:", "cm"),
        ("Modelo comp.:", "cmo"),
        ("Tamaño:", "tam"),
        ("Existencias:", "exi"),
        ("Caducidad (YYYY-MM-DD):", "cad"),
        ("Stock mínimo:", "min"),
    ]
    entradas = {}
    for txt, key in campos:
        tk.Label(win, text=txt).pack()
        e = tk.Entry(win)
        e.pack()
        entradas[key] = e

    entry_grupo = entradas["grupo"]
    entry_ng = entradas["ng"]
    entry_num = entradas["num"]
    entry_tipo = entradas["tipo"]
    entry_fv = entradas["fv"]
    entry_car = entradas["car"]
    entry_cm = entradas["cm"]
    entry_cmo = entradas["cmo"]
    entry_tam = entradas["tam"]
    entry_exi = entradas["exi"]
    entry_cad = entradas["cad"]
    entry_min = entradas["min"]

    tk.Button(win, text="Agregar", command=confirmar).pack(pady=10)

def mostrar_ventana() -> None:
    global tree, entry_busqueda

    raiz = tk.Tk()
    raiz.title("Inventario de Insumos Biomédicos")
    raiz.geometry("1200x600")

    tk.Label(raiz, text="Buscar (id, grupo, código, tipo, marca, etc):").pack(pady=5)
    entry_busqueda = tk.Entry(raiz, width=60)
    entry_busqueda.pack()

    tk.Button(
        raiz,
        text="Buscar",
        command=lambda: actualizar_tabla(entry_busqueda.get()),
    ).pack(pady=5)

    cols = [c[1] for c in cursor.execute("PRAGMA table_info(insumos)")]
    tree = ttk.Treeview(raiz, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor=tk.CENTER, width=100)

    sb = ttk.Scrollbar(raiz, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    sb.pack(fill="y", side="right")
    tree.pack(expand=True, fill="both")

    tree.tag_configure("bajo", background="tomato")

    tk.Button(raiz, text="Registrar salida", command=registrar_salida).pack(pady=5)
    tk.Button(raiz, text="Registrar entrada", command=registrar_entrada).pack(pady=5)
    tk.Button(raiz, text="Agregar nuevo insumo", command=agregar_insumo).pack(pady=5)
    tk.Button(raiz, text="Ver historial", command=mostrar_historial).pack(pady=5)

    actualizar_tabla()
    raiz.mainloop()

if __name__ == "__main__":
    try:
        mostrar_ventana()
    finally:
        conn.close()
