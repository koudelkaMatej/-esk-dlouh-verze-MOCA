# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup

from functools import partial

from datetime import datetime

from person import Person
from utils import microgrid

from tests import ConnectTest
from tests import CubeTest
from tests import ClockTest
from tests import AnimalTestLion, AnimalTestRhino, AnimalTestCamel
from tests import RememberTest
from tests import AbstractionTest
from tests import SpeachRepeatTest
from tests import KTest
from tests import AdvancedRememberTest 
from tests import OrientationTest
from tests import LettersTest
from tests import NumberTest
from tests import SevenTest
from tests import DokoncitTest

import os

class Screen(Carousel):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.scroll_timeout = 0
        self.loop = True
        self.subject = None
        self.time_start = datetime.now().strftime("%H:%M") 
        self.direction = "right"
        self.tests = { 1 : ("Pamět", [RememberTest(self)]),
		       2 : ("Prostorová orientace / zručnost", [ConnectTest(self),
                                                                ClockTest(self)]),
                      3 : ("Pozornost", [NumberTest(self),
                                         SevenTest(self)]),
                      4 : ("Řeč", [SpeachRepeatTest(self),
                                   KTest(self)]),
                      5 : ("Abstrakce", [AbstractionTest(self)]),
                      6 : ("Pozdější vybavení slov", [AdvancedRememberTest(self)]),
                      7 : ("Dokončeno", [DokoncitTest(self)])}
        try:
            self.welcome_screen()

            if not os.path.exists("/sdcard/vysledky"):
                os.makedirs("/sdcard/vysledky")
        except Exception as ex:
            Popup(title='Test popup',
                  content=Label(text=str(ex)))

    def setup_tests(self):
        for key in sorted(self.tests):
            for test in self.tests[key][1]:
                test.draw_uix()
                self.add_widget(test)

        self.tests[1][1][0].popup_instruction.open()
    
    def desetup_tests(self):
        for desc, test_list in self.tests.values():
            for test in test_list: self.remove_widget(test)
    
    def result_screen(self, *args):
        self.desetup_tests()
        screen = GridLayout(cols=1)
        save_button = Button(text="Export")
        save_button.bind(on_press=lambda x: self.subject.save_results(self.tests))
        with screen.canvas.before:
            Color(.2,.2,.2)
            Rectangle(size=Window.size)
        
        for desc, test_list in self.tests.values():
            screen.add_widget(Label(text=desc))
            
            if len(test_list) > 1:
                points = [t.export_layout() for t in test_list] + [ 
                          Label(text=str(sum([t.points for t in test_list])))]

            else:
                points = [test_list[0].export_layout()]

            screen.add_widget(microgrid(False, *points)) 

        screen.add_widget(save_button)
                
        self.add_widget(screen) 

    def welcome_screen(self):
        screen = GridLayout(cols=1, size_hint=(.60, .6), pos_hint={"x":.2, "y":.3}, row_default_height=90, row_force_default=True)
        with screen.canvas.before:
            Color(.2,.2,.2)
            Rectangle(size=Window.size)
        name = TextInput(multiline=False, size_hint=(.3, .1), hint_text=u"Jméno",  font_size=60 )
        mez = Label(text=u"",  font_size=10,  height = 10)
        age = TextInput(multiline=False, size_hint=(.1, .1), hint_text=u"Věk",  font_size=60 )
        mez1 = Label(text=u"",  font_size=10,  height = 10)
        edu = TextInput(multiline=False, size_hint=(.15, .1), hint_text=u"Vzdělání",  font_size=60 )
        mez2 = Label(text=u"",  font_size=10,  height = 10)
        study = TextInput(multiline=False,text='KV', hint_text="Studie")
        mez3 = Label(text=u"",  font_size=10,  height = 10)
        start_button = Button(text="Start", size_hint=(.25,.3),  font_size=60 )
        sex_m = CheckBox(text=u"Muž", group="sex")
        sex_f = CheckBox(label=u"Žena", group="sex")
        lab_sex_m = Label(text=u"Muž",  font_size=60 )
        lab_sex_f = Label(text=u"Žena",  font_size=60 )
        sex = microgrid(False, lab_sex_m, sex_m, lab_sex_f, sex_f)
        
        screen.add_widget(name)
        screen.add_widget(mez)
        screen.add_widget(edu)
        screen.add_widget(mez1)
        screen.add_widget(age)
        screen.add_widget(mez2)
        screen.add_widget(sex)
        screen.add_widget(mez3)
        screen.add_widget(start_button)
        
        def start_btn(self, button):
            try:
                if not os.path.exists("/sdcard/vysledky/{0}".format(study.text)):
                    os.makedirs("/sdcard/vysledky/{0}".format(study.text))

                self.subject = Person(name=name.text, age=age.text,
                                      edu=edu.text, sex = "m" if sex_m.active else "f",
                                      study=study.text)
                self.remove_widget(screen)
                self.setup_tests()
            except:
                pass 
        
        start_button.bind(on_press=partial(start_btn, self))
        self.add_widget(screen)
        


class Program(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        
        return Screen() 

    def on_pause(self):
        return True

    def on_resume(self):
        return True

if __name__ == '__main__':
    Program().run()
                    
