import flet as ft
import openpyxl
import flet_easy as fs
import os
from models.database import init_db, insert_bobina, update_bobina, bobina_exists, get_max_sec

def imprimir_y_guardar(nueva_bobina):
    init_db()
    
    #Compartir nueva_bobina segun fs no como parametro.

    # Crear una página para la impresión
    #page = data.page
    #page.window_width = 900
    #page.window_height = 800

    # Crear un contenedor con los valores de nueva_bobina
    """ contenido = ft.Column(
        controls=[
            ft.Text(f"ANCHO: {nueva_bobina.ancho}", size=40),
            ft.Text(f"DIÁMETRO: {nueva_bobina.diametro}", size=40),
            ft.Text(f"GRAMAJE: {nueva_bobina.gramaje}", size=40),
            ft.Text(f"PESO: {nueva_bobina.peso}", size=40),
            ft.Text(f"Bobina Nro: {nueva_bobina.bobina_nro}", size=40),
            ft.Text(f"Sec: {nueva_bobina.sec}", size=40),
            ft.Text(f"Orden de Fabricación: {nueva_bobina.orden_fab}", size=40),
            ft.Text(f"Fecha y Hora: {nueva_bobina.fecha_str}", size=40),
            ft.Text(f"Turno: {nueva_bobina.turno}", size=40),
            ft.Text(f"Calidad: {nueva_bobina.calidad}", size=40)
        ]
    )

    # Agregar el contenedor a la página y mostrarla
    page.add(contenido)
    page.show() """

    # Enviar los datos a la impresora
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    c = canvas.Canvas("print_output.pdf", pagesize=A4)
    width, height = A4

    # Definir las coordenadas y el tamaño de la letra
    y = height - 40  # Coordenada Y inicial
    line_height = 50  # Altura de cada línea
    x_left = 100  # Coordenada X para la primera columna
    x_right = 300 + 28.35  # Coordenada X para la segunda columna (1 cm = 28.35 points)

    c.setFont("Helvetica", 40)
    c.drawString(x_left, y, f"{nueva_bobina.ancho}")
    c.drawString(x_right, y, f"{nueva_bobina.diametro}")
    y -= line_height
    c.drawString(x_left, y, f"{nueva_bobina.gramaje}")
    c.drawString(x_right, y, f"{nueva_bobina.peso}")
    y -= line_height
    c.drawString(x_left, y, f"{nueva_bobina.bobina_nro}{nueva_bobina.sec}")
    c.drawString(x_right, y, f"{nueva_bobina.orden_fab}")
    y -= line_height
    c.setFont("Helvetica", 26)
    c.drawString(x_left, y, f"{nueva_bobina.fecha}")
    c.setFont("Helvetica", 40)
    c.drawString(x_right, y, f"{nueva_bobina.turno}")
    y -= line_height
    c.drawString(x_left, y, f"{nueva_bobina.calidad[3:]}")

    c.showPage()
    c.save()

    # Enviar el archivo PDF directamente a la impresora en Windows
    os.system(f'start /min "" "print_output.pdf" /p')

    # Guardar los valores en un archivo Excel
    file_path = "nueva_bobina.xlsx"
    if os.path.exists(file_path):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        # Agregar encabezados si es un nuevo archivo
        sheet.append([
            "Ancho", "Diámetro", "Gramaje", "Peso", "Bobina Nro", "Sec", 
            "Orden de Fabricación", "Fecha", "Turno", "CodCal", "DescCal"
        ])

    sheet.append([
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
        nueva_bobina.calidad[3:],  # solo desc de cal
    ])
    workbook.save(file_path)

    # Check if bobina exists in the database and insert or update accordingly
    if bobina_exists(nueva_bobina):
        update_bobina(nueva_bobina)
    else:
        insert_bobina(nueva_bobina)

    # Return bobina_nro for further processing
    return nueva_bobina.bobina_nro
