from models.database import bobina_exists, get_max_sec

def set_sec_value(sec, bobina_nro):
    try:
        if not bobina_exists({'bobina_nro': bobina_nro, 'sec': sec.value}):
            nuevo_sec = int(sec.value) + 1
            sec.value = str(nuevo_sec)
        else:
            max_sec = get_max_sec(bobina_nro)
            sec.value = str(max_sec + 1)
        
        print(f"nuevo sec: {sec.value}")
    except Exception as e:
        print("No pudo incrementar el valor de la secuencia:", e)
        sec.value = "1"
