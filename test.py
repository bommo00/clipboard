import boto3
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
import json
global requ_time
import requests
import flet as ft
import pyperclip
import requests
from cryptography.fernet import Fernet


def main(page: ft.Page):
    page.title = "ClipBroad"

    page.window_opacity = 0.7
    page.window_width = 300
    page.window_height = 68
    page.window_left = 1500
    page.window_top = 150

    def copy_text(e):
        pyperclip.copy(e.control.text)

    new = ft.ElevatedButton(text="w", bgcolor='blue', on_click=copy_text,)
    page.add(new)

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
    # key = Fernet.generate_key()
    # f = Fernet(key)
    # token = f.encrypt(b"A really secret message. Not for prying eyes.")
    # print(token)
    # print(f.decrypt(token).decode('utf-8'))