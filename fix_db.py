import sqlite3

conn = sqlite3.connect('instance/stockflow.db')

try:
    conn.execute('ALTER TABLE usuarios ADD COLUMN empresa_id INTEGER')
    print('usuarios.empresa_id agregada')
except Exception as e:
    print(f'usuarios: {e}')

try:
    conn.execute('ALTER TABLE productos ADD COLUMN empresa_id INTEGER')
    print('productos.empresa_id agregada')
except Exception as e:
    print(f'productos: {e}')

try:
    conn.execute('ALTER TABLE entradas ADD COLUMN empresa_id INTEGER')
    print('entradas.empresa_id agregada')
except Exception as e:
    print(f'entradas: {e}')

try:
    conn.execute('ALTER TABLE salidas ADD COLUMN empresa_id INTEGER')
    print('salidas.empresa_id agregada')
except Exception as e:
    print(f'salidas: {e}')

conn.commit()
conn.close()
print('Listo!')