import sqlite3
import os

def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', '..', 'data', 'produccion.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return db_path

def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bobinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ancho REAL,
            diametro REAL,
            gramaje REAL,
            peso REAL,
            bobina_nro TEXT,
            sec TEXT,
            orden_fab TEXT,
            fecha TEXT,
            turno TEXT,
            codcal TEXT,
            desccal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_bobina(nueva_bobina):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bobinas (ancho, diametro, gramaje, peso, bobina_nro, sec, orden_fab, fecha, turno, codcal, desccal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        nueva_bobina.ancho,
        nueva_bobina.diametro,
        nueva_bobina.gramaje,
        nueva_bobina.peso,
        nueva_bobina.bobina_nro,
        nueva_bobina.sec,
        nueva_bobina.orden_fab,
        nueva_bobina.fecha,
        nueva_bobina.turno,
        nueva_bobina.calidad[:2],  # codcal
        nueva_bobina.calidad[3:]   # desccal
    ))
    conn.commit()
    conn.close()

def update_bobina(nueva_bobina):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE bobinas
        SET ancho = ?, diametro = ?, gramaje = ?, peso = ?, orden_fab = ?, fecha = ?, turno = ?, codcal = ?, desccal = ?
        WHERE bobina_nro = ? AND sec = ?
    ''', (
        nueva_bobina.ancho,
        nueva_bobina.diametro,
        nueva_bobina.gramaje,
        nueva_bobina.peso,
        nueva_bobina.orden_fab,
        nueva_bobina.fecha,
        nueva_bobina.turno,
        nueva_bobina.calidad[:2],  # codcal
        nueva_bobina.calidad[3:],  # desccal
        nueva_bobina.bobina_nro,
        nueva_bobina.sec
    ))
    conn.commit()
    conn.close()

#def bobina_exists(nueva_bobina):
def bobina_exists(nueva_bobina):    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM bobinas WHERE bobina_nro = ? AND sec = ?
    ''', (nueva_bobina.bobina_nro, nueva_bobina.sec))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def get_max_sec(bobina_nro):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT MAX(CAST(sec AS INTEGER)) FROM bobinas WHERE bobina_nro = ?
    ''', (bobina_nro,))
    max_sec = cursor.fetchone()[0]
    conn.close()
    return max_sec if max_sec is not None else 0
