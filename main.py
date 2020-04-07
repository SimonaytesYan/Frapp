import os
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
import time
import subprocess
from kivy.uix.screenmanager import ScreenManager, Screen
from nnc import *
import socket




f = True
n = 0
data = []
differences = []
with open(os.path.join("db", "number.txt"), "r") as f:
    for line in f:
        data.append(line)
n = int(data[0])
print(n)
print(data)


Builder.load_string('''
<CameraClick>:
    BoxLayout:
        id: lol
        orintation: 'vertical'
        Camera:
            id: camera
            resolution: (640, 480)
            play: False
            size_hint: (1, .5)
        BoxLayout:
            orintation: 'vertical'
            ToggleButton:
                text: 'Play'
                on_press: root.play()
                size_hint_y: None
                height: '48px'
            Button:
                size_hint_y: None
                height: '48px'
                text: 'All image'
                on_press: root.show_all()
            Button:
                size_hint_y: None
                height: '48px'
                text: 'Add new'
                on_press: root.add(input_path.text, input_name.text)
            BoxLayout:
                orintation: 'vertical'
                Label:
                    text: "name"
                    size_hint: (1, .5)
                TextInput:
                    size_hint_y: None
                    size_hint_x: 1
                    id: input_name
                Label:
                    text: "path"
                    size_hint: (1, .5)
                TextInput:
                    size_hint_y: None
                    size_hint_x: 1
                    id: input_path
    GridLayout:
        id: gl
        cols: 1

''')


class TestCamera(App):

    def build(self):

        return CameraClick()
class CameraClick(PageLayout):
    def play(self):
        global f
        if f:
            event = Clock.schedule_interval(self.capture, 3)
        f = False

        self.ids['camera'].play = not self.ids['camera'].play
        
    def capture(self, _):
        if self.ids['camera'].play:
            global differences
            camera = self.ids['camera']
            camera.export_to_png("IMG_now.jpg")
            s = socket.socket() 

            s.connect(('localhost', 9090))  
            op = open("IMG_now.jpg", 'rb')  
            data = op.read(1024)
            s.send(data) 
            op.close()  
            s.shutdown(socket.SHUT_WR)

            #differences = what_difference(n)

            print("Captured")
        
            

    def add(self, path, name):
        global n
        n += 1
        data.append(str(name)+"\n")
        data[0]  = str(n) + "\n"
        f = open(os.path.join("db", "number.txt"), "w")
        for i in data:
            f.write(i)
        update_db(n, path)
    def show_all(self):
        print(n)
        if n!= 0:
            if differences !=  []:
                self.ids['gl'].clear_widgets()
                for i in range(1, n+1):
                    self.ids['gl'].add_widget(Label(text = data[i]))
                    if differences[i-1]:
                        self.ids['gl'].add_widget(Label(text = str(differences[i-1])))
                        print(data[i])
                        if differences[i-1] < 0.55:
                            print("It`s you")
                        print(i)
                    else:
                        print("Лицо на изображении не найдено")
            else:
                print("Сделайте фото")
        else:
            print("Изображений не найдено")
    def out(self):
        TestCamera.stop()




TestCamera().run()