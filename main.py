import flet as ft
import pyperclip
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

url = 'url'
username = 'what'
is_expansion = True
key = b'3333333333333'
aes = AES.new(key,AES.MODE_ECB)



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


    def copy_text(e):
        pyperclip.copy(e.control.text)

    def fixed(e):
        msg = pad(new_text.value.encode('utf-8'), AES.block_size)
        en_text = aes.encrypt(msg)
        base64_en_text = base64.b64encode(en_text).decode('utf-8')
        data = {'id': username, 'text': base64_en_text}
        requests.post(url + '/switch', data=data)
        if e.control.bgcolor == "blue":
            e.control.bgcolor = "white"
        else:
            e.control.bgcolor = "blue"
        e.control.update()

    def loading():
        params = {'id': username}
        response = requests.get(url+'/get', params=params)
        texts = response.json()
        if texts:
            for t in texts:
                base64_de_text = base64.b64decode(t['content'])  # Base64解码
                de_text = aes.decrypt(base64_de_text)
                msg = unpad(de_text, AES.block_size).decode('utf-8')
                page.insert(2,
                    ft.ElevatedButton(text=msg, bgcolor='blue', color='white',on_click=copy_text, on_long_press=fixed)
                )
        page.update()
    def refresh(e):
        params = {'id': username}
        response = requests.get(url+'/get', params=params)
        texts = response.json()
        if texts:
            for t in texts:
                base64_de_text = base64.b64decode(t['content'])  # Base64解码
                de_text = aes.decrypt(base64_de_text)
                msg = unpad(de_text, AES.block_size).decode('utf-8')
                page.insert(2,
                    ft.ElevatedButton(text=msg, bgcolor='white', on_click=copy_text, on_long_press=fixed)
                )
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
        text = ft.ElevatedButton(text=new_text.value, bgcolor='white', on_click=copy_text, on_long_press=fixed)
        page.controls.insert(2, text)

        msg = pad(new_text.value.encode('utf-8'), AES.block_size)
        en_text = aes.encrypt(msg)
        base64_en_text = base64.b64encode(en_text).decode('utf-8')
        data = {'id': username, 'text': base64_en_text}
        response = requests.post(url+'/update', data=data)
        texts = response.json()
        if texts:
            for t in texts:
                base64_de_text = base64.b64decode(t['content'])  # Base64解码
                de_text = aes.decrypt(base64_de_text)
                msg = unpad(de_text, AES.block_size).decode('utf-8')
                page.insert(2,
                    ft.ElevatedButton(text=msg, bgcolor='white', on_click=copy_text, on_long_press=fixed)
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
    loading()


if __name__ == "__main__":
    try:
        ft.app(target=main)
    finally:
        params = {'id': username}
        response = requests.get(url + '/end', params=params)


