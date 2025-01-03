import flet as ft
import flet_easy as fs

index = fs.AddPagesy()


# We add a page
@index.page(route="/home", title="Home")
def index_page(data: fs.Datasy):
    view = data.view

    return ft.View(
        controls=[
            ft.Text("Home page", size=30),
            ft.FilledButton("Go to Counter", on_click=data.go("/counter/test/0")),
            ft.FilledButton("Etiquetas", on_click=data.go("/etiqueta")),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.appbar,
    )
