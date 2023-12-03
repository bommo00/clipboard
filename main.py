import flet as ft
import pyperclip
import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth(settings_file="setting.yaml")
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

is_expansion = True
FOLDER_ID = os.getenv('FOLDER_ID')
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

    def refresh(e):

        def copy_text(e):
            pyperclip.copy(new.text)

        query = f"'{FOLDER_ID}' in parents and title = 'temp.txt' and trashed=false"
        file_list = drive.ListFile({'q': query}).GetList()

        if file_list:
            file1 = drive.CreateFile({'id': file_list[0]['id']})
            file1.GetContentFile('temp-online.txt')
            with open('temp.txt', 'r') as f:
                texts = f.read().split('|||：：：')
            with open('temp-online.txt', 'r') as f:
                texts_online = f.read().split(',')
            file1.GetContentFile('temp.txt')
            os.remove('temp-online.txt')
            new_online = list(set(texts_online) - set(texts))
            for n in new_online:
                new = ft.TextButton(text=n,on_click=copy_text)
                page.controls.insert(2, new)
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
        query = f"'{FOLDER_ID}' in parents and title = 'temp.txt' and trashed=false"
        file_list = drive.ListFile({'q': query}).GetList()
        if file_list:
            file1 = drive.CreateFile({'id': file_list[0]['id']})
            file1.GetContentFile('temp.txt')
            with open('temp.txt','a') as f:
                f.write(f'|||：：：{new_text.value}')
            file1.SetContentFile('temp.txt')
            file1.Upload()  # Files.insert()
        else:
            file1 = drive.CreateFile({'title': 'temp.txt',
                                      'parents': [{'id': f'{FOLDER_ID}'}]})
            with open('temp.txt','w') as f:
                f.write(f'{new_text.value}')
            file1.SetContentFile('temp.txt')
            file1.Upload()  # Files.insert()
        def copy_text(e):
            pyperclip.copy(text.text)

        text = ft.TextButton(text=f"{new_text.value}",on_click=copy_text)

        page.controls.insert(2, text)
        page.update()


    new_text = ft.TextField(hint_text="Copy in here",on_submit=add_text, multiline=True, shift_enter=True)

    page.add(new_text)


if __name__ == "__main__":
    try:
        ft.app(target=main)
    finally:
        query = f"'{FOLDER_ID}' in parents and title = 'temp.txt' and trashed=false"
        file_list = drive.ListFile({'q': query}).GetList()
        if file_list:
            file_to_delete = drive.CreateFile({'id': file_list[0]['id']})
            file_to_delete.Delete()
            os.remove('temp.txt')

