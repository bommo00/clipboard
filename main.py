import flet as ft
import pyperclip
import requests
import os

url = 'MY URL'
username = 'what'
is_expansion = True



def main(page: ft.Page):
    page.title = "ClipBroad"
    page.window_always_on_top = True
    page.window_title_bar_hidden = True
    page.window_opacity = 0.7
    page.window_width = 300
    page.window_height = 68
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
        load_in(e)

    def load_in(e):
        def copy_text(e):
            pyperclip.copy(new.text)

        def fixed(e):
            data = {'id': username, 'text': new.text}
            requests.post(url + '/switch', data=data)
            if e.control.bgcolor == "blue":
                e.control.bgcolor = "white"
            else:
                e.control.bgcolor = "blue"
            e.control.update()

        params = {'id': username}
        response = requests.get(url+'/get', params=params)
        texts = response.json()
        if texts:
            for t in texts:
                new = ft.ElevatedButton(text=f"{t['content']}", bgcolor='blue', on_click=copy_text, on_long_press=fixed)
                page.add(new)
        page.update()
    def refresh(e):

        def copy_text(e):
            pyperclip.copy(new.text)

        def fixed(e):
            data = {'id': username, 'text': new.text}
            requests.post(url + '/switch', data=data)
            if e.control.bgcolor == "blue":
                e.control.bgcolor = "white"
            else:
                e.control.bgcolor = "blue"
            e.control.update()

        params = {'id': username}
        response = requests.get(url+'/get', params=params)
        texts = response.json()
        if texts:
            for t in texts:
                new = ft.ElevatedButton(text=f"{t['content']}", bgcolor='white', on_click=copy_text, on_long_press=fixed)
                page.add(new)
        page.update()


    page.add(
        ft.Row(
            [
                ft.WindowDragArea(
                    ft.Container(ft.Text("CLIP-BROAD"),
                                 bgcolor=ft.colors.WHITE10, padding=3, on_click=expansion), expand=True),
                ft.IconButton(ft.icons.REFRESH, on_click=refresh),
                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close(),),

            ]
        )
    )


    def add_text(e):
        def copy_text(e):
            pyperclip.copy(text.text)

        def fixed(e):
            data = {'id': username, 'text': text.text}
            requests.post(url + '/switch', data=data)
            if e.control.bgcolor == "blue":
                e.control.bgcolor = "white"
            else:
                e.control.bgcolor = "blue"
            e.control.update()


        text = ft.ElevatedButton(text=f"{new_text.value}", bgcolor='white', on_click=copy_text, on_long_press=fixed)
        page.controls.insert(2, text)

        data = {'id': username, 'text': new_text.value}
        response = requests.post(url+'/update', data=data)
        texts = response.json()
        if texts:
            for t in texts:
                page.add(
                    ft.ElevatedButton(text=f"{t['content']}", bgcolor='white', on_click=copy_text, on_long_press=fixed)
                )
        page.update()

    # def login_view(page: ft.Page, route: str):
    #     page.add(ElevatedButton("Go to Page 2", on_click=goto_page2))
    #
    # def content_view(page: ft.Page, route: str):
    #     page.add(ElevatedButton("Go to Page 2", on_click=goto_page2))
    #
    # page.add_route("/login", login_view)
    # page.add_route("/page1", content_view)

    new_text = ft.TextField(hint_text="Copy in here",on_submit=add_text, multiline=True, shift_enter=True)
    page.add(new_text)


if __name__ == "__main__":
    try:
        ft.app(target=main)
    finally:
        params = {'id': username}
        response = requests.get(url + '/end', params=params)


