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
from kivy.uix.image import Image

import requests



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
    PageLayout:
        BoxLayout:
            orientation: "vertical"
            anchor_x: 'center'
            anchor_y: 'center'
            canvas:
                Color:
                    rgba: .80,.90,.80,1
                Rectangle:
                    size: self.size
                    pos: self.pos
            Camera:
                id: camera
                resolution: (640, 480)
                play: False
                size_hint: (1, 1)
            AnchorLayout:
                anchor_x: 'center'
                anchor_y: 'center'
                ToggleButton:
                    size_hint: [0.3, 0.2]
                    text: 'Play'
                    background_color: .70,.80,.70,1
                    on_press: root.play()
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center' 
            canvas:
                Color:
                    rgba: .90,.80,.80,1
                Rectangle:
                    size: self.size
                    pos: self.pos       
            BoxLayout:
                orientation: "vertical"
                size_hint: [0.4,0.4]
                padding: '3px','3px','3px','3px'
                
                Label:
                    text: "Add new file in db"
                    test_size: (200, None)
                    color: 0.3,0,0,.5
                    size_hint: (1, 1)
                Label:
                    text: "name"
                    color: 0,0,0.3,.5
                    size_hint: (1, 1)
                TextInput:
                    #size_hint_y: None
                    size_hint_x: 1
                    id: input_name
                Label:
                    text: "path"
                    color: 0,0,0.3,.5
                    size_hint: (1, 1)
                TextInput:
                    #size_hint_y: None
                    size_hint_x: 1
                    id: input_path
                Button:
                    background_color: 0,0,0.3,.5
                    text: 'Add'
                    on_press: root.add(input_path.text, input_name.text)

    AnchorLayout:
        
        anchor_x: 'center'
        anchor_y: 'top'
        canvas:
            Color:
                rgba: .80,.80,.90,1
            Rectangle:
                size: self.size
                pos: self.pos
        Button:
            background_color: 0,0,0.3,.5
            pos_hint: {'right': 1}
            size_hint: [1, 0.1]
            text: 'Reload'
            on_press: root.show_all()
        
        GridLayout:
            cols: 2
            id: gl
            orientation: 'vertical'
            #size_hint: [0.8,0.8]
       
        
            
            
''')


class TestCamera(App):

    def build(self):

        return CameraClick()
class CameraClick(PageLayout):
    def play(self):
        global f
        if f:
            event = Clock.schedule_interval(self.capture, 4)
            #event1 = Clock.schedule_once(self.capture, 2)
        f = False

        self.ids['camera'].play = not self.ids['camera'].play
    
    def tostrnahfromlist(self, s):
        global differences
        st = ''
        for i in s:
            if i  != ' ':
                st += i
            else:
                differences.append(float(st))
                st = ''
        print(differences)

    def capture(self, _):
        if self.ids['camera'].play:
            global differences
            camera = self.ids['camera']
            camera.export_to_png("IMG_now.jpg")
            print("Captured")

            url='http://127.0.0.1:5000/'
            values={'file' : 'file.jpg', 'OUT':'csv', 'what' : 'lol'}
            files={'file': open('IMG_now.jpg','rb')}
            r=requests.post(url,files=files, data = values)
            if r == "face_not_found":
                print("Face not found")
            else:
                self.tostrnahfromlist(r.text)

    def add(self, path, name):
        global n
        global data
        data.append(name)
        n += 1
        url='http://127.0.0.1:5000/'
        values={'file' : 'file.jpg', 'OUT':'csv', 'what' : 'add', 'name' : name}
        files={'file': open(path,'rb')}
        r=requests.post(url,files=files, data = values)
    def show_all(self):
        print(n)
        if n!= 0:
            if differences !=  []:
                self.ids['gl'].clear_widgets()
                for i in range(1, n+1):
                    self.ids['gl'].add_widget(Label(text = data[i], color = [0,0,0,1]))
                    #self.ids['gl'].add_widget(Image(source=os.path.join("bd", "IMG_{}.png".format(i))))
                    if differences[i-1]:
                        self.ids['gl'].add_widget(Label(text = str(differences[i-1]), color = [0,0,0,1]))
                        print(data[i])
                        if float(differences[i-1]) < 0.55:
                            print("It`s you")
                        print(i)
                    else:
                        self.ids['gl'].add_widget(Label(text = "Лицо на изображение не найдено", color = [0,0,0,1]))
            else:
                self.ids['gl'].add_widget(Label(text = "Сделайте фото ", color = [0,0,0,1]))
                print("Сделайте фото")
        else:
            self.ids['gl'].add_widget(Label(text = "Изображений в базе данных не найдено", color = [0,0,0,1]))
    def out(self):
        TestCamera.stop()




TestCamera().run()