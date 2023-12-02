import flet as ft
import pyperclip

is_expansion = True
def main(page: ft.Page):
    page.title = "ClipBroad"
    page.window_always_on_top = True
    page.window_opacity = 0.7
    page.window_width = 300
    page.window_height = 68
    page.window_title_bar_hidden = True
    page.window_left = 1500
    page.window_top = 150

    def expansion(e):
        global is_expansion
        if is_expansion:
            page.window_height = 500
            page.update()
            is_expansion = False
        else:
            page.window_height = 68
            page.update()
            is_expansion = True

    page.add(
        ft.Row(
            [
                ft.WindowDragArea(
                    ft.Container(ft.Text("CLIP-BROAD"),
                                 bgcolor=ft.colors.WHITE10, padding=3, on_click=expansion), expand=True),
                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close(),)
            ]
        )
    )


    def add_text(e):
        def copy_text(e):
            pyperclip.copy(text.text)

        text = ft.TextButton(text=f"{new_text.value}",on_click=copy_text)
        page.add(text)
        page.update()


    new_text = ft.TextField(hint_text="Copy in here",on_submit=add_text, multiline=True, shift_enter=True)

    page.add(new_text)


if __name__ == "__main__":
    ft.app(target=main)
