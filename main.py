n = 0
data = []
differences = []
with open("db\\number.txt", "r") as f:
    for line in f:
        data.append(line)
n = int(data[0])
print(n)
print(data)
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
from  kivy.uix.togglebutton import ToggleButton
import time
import subprocess
from kivy.uix.screenmanager import ScreenManager, Screen
from nnc import *


Builder.load_string('''
<CameraClick>:
    BoxLayout:
        id: lol
        orintation: 'horizontal'
        Camera:
            id: camera
            resolution: (640, 480)
            play: False
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
                on_press: root.add()
    GridLayout:
        id: gl
        cols: 1

''')


class TestCamera(App):

    def build(self):

        return CameraClick()
class CameraClick(PageLayout):
    def play(self):
        event = Clock.schedule_interval(self.capture, 20)
        if self.ids['camera'].play:
            event.cancel()
        self.ids['camera'].play = not  self.ids['camera'].play

    def capture(self, _):
        global n
        global differences

        camera = self.ids['camera']
        camera.export_to_png("IMG_now.jpg")

        for i in range(0, n):
            differences.append(what_difference(i))
            if differences[i] == -1:
                print("Face not found")
        print("Captured")

    def add(self):
        global n
        n+=1
        PATH = "D:\Small"
        add_new(n,PATH)
    def show_all(self):
        print(n)
        if n!= 0:
            #self.ids['gl'].rows = 3
            self.ids['gl'].clear_widgets()
            for i in range(1, n):
                self.ids['gl'].add_widget(Label(text = data[i]))
                self.ids['gl'].add_widget(Label(text = str(differences[i-1])))
                #self.ids["label_{}".format(i)].text = data[i]
                print(data[i])
                print(i)
        else:
            print("Изображений не найдено")
    def out(self):
        TestCamera.stop()




TestCamera().run()