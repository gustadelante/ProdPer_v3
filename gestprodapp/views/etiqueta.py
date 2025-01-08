import flet as ft
import flet_easy as fs
from controllers.producto import bobina
from controllers.imprimir import imprimir_y_guardar  # Import the new function
from datetime import datetime
from models.database import bobina_exists, get_max_sec

# Agregar pagina de etiquetas
""" @fs.page(route="/etiqueta", title="Emisión de Etiquetas", share_data=True) """
@fs.page(route="/etiqueta", title="Emisión de Etiquetas", share_data=True)
def etiqueta_page(data: fs.Datasy):
    page = data.page
    view = data.view
    
      
    if data.share.contains():
        x: str = data.share.get("turnoH")
        y: str = data.share.get("calidadH")
    else:
        res = ft.Text("No value passed on the page!.")
    

    page.bgcolor = ft.colors.BLUE_GREY_800
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_resizable = True        

     # Ajuste del tamaño de la ventana
    page.window_width = 900
    page.window_height = 800

    # Colores para modo claro y oscuro con verde oscuro predominante
    light_primary_color = ft.colors.GREEN
    dark_primary_color = ft.colors.GREEN_900
    light_background_color = ft.colors.WHITE
    dark_background_color = ft.colors.BLACK
    light_text_color = ft.colors.BLACK
    dark_text_color = ft.colors.WHITE

    #saco el mensaje de no completado de drpodowns
    # Limpiar el error de no completado
    def clear_error_text(e):
        if calidad.error_text:
           calidad.error_text = ""
           calidad.update() 
        if turno.error_text:
           turno.error_text = "" 
           turno.update()

    # Validar contenido de los text field
    def validate_float(e):
        if not e.control.value.replace(",", "", 1).isdigit() or len(e.control.value) > 5:
            e.control.error_text = "Número no válido o demasiado largo"
        else:
            e.control.error_text = ""
        page.update()

    def validate_int(e):
        if not e.control.value.isdigit() or len(e.control.value) > 5:
            e.control.error_text = "Número no válido o demasiado largo"
        else:
            e.control.error_text = ""
        page.update()

    def validate_single_digit(e):
        if not e.control.value.isdigit() or len(e.control.value) != 1:
            e.control.error_text = "Debe ser un solo dígito"
        else:
            e.control.error_text = ""
        page.update()


    def create_text_field(label, on_change, mode):
        fill_color = dark_background_color if mode == "dark" else ft.colors.GREY_200
        text_color = dark_text_color if mode == "dark" else light_text_color
        return ft.TextField(
            label=label, on_change=on_change,
            text_size=26, width=400,
            border_radius=10, filled=True, fill_color=fill_color,
            color=text_color,
            border_color=ft.Colors.RED_800, 
            border_width=10,
            hover_color=ft.colors.GREEN_100
        )
    
    def create_dropdown(label, options, mode):
        fill_color = dark_background_color if mode == "dark" else ft.colors.GREY_200
        text_color = dark_text_color if mode == "dark" else light_text_color        
        return ft.Dropdown(
            label=label, options=options,
            text_size=20, width=400,
            border_radius=10, filled=True, fill_color=fill_color,
            color=text_color,
            border_color=ft.Colors.RED_800, 
            border_width=10,
            on_change=clear_error_text
        )

    #Definir los campos del formulario
    ancho = create_text_field("ANCHO", validate_float, page.theme_mode)
    diametro = create_text_field("DIÁMETRO", validate_int, page.theme_mode)
    gramaje = create_text_field("GRAMAJE", validate_int, page.theme_mode)
    peso = create_text_field("PESO", validate_float, page.theme_mode)
    bobina_nro = create_text_field("Bobina Nro", validate_int, page.theme_mode)
    sec = create_text_field("Sec", validate_single_digit, page.theme_mode)
    orden_fab = create_text_field("Orden de Fabricación", validate_int, page.theme_mode)

    now = datetime.now()
    fecha_str = now.strftime("%Y-%m-%d %H:%M")

    fecha_container = create_text_field("Fecha y Hora", lambda e: None, page.theme_mode)
    fecha_container.value = fecha_str

    turno_options = [ft.dropdown.Option("A"), ft.dropdown.Option("B"), ft.dropdown.Option("C"), ft.dropdown.Option("D")]
    calidad_options = [ft.dropdown.Option("01-ONDA LINER"), ft.dropdown.Option("02-COVERING"), ft.dropdown.Option("03-L.BLANCO")
                       , ft.dropdown.Option("04-CART.GRIS"), ft.dropdown.Option("05-CART.BLANCA"), ft.dropdown.Option("06-LINER PER")
                       , ft.dropdown.Option("07-ONDA C"), ft.dropdown.Option("08-ONDA EFL")
    ]

    turno = create_dropdown("Turno", turno_options, page.theme_mode)
    calidad = create_dropdown("Calidad", calidad_options, page.theme_mode)

    #Asignar valores pasados desde otro formulario
    turno.value = data.share.get("turnoH")
    calidad.value = data.share.get("calidadH")

    #Asignar valores iniciales o incrementales.
    sec.value = 1    
    #Asignar valor incremental al campo sec (secuencia)


    def verificar_datos():
        campos = [ancho, diametro, gramaje, peso, bobina_nro, sec, orden_fab, turno, calidad]
        for campo in campos:
            if campo.value == "":
                return campo
            if campo.label == "Turno" and campo.value == None:
                return campo 
            if campo.label == "Calidad" and campo.value == None:
                return campo
        return None

    def cerrar_dialogo_y_enfocar(e, dialog, campo):
        dialog.open = False
        campo.focus()
        page.update()

    def set_sec_value(sec, bobina_nro):
        try:
            max_sec = get_max_sec(bobina_nro)
            nuevo_sec = max_sec + 1
            sec.value = str(nuevo_sec)
            print(f"nuevo sec: {sec.value}")
        except Exception as e:
            print("No pudo incrementar el valor de la secuencia:", e)
            sec.value = "1"
        sec.update()

    def handle_imprimir_y_guardar(nueva_bobina, sec):
        bobina_nro = imprimir_y_guardar(nueva_bobina)
        set_sec_value(sec, bobina_nro)

    def imprimir_datos(e):
        old_sec = sec.value
        campo_incompleto = verificar_datos()
        if campo_incompleto:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Debe completar todos los campos"),
                actions=[
                    ft.TextButton(
                        text="Aceptar",
                        on_click=lambda e: cerrar_dialogo_y_enfocar(e, dialog, campo_incompleto)
                    )
                ]
            )
            page.dialog = dialog
            dialog.open = True
        else:
            datos = {
                "ANCHO": ancho.value,
                "DIÁMETRO": diametro.value,
                "GRAMAJE": gramaje.value,
                "PESO": peso.value,
                "Bobina Nro": bobina_nro.value,
                "Sec": sec.value,
                "Orden de Fabricación": orden_fab.value,
                "Fecha y Hora": fecha_str,
                "Turno": turno.value,
                "Calidad": calidad.value
            }
            params = {
                ancho.value,
                diametro.value,
                gramaje.value,
                peso.value,
                bobina_nro.value,
                sec.value,
                orden_fab.value,
                fecha_str,
                turno.value,
                calidad.value
            }            
            print(datos)
            # Llamada a la función con los campos ingresados
            funcion_procesar_datos(datos)
            # llamada a metodo de producto.py
            nueva_bobina = bobina(ancho.value,
                diametro.value,
                gramaje.value,
                peso.value,
                bobina_nro.value,
                sec.value,
                orden_fab.value,
                fecha_str,
                turno.value,
                calidad.value)
            # Llamada a la función para imprimir y guardar
            handle_imprimir_y_guardar(nueva_bobina, sec)

        page.update()

    # Definición de la función para procesar los datos
    def funcion_procesar_datos(datos):
        # Implementación de lógica
        pass

    imprimir_button = ft.ElevatedButton(
        text="IMPRIMIR",
        on_click=imprimir_datos,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 20, 20, 20),
            text_style=ft.TextStyle(size=22, weight="bold"),
            #bgcolor=page.theme.primary_color, 
            bgcolor=ft.colors.BLUE_GREY_100,
            color=ft.colors.GREEN_900,
        )
    )

#, border_radius=10, border=ft.border.all(1,ft.Colors.RED_800), bgcolor=ft.Colors.RED_800

    responsive_grid = ft.GridView(
        expand=True,
        max_extent=450,
        padding=10,
        child_aspect_ratio=4,        
        controls=[            
            ft.Container(content=ancho, alignment=ft.alignment.center),
            ft.Container(content=diametro, alignment=ft.alignment.center),
            ft.Container(content=gramaje, alignment=ft.alignment.center),
            ft.Container(content=peso, alignment=ft.alignment.center),
            ft.Container(content=ft.Row(
                [
                    ft.Container(content=bobina_nro, alignment=ft.alignment.center, expand=7),
                    ft.Container(content=sec, alignment=ft.alignment.center, expand=3)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), 
            alignment=ft.alignment.center),
            ft.Container(content=orden_fab, alignment=ft.alignment.center),
            ft.Container(content=fecha_container, alignment=ft.alignment.center),
            ft.Container(content=turno, alignment=ft.alignment.center),
            ft.Container(content=calidad, alignment=ft.alignment.center),
            ft.Container(content=imprimir_button, alignment=ft.alignment.center)
        ],
    )

    titulo = ft.Row(
        controls=[
            ft.Text(
                value="IMPRESION DE ETIQUETAS",
                text_align=ft.TextAlign.CENTER,
                size=40,
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREEN_900
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    return ft.View(
            controls=[
                titulo,
                ft.Divider(height=9, thickness=3, color="green"),
                ft.Card(
                    ft.Container(
                        content=ft.Column([
                            responsive_grid
                        ]),
                        padding=20,
                        border_radius=10,
                        bgcolor=ft.colors.GREEN_300,
                        alignment=ft.alignment.center,
                    )

                ),
                                
            ]

    )
    """ controls=[
        titulo,
        ft.Divider(height=9, thickness=3, color="green"),
        ft.Card(                            
        ft.Container(
            content=ft.Column([
                responsive_grid
            ]),
            padding=20,
            border_radius=10,                
            bgcolor=ft.colors.GREEN_300,
            alignment=ft.alignment.center,
                                    
        ),        
    )],
    bgcolor=ft.colors.BLUE_GREY_100                    """


    

""" 
    return ft.View(
        controls=[
            ft.Text("Counter page", size=30),
            ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ],
                alignment="center",
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=view.appbar,
    ) """




"""     
    txt_number = ft.TextField(value=id, text_align="right", width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()
"""
