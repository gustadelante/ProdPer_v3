import flet as ft
import flet_easy as fs

@fs.page(route="/caltur", title="Acceso", share_data=True)
def caltur_page(data: fs.Datasy):
    page = data.page
    view = data.view
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_resizable = False
    page.window.center()

    # Ajuste del tamaño de la ventana
    page.window_width = 400
    page.window_height = 300

    # TextField para ingreso de datos
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
        on_change=clear_error_text, text_size=14
    )

    turno_dropdown = ft.Dropdown(
        label="Turno", options=[ft.dropdown.Option(key=opt, text=opt) for opt in turno_options],
        on_change=clear_error_text, text_size=14
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
            try:
                data.share.set("turnoH", turno_dropdown.value)
                data.share.set("calidadH", calidad_dropdown.value)                
                page.go("/etiqueta")
            except:
                print("Error al proceder", error_message)

    ingresar_button = ft.ElevatedButton(
        text="Ingresar", on_click=validate_and_proceed, width=300
    )

    return ft.View(
        controls=[
            #ft.Text("Seleccione Calidad y Turno", size=30, weight=ft.FontWeight.BOLD),
            ft.Column(
                [
                    ft.Row(
                        [                            
                            calidad_dropdown
                        ],
                        alignment="center",
                    ),
                    ft.Row(
                        [                            
                            turno_dropdown
                        ],
                        alignment="center",
                    ),
                    ft.Row(
                        [                            
                            ingresar_button
                        ],
                        alignment="center",
                    ),                    
                    error_message
                ],
                alignment="center",
                spacing=10
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=view.appbar,
        bgcolor=ft.colors.GREEN_300
    )