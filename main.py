import requests
import os
from datetime import date

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QTextBrowser


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("osu! player stats")

        layout_main = QVBoxLayout()

        self.textW = QLineEdit()
        self.textW.setMaxLength(50)
        self.textW.setPlaceholderText("Введите id пользователя")

        layout_main.addWidget(self.textW)

        layout_sub = QGridLayout()

        self.status_text = QLabel()
        self.token = get_token()
        if self.token:
            self.set_label_text("green", "Токен приложения получен!")
        else:
            self.set_label_text("red", "Ошибка авторизации!")
        layout_sub.addWidget(self.status_text, 0, 0, 1, 2)

        button = QPushButton("Найти", self)
        button.clicked.connect(self.button_click)
        layout_sub.addWidget(button, 0, 2)

        layout_main.addLayout(layout_sub)

        self.text_box = QTextBrowser()
        self.text_box.setOpenExternalLinks(True)

        layout_main.addWidget(self.text_box)

        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)

    def set_label_text(self, color, text):
        text = f"<span style=\"color: {color}\">{text}</span>"
        self.status_text.setText(text)


    def button_click(self):
        word = self.textW.text()

        payload = {"key": word}
        header = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"https://osu.ppy.sh/api/v2/users/{word}", params=payload, headers=header)
        if r.status_code == 200:
            try:
                result = format_json(r.json())
            except:
                self.set_label_text("red", "Ошибка")
                result = ""
            finally:
                self.text_box.setText(result)
        else:
            self.set_label_text("red", "Пользователя не существует!")


def get_token():
    try:
        secret = os.environ['CLIENT_SECRET']
    except KeyError:
        print("No key found!")
        return None
    data = {"client_id": "18739", "client_secret": secret, "grant_type": "client_credentials", "scope": "public"}
    r = requests.post("https://osu.ppy.sh/oauth/token", data=data)
    if r.status_code == 200:
        return r.json()["access_token"]
    return None

def format_json(json):
    text = f"<p><b><a href=\"https://osu.ppy.sh/users/{json['id']}\">{json['username']}</a></b></p>" \
           f"<p><b>Страна:</b> {json['country']['name']} </p>" \
           f"<p><b>Стандартный режим:</b> {json['playmode']} </p>" \
           f"<p><b>Время регистрации:</b> {date.fromisoformat(json['join_date'][:10])} </p>" \
           f"<p><b>pp:</b> {json['statistics']['pp']} </p>" \
           f"<p><b>Количество игр:</b> {json['statistics']['play_count']} </p>"
    return text

app = QApplication()

window = MainWindow()
window.show()

app.exec()