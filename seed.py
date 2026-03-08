from database import db
from models import Producto

def cargar_datos_iniciales():
    productos = [
        # DISCOS DE CORTE
        ("DC-001", "Disco corte 7\"",          "Discos de Corte",         290, 50),
        ("DC-002", "Disco corte 9\"",          "Discos de Corte",         300, 50),
        ("DC-003", "Disco corte 4.5 x 3mm",   "Discos de Corte",         250, 80),
        ("DC-004", "Disco corte 4.5 x 2.5mm", "Discos de Corte",         900, 100),
        ("DC-005", "Disco corte 4.5 x 1mm",   "Discos de Corte",         900, 100),
        # DISCOS DE DESBASTE
        ("DD-001", "Disco desbaste 4½\"",      "Discos de Desbaste",      110, 30),
        ("DD-002", "Disco desbaste 7\"",       "Discos de Desbaste",      250, 30),
        # DISCOS DE TRASLAPE
        ("DT-001", "Disco traslape 4.5\"",     "Discos de Traslape",      255, 50),
        # SOLDADURA
        ("SO-001", "7018 - 1/8",               "Soldadura",               175, 40),
        ("SO-002", "7018 - 3/32",              "Soldadura",               190, 40),
        ("SO-003", "6011 - 1/8",               "Soldadura",               285, 40),
        ("SO-004", "6011 - 3/32",              "Soldadura",               36,  40),
        # LIJAS
        ("LJ-001", "Lija 80 metal",            "Lijas",                   156, 30),
        ("LJ-002", "Lija 100 metal",           "Lijas",                   90,  30),
        ("LJ-003", "Lija 120 metal",           "Lijas",                   67,  30),
        ("LJ-004", "Lija 80 madera",           "Lijas",                   30,  20),
        ("LJ-005", "Lija 100 madera",          "Lijas",                   29,  20),
        ("LJ-006", "Lija 120 madera",          "Lijas",                   55,  20),
        # MATERIALES DE CONSTRUCCION
        ("MC-001", "Aquapanel 12.5mm",         "Materiales Construccion", 595, 50),
        ("MC-002", "Plancha ST 10mm",          "Materiales Construccion", 90,  20),
        ("MC-003", "Permanit 10mm",            "Materiales Construccion", 190, 30),
        ("MC-004", "Planchas RH 12.5",         "Materiales Construccion", 193, 30),
        ("MC-005", "Placa Diamant 12.5",       "Materiales Construccion", 50,  20),
        ("MC-006", "XPS Soprema",              "Materiales Construccion", 16,  5),
        ("MC-007", "Lana de vidrio libre",     "Materiales Construccion", 49,  10),
        ("MC-008", "Fonodan 70",               "Materiales Construccion", 25,  5),
        ("MC-009", "Emcekrette 40",            "Materiales Construccion", 20,  5),
        # PRODUCTOS RENNER
        ("RN-001", "Epomar B Rojo",            "Productos Renner",        2,   3),
        ("RN-002", "Catalizador Retanhe PE",   "Productos Renner",        20,  5),
        ("RN-003", "Rethane PE Negro",         "Productos Renner",        4,   3),
        ("RN-004", "Disolvente Epóxico",       "Productos Renner",        11,  3),
        ("RN-005", "Disolvente Poliuretano",   "Productos Renner",        5,   3),
        # OTROS PRODUCTOS
        ("OP-001", "Bekron D.A. Bodega",       "Otros Productos",         20,  5),
        ("OP-002", "Bekron D.A. San Antonio",  "Otros Productos",         32,  5),
        ("OP-003", "Masilla base",             "Otros Productos",         3,   2),
        ("OP-004", "A-01 Pega Albanileria",    "Otros Productos",         100, 20),
        ("OP-005", "Five Star",                "Otros Productos",         28,  5),
        ("OP-006", "Nafufill R",               "Otros Productos",         2,   2),
        ("OP-007", "Filler 16/40",             "Otros Productos",         6,   2),
        ("OP-008", "Pintura intumescente",     "Otros Productos",         100, 20),
        ("OP-009", "Velosit RM 205",           "Otros Productos",         6,   2),
        ("OP-010", "Velosit CW 111",           "Otros Productos",         6,   2),
        ("OP-011", "Velosit PC 222",           "Otros Productos",         7,   2),
        ("OP-012", "Velosit 453",              "Otros Productos",         1,   1),
        ("OP-013", "Policret 201",             "Otros Productos",         7,   2),
        ("OP-014", "Macropoxi 646 Sherwin W.", "Otros Productos",         1,   1),
        ("OP-015", "Funtac Dynal",             "Otros Productos",         1,   1),
    ]

    for codigo, nombre, categoria, stock, minimo in productos:
        db.session.add(Producto(
            codigo=codigo, nombre=nombre,
            categoria=categoria, stock=stock, minimo=minimo
        ))
    db.session.commit()
    print(f"✅ {len(productos)} productos cargados.")
