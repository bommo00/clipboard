import flet as ft
import pyperclip
import requests
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
import json

url = 'BACKENDURL'
is_expansion = True



def main(page: ft.Page):
    def to_encode(text):
        msg = pad(text.encode('utf-8'), AES.block_size)
        en_msg = aes.encrypt(msg)
        en_text = base64.b64encode(en_msg).decode('utf-8')
        return en_text

    def to_decode(en_text):
        base64_de_text = base64.b64decode(en_text)  # Base64解码
        de_text = aes.decrypt(base64_de_text)
        text = unpad(de_text, AES.block_size).decode('utf-8')
        return text

    def verity_page():
        def submit(e):
            global aes
            key = os.urandom(32)
            aes = AES.new(key, AES.MODE_ECB)

            global username
            username = to_encode(email.value)
            user_pass = to_encode(password.value)
            data = {'email': username, 'password': user_pass}
            response = requests.post(url + '/' + func, data=data)
            if response == 401:
                page.add(ft.Text('Wrong password or Account.', color=ft.colors.RED_400))
            elif response == 500:
                page.add(ft.Text('You already have an account.', color=ft.colors.RED_400))
            elif response:
                page.add(ft.Text('Succeed.', color=ft.colors.BLUE))
                global access_token
                access_token = response.json()['access_token']
                content = {'words': access_token, 'for': username}
                data = json.dumps(content)
                with open(".info/ts.json", 'w') as file:
                    file.write(data)
                with open(".info/e.bin", 'wb') as file:
                    file.write(key)
                page.go('/')

        def routing_register(e):
            global func
            func = 'register'
            t.value = func
            page.update()

        def routing_login(e):
            global func
            func = 'login'
            t.value = func
            page.update()

        global func
        func = 'register'

        page.window_width = 300
        page.window_height = 500

        email = ft.TextField(keyboard_type=ft.KeyboardType.EMAIL, label="This would be your login ID",
                             hint_text="email")
        password = ft.TextField(label="Password", password=True, can_reveal_password=True)

        t = ft.Text(func)
        controls = ft.View('/verify', [
            ft.ElevatedButton('Sign in', on_click=routing_register),
            ft.ElevatedButton('Log in', on_click=routing_login),
            t,
            email,
            password,
            ft.ElevatedButton('Submit', on_click=submit),
        ])
        page.views.append(controls)

    def home_page():
        # Function of GUI elements performance
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
            en_text = to_encode(e.control.text)

            data = {'id': username, 'text': en_text}
            headers = {'Authorization': f'Bearer {access_token}'}
            requests.post(url + '/switch', data=data, headers=headers)

            if e.control.bgcolor == "blue":
                e.control.bgcolor = "white"
            else:
                e.control.bgcolor = "blue"
            e.control.update()

        def open_dlg():
            page.dialog = dlg
            dlg.open = True
            page.update()

        # Function for text manage with API
        def loading():
            global time
            time = datetime.now().isoformat()
            params = {'id': username, 'time': time}
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url + '/load', params=params, headers=headers)
            if response.status_code == 200:
                texts = response.json()
                if texts == {'status': 'success'}:
                    pass
                else:
                    if not isinstance(texts, list):
                        texts = [texts]
                    for t in texts:
                        text = to_decode(t['content'])
                        main_page.controls.insert(2,
                                    ft.ElevatedButton(text=text, bgcolor='blue', color='white', on_click=copy_text,
                                                      on_long_press=fixed)
                                    )
            else:
                open_dlg()

            page.update()

        def refresh(e):
            global time
            params = {'id': username, 'time': time}
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url + '/get', params=params, headers=headers)
            if response.status_code == 200:
                texts = response.json()
                if texts == {'status': 'success'}:
                    pass
                else:
                    if not isinstance(texts, list):
                        texts = [texts]
                    for t in texts:
                        text = to_decode(t['content'])
                        main_page.controls.insert(2,
                                    ft.ElevatedButton(text=text, bgcolor='white', on_click=copy_text,
                                                      on_long_press=fixed)
                                    )
            else:
                open_dlg()
            time = datetime.now().isoformat()
            page.update()

        def add_text(e):
            text = ft.ElevatedButton(text=new_text.value, bgcolor='white', on_click=copy_text, on_long_press=fixed)
            main_page.controls.insert(2, text)

            en_text = to_encode(new_text.value)
            global time
            time = datetime.now().isoformat()
            data = {'id': username, 'text': en_text, 'time': time}

            new_text.value = ''

            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post(url + '/update', data=data, headers=headers)
            if response.status_code == 200:
                texts = response.json()
                if texts == {'status': 'success'}:
                    pass
                else:
                    if not isinstance(texts, list):
                        texts = [texts]
                    for t in texts:
                        text = to_decode(t['content'])
                        main_page.controls.insert(2,
                                    ft.ElevatedButton(text=text, bgcolor='white', on_click=copy_text,
                                                      on_long_press=fixed)
                                    )
            else:
                open_dlg()
            page.update()


        page.window_always_on_top = True
        page.window_title_bar_hidden = True
        page.window_opacity = 0.7
        page.window_width = 300
        page.window_height = 68
        page.window_left = 1500
        page.window_top = 150


        dlg = ft.AlertDialog(title=ft.Text("Here is some problem;("))
        new_text = ft.TextField(hint_text="Copy in here", on_submit=add_text, multiline=True, shift_enter=True)
        main_page = ft.View('/', [
            ft.Row(
            [
                ft.WindowDragArea(
                    ft.Container(ft.Text("CLIP-BROAD"),
                                 bgcolor=ft.colors.WHITE10, padding=3, on_click=expansion), expand=True),
                ft.IconButton(ft.icons.REFRESH, on_click=refresh),
                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close(), ),

            ]),
            new_text])
        page.views.append(main_page)
        loading()
        page.update()

    def route_change(handler):
        route = ft.TemplateRoute(handler.route)
        if route.match("/verify"):
            verity_page()
        elif route.match("/"):
            page.views.clear()
            page.controls = []
            home_page()

    page.on_route_change = route_change
    page.title = "ClipBroad"
    if not os.path.exists(".info/ts.json") or not os.path.exists(".info/e.bin"):
        page.go('/verify')
    else:
        with open(".info/ts.json", 'r') as file:
            data = file.read()
        user_info = json.loads(data)

        global username
        global access_token
        access_token = user_info['words']
        username = user_info['for']

        with open(".info/e.bin", 'rb') as file:
            key = file.read()
        global aes
        aes = AES.new(key, AES.MODE_ECB)
        page.go('/')


if __name__ == "__main__":
    try:
        ft.app(target=main)
    finally:
        params = {'id': username}
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url + '/end', params=params, headers=headers)
