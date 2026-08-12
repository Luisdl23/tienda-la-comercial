# Genera tienda.db con ventas historicas deterministas
# La Comercial - una sola sucursal (la dueña evalua abrir la segunda)
import sqlite3, random, os
from datetime import date, timedelta

random.seed(2026)
DB = "tienda.db"
if os.path.exists(DB):
    os.remove(DB)

con = sqlite3.connect(DB)
cur = con.cursor()
cur.executescript("""
CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL
);
CREATE TABLE ventas (
    id INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL
);
CREATE TABLE detalle_venta (
    id_venta INTEGER NOT NULL REFERENCES ventas(id),
    id_producto INTEGER NOT NULL REFERENCES productos(id),
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL
);
""")

productos = [
    (1, "Azucar 5 lb", "granos", 22.50),
    (2, "Frijol negro 1 lb", "granos", 9.75),
    (3, "Arroz 1 lb", "granos", 6.50),
    (4, "Aceite 900 ml", "abarrotes", 25.00),
    (5, "Cafe molido 460 g", "abarrotes", 48.00),
    (6, "Incaparina 450 g", "abarrotes", 21.00),
    (7, "Pasta 200 g", "abarrotes", 5.25),
    (8, "Agua pura galon", "bebidas", 12.00),
    (9, "Gaseosa 3 L", "bebidas", 18.50),
    (10, "Jabon de bola", "limpieza", 8.00),
    (11, "Cloro 1 L", "limpieza", 14.00),
    (12, "Detergente 500 g", "limpieza", 16.75),
]
cur.executemany("INSERT INTO productos VALUES (?,?,?,?)", productos)

inicio = date(2024, 1, 1)
fin = date(2026, 6, 30)
venta_id = 0
ventas_rows = []
detalle_rows = []
d = inicio
while d <= fin:
    # crecimiento sostenido + pico de diciembre
    dias_transcurridos = (d - inicio).days
    base = 90 + dias_transcurridos // 12          # crece con el tiempo
    if d.month == 12:
        base = int(base * 1.35)                    # temporada alta
    n_ventas = base + random.randint(-10, 10)
    for _ in range(n_ventas):
        venta_id += 1
        ventas_rows.append((venta_id, d.isoformat()))
        for _ in range(random.randint(1, 4)):
            pid, _, _, precio = random.choice(productos)
            detalle_rows.append((venta_id, pid, random.randint(1, 3), precio))
    d += timedelta(days=1)

cur.executemany("INSERT INTO ventas VALUES (?,?)", ventas_rows)
cur.executemany("INSERT INTO detalle_venta VALUES (?,?,?,?)", detalle_rows)
con.commit()

print(f"ventas: {venta_id}")
print(f"detalle: {len(detalle_rows)}")
con.close()
