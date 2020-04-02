n = 0
f = open('db\\number.txt', 'r')
n = int(f.read())
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from  kivy.uix.togglebutton import ToggleButton
import time
from kivy.uix.screenmanager import ScreenManager, Screen
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
                on_press: camera.play = not camera.play
                size_hint_y: None
                height: '48px'
            Button:
                text: 'Capture'
                size_hint_y: None
                height: '48px'
                on_press: root.capture()
            Button:
                size_hint_y: None
                height: '48px'
                text: 'All image'
                on_press: root.show_all()
            Button:
                text: 'Out'
                size_hint_y: None
                on_press: root.out()
    GridLayout:
        id: gl
        cols: 3

''')


class TestCamera(App):

    def build(self):

        return CameraClick()
class CameraClick(PageLayout):
    def capture(self):
        global n
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        camera.export_to_png("db\IMG_{}.jpeg".format(n))
        n+=1
        f = open('db\\number.txt', 'w')
        f.write(str(n))
        print("Captured")
    def show_all(self):
        
        if n!= 0:
            #self.ids['gl'].rows = 3
            for i in range(n):
                self.ids['gl'].add_widget(Image(source="db\IMG_{}.jpeg".format(i)))
                print(i)
        else:
            print("Изображений не найдено")
    def out(self):
        TestCamera.stop()




TestCamera().run()