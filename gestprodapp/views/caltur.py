import flet as ft
import flet_easy as fs

""" caltur = fs.AddPagesy(
    route_prefix="/caltur",
)
 """

# We add a second page
@fs.page(route="/caltur", title="Acceso", share_data=True)
def caltur_page(data: fs.Datasy):
    page = data.page
    view = data.view
    page.theme_mode = "light"

    txt_number = ft.TextField(value=id, text_align="right", width=100)

     # TextField para ingreso de datos
    text1 = ft.TextField(label="Texto 1", width=300)
    text2 = ft.TextField(label="Texto 2", width=300)
    error_message = ft.Text(value="", color="red")

    # Limpiar el error de no completado
    def clear_error_text(e):
        if calidad_dropdown.error_text:
           calidad_dropdown.error_text = ""
           calidad_dropdown.update() 
        if turno_dropdown.error_text:
           turno_dropdown.error_text = "" 
           turno_dropdown.update()
    

     # Configuración de los dropdown
    calidad_options = [
        "01-ONDA LINER", "02-COVERING", "03-L.BLANCO", "04-CART.GRIS",
        "05-CART.BLANCA", "06-LINER PER", "07-ONDA C", "08-ONDA EFL"
    ]
    turno_options = ["A", "B", "C", "D"]

    calidad_dropdown = ft.Dropdown(
        label="Calidad", options=[ft.dropdown.Option(key=opt, text=opt) for opt in calidad_options],
        on_change=clear_error_text
    )

    turno_dropdown = ft.Dropdown(
        label="Turno", options=[ft.dropdown.Option(key=opt, text=opt) for opt in turno_options],
        on_change=clear_error_text
    )

    def validate_and_proceed(e):
        is_valid = True
        if not calidad_dropdown.value:
            calidad_dropdown.error_text = "Por favor, seleccione una calidad."
            calidad_dropdown.update()
            is_valid = False
        if not turno_dropdown.value:
            turno_dropdown.error_text = "Por favor, seleccione un turno."
            turno_dropdown.update()
            is_valid = False
        if is_valid:
            #page.go(f"/etiqueta?calidad={calidad_dropdown.value}&turno={turno_dropdown.value}")
            # Guardar valores en client_storage
            ###page.client_storage.set("text1", calidad_dropdown.value)
            ###page.client_storage.set("text2", turno_dropdown.value)
            ####ft.FilledButton("Etiquetas", on_click=data.go("/counter")),
            try:
                #ft.FilledButton("Ingresar", on_click=data.go("/caltur/etiqueta/")),
                
                #ft.FilledButton("Ingresar", on_click=lambda _: page.go("/etiqueta")),                
                
                data.share.set("turnoH", turno_dropdown.value)
                data.share.set("calidadH", calidad_dropdown.value)                
                page.go("/etiqueta"),


            except:
                print ("sale por error", error_message)
            

            
            #ft.Page.go(f"/etiqueta?calidad={calidad_dropdown.value}&turno={turno_dropdown.value}")
            #etiqueta.show_etiqueta(page, calidad_dropdown.value, turno_dropdown.value)
            #ft.Page.go("/etiqueta")

    ingresar_button = ft.ElevatedButton(
        text="Ingresar", on_click=validate_and_proceed, width=150
    )

   



    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()


    return ft.View(
        controls=[
            ft.Text("Seleccione Calidad y Turno", size=30),
            ft.Row(),
            ft.Row(
                [                    
                    #ft.Text("Bienvenido", size=24, weight=ft.FontWeight.BOLD),                    
                    calidad_dropdown,
                    turno_dropdown,
                    ingresar_button,
                    error_message

                ],
                alignment="center",
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=view.appbar,
    )


""" 
    return ft.View(
        controls=[
            ft.Text("Acceso Etiquetas", size=30),
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
    )
 """