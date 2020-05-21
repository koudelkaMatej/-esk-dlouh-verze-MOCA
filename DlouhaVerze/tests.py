# -*- coding: utf-8 -*-
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemLabel

from kivy.adapters.listadapter import ListAdapter

from kivy.graphics import Color
from kivy.graphics import Rectangle

from kivy.clock import Clock

from kivy.core.window import Window
from kivy.core.audio import SoundLoader

from functools import partial

import datetime
import utils
import time
import threading

class Test(FloatLayout):
	""" Base class for all tests """

	def __init__(self, screen,  **kwargs):
		super(Test, self).__init__(**kwargs)
		self.points = 0
		self.instruction = ""
		self.instruction_audio = "sounds/test.mp3"
		self.screen = screen 
		self.popup_instruction = utils.PopupHint(self.instruction)
		self.hidden_options = utils.Hidden(self)       
		self.help_button = Button(text="?", pos_hint={"x":.9, "y":.9}, size_hint=(.1,.1))
		self.hidden_button = Button(text="Možnosti", pos_hint={"x":0, "y":.9}, size_hint=(.1,.1), opacity=1)
		self.desc = None
		self.help_button.bind(on_press=partial(self.draw_hint, self))
		self.hidden_button.bind(on_press=partial(self.draw_hidden, self))		

	def draw_uix(self):
		self.popup_instruction = utils.PopupHint(self.instruction)
		self.hidden_options = utils.Hidden(self)
		self.inst_audio_button = utils.AudioButton(self.instruction_audio, pos_hint={"x":.8, "y":.92})

		self.add_widget(self.inst_audio_button)
		self.add_widget(self.help_button)
		self.add_widget(self.hidden_button)
		

	def draw_hint(self, inst, btn):
		self.popup_instruction.open()

	def draw_hidden(self, inst, btn):
		self.hidden_options.open()

	def result(self):
		return self.points

	def export_layout(self):
		return Label(text=str(self.points))



class ConnectTest(Test):
	"""First spatial test, connectiing letters"""

	def __init__(self, screen, **kwargs):
		super(ConnectTest, self).__init__(screen, **kwargs)
		self.drawing = utils.DrawLayer(pos_hint={"x":0, "y":0})
		self.desc = "Spojování bodů"
		self.test_field = FloatLayout()
		self.test_image = Image(source="images/test1.png")
		self.instruction = u"Spojte postupně čarou číslice a písmena.\nZačněte číslem 1 směrem k A, pak od A ke 2 \na tak dále a skončete u E"
		self.instruction_audio = "sounds/ins1-1.mp3"
		

		with self.test_field.canvas.before:
			Color(1,1,1,1) 
			self.rec = Rectangle(size=Window.size)


	def draw_uix(self):
		self.test_field.add_widget(self.test_image)
		self.test_field.add_widget(self.drawing)
		self.add_widget(self.test_field)
		super(ConnectTest, self).draw_uix()
		self.hidden_options.modify(self.drawing.erase)

	def result(self): 
		self.test_field.export_to_png("/sdcard/vysledky/{2}/{0}_{1}_1.png".format(self.screen.subject.name.replace(" ","_"), self.screen.subject.age, self.screen.subject.study))
		return self.points

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))
		
class CubeTest(Test):
	"""Cube redrawing test"""
	
	def __init__(self, screen, **kwargs):
		super(CubeTest, self).__init__(screen, **kwargs)

		self.test_field = FloatLayout()
		self.drawing = utils.DrawLayer(pos_hint={"x":0, "y":0})
		self.desc = "Překreslování"
		self.test_image = Image(source="images/test2.png")
		self.instruction = "Překreslete do volného místa dolů tuto kresbu,  \njak nejpřesněji dokážete."
		self.instruction_audio = "sounds/ins1-2.mp3"

		with self.test_field.canvas.before:
			Color(1,1,1,1) 
			self.rec = Rectangle(size=Window.size)


	def draw_uix(self):
		self.test_field.add_widget(self.test_image)
		self.test_field.add_widget(self.drawing)
		self.add_widget(self.test_field)
		super(CubeTest, self).draw_uix()
		self.hidden_options.modify(self.drawing.erase)

	def result(self):
		self.test_field.export_to_png("/sdcard/vysledky/{2}/{0}_{1}_2.png".format(self.screen.subject.name.replace(" ","_"), self.screen.subject.age, self.screen.subject.study))
		return self.points

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))

class ClockTest(Test):
	"""Clock test drawing. Dunno"""

	def __init__(self, screen, **kwargs):
		super(ClockTest, self).__init__(screen, **kwargs)

		self.test_field = FloatLayout()
		self.desc = "Hodiny"
		self.drawing = utils.DrawLayer(pos_hint={"x":0, "y":0})
		self.instruction = "Nakreslete ciferník hodin se všemi číslicemi tak, \njak jsou na ciferníku a nastavte čas, \naby hodiny ukazovaly 11 hodin a 10 minut."
		self.instruction_audio = "sounds/ins1-3.mp3"

		with self.test_field.canvas.before:
			Color(1,1,1,1) 
			self.rec = Rectangle(size=Window.size)


	def draw_uix(self):
		self.test_field.add_widget(self.drawing)
		self.add_widget(self.test_field)
		super(ClockTest, self).draw_uix()
		self.hidden_options.modify(self.drawing.erase)

	def result(self):
		self.test_field.export_to_png("/sdcard/vysledky/{2}/{0}_{1}_3.png".format(self.screen.subject.name.replace(" ","_"), self.screen.subject.age, self.screen.subject.study))
		return self.points

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))



class AnimalTestLion(Test):
	"""Animal test, Lion"""

	def __init__(self, screen, **kwargs):
		super(AnimalTestLion, self).__init__(screen, **kwargs)
		self.test_image = Image(source="images/test4lev.png")
		self.desc = "Lev"
		self.instruction = "Pojmenujte toto zvíře. \nJméno napište do řádku pod zvířetem." 
		self.instruction_audio = "sounds/ins2.mp3"
		self.name_ti = TextInput(multiline=False, size_hint=(1, .15), font_size=60, hint_text=u"Co je to za zvíře?")

		self.name_ti.bind(text=self.change_callback)
		#pridat podminku
			

	def draw_uix(self):
		self.add_widget(self.test_image)
		self.add_widget(self.name_ti)
		super(AnimalTestLion, self).draw_uix()

	def change_callback(self, instance, text):
		if text == "Lev" or text == "lev":
			self.points +=1
		else:
			self.points =0

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))


class AnimalTestRhino(Test):
	"""Animal test, Rhino"""
	def __init__(self, screen, **kwargs):
		super(AnimalTestRhino, self).__init__(screen, **kwargs)
		self.test_image = Image(source="images/test4nos.png")
		self.desc = "Nosorožec"
		self.instruction = "Pojmenujte toto zvíře. \nJméno napište do řádku pod zvířetem."
		self.instruction_audio = "sounds/ins2.mp3"
		self.name_ti = TextInput(multiline=False, size_hint=(1,.15), font_size=60, hint_text=u"Co je to za zvíře?")

		self.name_ti.bind(text=self.change_callback)

	def draw_uix(self):
		self.add_widget(self.test_image)
		self.add_widget(self.name_ti)
		super(AnimalTestRhino, self).draw_uix()

	def change_callback(self, instance, text):
		if text == u'nosorožec' or text == u'Nosorožec' or text == u'nosorozec' or text == u'Nosorozec':
			self.points +=1
		else:
			self.points =0

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))



class AnimalTestCamel(Test):
	"""Animal test, camel"""

	def __init__(self, screen, **kwargs):
		super(AnimalTestCamel, self).__init__(screen, **kwargs)
		self.test_image = Image(source="images/test4vel.png")
		self.desc = "Velbloud"
		self.instruction = "Pojmenujte toto zvíře. \nJméno napište do řádku pod zvířetem."
		self.instruction_audio = "sounds/ins2.mp3"
		self.name_ti = TextInput(multiline=False, size_hint=(1,.15), font_size=60, hint_text=u"Co je to za zvíře?")

		self.name_ti.bind(text=self.change_callback)

	def draw_uix(self):
		self.add_widget(self.test_image)
		self.add_widget(self.name_ti)
		super(AnimalTestCamel, self).draw_uix()

	def change_callback(self, instance, text):
		if text == "Velbloud" or text == "velbloud":
			self.points +=1
		else:
			self.points =0

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))



class RememberTest(Test):
	"""Remember words test"""

	def __init__(self, screen, **kwargs):
		super(RememberTest, self).__init__(screen, **kwargs)
		self.instruction = "TENTO TEST ZPRACOVÁVÁ TESTUJÍCÍ! \nPřečtěte: Toto je test paměti. \nPřečtu Vám seznam slov, která si máte zapamatovat. \nPoslouchejte pozorně. Až skončím,\nsnažte si vybavit co nejvíce slov. \nNa pořadí nezáleží. -- \n DRUHÁ ČÁST\nPřečtěte: Přečtu Vám stejný seznam slov ještě jednou. \nSnažte si zapamatovat co nejvíce slov\n a poté mi je vyjmenujte, včetně těch, \nkterá jste jmenoval/a i poprvé. -- \n Na konci testu přečtěte: Na konci testu Vás požádám, \nabyste si tato slova znovu vybavil/a."
		self.instruction_audio = "sounds/ins3-1.mp3"
		self.test_field = GridLayout(rows=3, size_hint=(.9,.5), pos_hint={"y":.25}, row_default_height=70, row_force_default=True)
		self.words = ["TVÁŘ", "SAMET", "KOSTEL", "KOPRETINA", "ČERVENÁ"]
		self.f_try = {}
		self.s_try = {}
		
		self.labels = []

		for word in self.words:
			label = Label(text=word)
			self.f_try[label] = CheckBox()
			self.s_try[label] = CheckBox()
			self.labels.append(label)
			
		
		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)
			 

	def draw_uix(self):
		self.test_field.add_widget(Label(text="Slovo", size_hint_x=.3))
		self.test_field.add_widget(utils.microgrid(False, *([utils.microgrid(True, label) for label in self.labels] + [
															 utils.AudioButton("sounds/ins3-2.mp3")])))
		
		self.test_field.add_widget(Label(text="1. pokus", size_hint_x=.3))
		self.test_field.add_widget(utils.microgrid(False, *([utils.microgrid(True, self.f_try[label]) for label in self.labels] + [
															 utils.AudioButton("sounds/ins3-3.mp3",
															 size_hint=(None, None), 
															 width=32, height=32)])))
		
		self.test_field.add_widget(Label(text="2. pokus", size_hint_x=.3))
		self.test_field.add_widget(utils.microgrid(False, *([utils.microgrid(True, self.s_try[label]) for label in self.labels] + [
															 utils.AudioButton("sounds/ins3-4.mp3",
															 size_hint=(None, None), 
															 width=32, height=32)])))

		self.add_widget(self.test_field)
		super(RememberTest, self).draw_uix()

class DokoncitTest(Test):
	def __init__(self, screen, **kwargs):
		super(DokoncitTest, self).__init__(screen, **kwargs)
		self.instruction = "Předejte zařízení Doktorovi"
		self.test_field = GridLayout(cols=2, pos_hint={"x":.5, "y":.5}, size_hint=(.25,.25)) 
		self.dokoncit_lb = Label(text="Předejte zařízení Doktorovi", width=50, size_hint=(None, .1), font_size=60)
		self.done_button = Button(text=u"Dokončit", size_hint_x=.4 , size_hint_y=.2, pos_hint={"x":.30,"y":.1})
		self.done_button.bind(on_press=screen.result_screen)

		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)

	def index_callback(self, button):
		self.test.screen.load_previous()
		if self.test.screen.previous_slide is not None:
			self.test.screen.previous_slide.popup_instruction.open()
		self.dismiss()

	def draw_uix(self):
		self.test_field.add_widget(self.dokoncit_lb)
		self.add_widget(self.done_button)
		self.add_widget(self.test_field)
		super(DokoncitTest, self).draw_uix()

class AbstractionTest(Test):
	"""Abstraction Tes"""

	def __init__(self, screen, **kwargs):
		super(AbstractionTest, self).__init__(screen, **kwargs)
		self.instruction = "TENTO TEST ZPRACOVÁVÁ TESTUJÍCÍ!\nZačněte příkladem: Řekněte mi, co mají společného pomeranč a banán.\nNyní mi řekněte, co mají společného vlak a bicykl ?\nNyní mi řekněte, co mají společného hodinky a pravítko?"
		self.test_field = GridLayout(cols=2, pos_hint={"x":.3, "y":.25}, size_hint=(.25,.25)) 
		self.vlak_bycikl_lb = Label(text="vlak - bicykl", width=50, size_hint=(None, .1))
		self.hodinky_pravitka_lb = Label(text="hodinky - pravítka", width=50, size_hint=(None, .1))
		self.vlak_bycikl_chb = CheckBox()
		self.hodinky_pravitka_chb = CheckBox()

		self.vlak_bycikl_chb.bind(active=partial(self.checkbox_callback, self))
		self.hodinky_pravitka_chb.bind(active=partial(self.checkbox_callback, self))
		 
		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)

	def draw_uix(self):
		self.test_field.add_widget(self.vlak_bycikl_lb)
		self.test_field.add_widget(self.vlak_bycikl_chb)
		self.test_field.add_widget(self.hodinky_pravitka_lb)
		self.test_field.add_widget(self.hodinky_pravitka_chb)
		self.add_widget(self.test_field)
		super(AbstractionTest, self).draw_uix()
		
	def checkbox_callback(self, inst, button, state):
		if state == True:
			self.points +=1
		else:
			self.points -=1


class NumberTest(Test):
	"""Abstraction Tes"""

	def __init__(self, screen, **kwargs):
		super(NumberTest, self).__init__(screen, **kwargs)
		self.desc = "Opakování číslic"
		self.instruction = "TENTO TEST ZPRACOVÁVÁ TESTUJÍCÍ!\nŘeknu Vám řadu číslic. Až skončím,\nopakujte je ve stejném pořadí, v jakém jste\nje slyšel/a."
		self.instruction_audio = "sounds/ins4-1.mp3"
		self.test_field = GridLayout(cols=1, pos_hint={"x":.1, "y":.3}, size_hint=(.8,.25), row_default_height=70 ,row_force_default=True) 
		self.normal_lb = Label(text="2 1 8 5 4", font_size="60px")
		self.normal_chb = CheckBox()
		self.reverse_lb = Label(text="7 4 2", font_size="60px")
		self.reverse_chb = CheckBox()

		self.normal_chb.bind(active=partial(self.checkbox_callback, self))
		self.reverse_chb.bind(active=partial(self.checkbox_callback, self))
		 
		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)

	def draw_uix(self):
		self.test_field.add_widget(utils.microgrid(False, utils.AudioButton("sounds/ins4-2.mp3"),self.normal_chb, self.normal_lb, utils.AudioButton("sounds/ins4-3.mp3")))
		self.test_field.add_widget(utils.microgrid(False, utils.AudioButton("sounds/ins4-4.mp3"), self.reverse_chb, self.reverse_lb))
		self.add_widget(self.test_field)
		super(NumberTest, self).draw_uix()
		
	def checkbox_callback(self, inst, button, state):
		if state == True:
			self.points +=1
		else:
			self.points -=1

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))


class LettersTest(Test):
	"""Abstraction Tes"""

	def __init__(self, screen, **kwargs):
		super(LettersTest, self).__init__(screen, **kwargs)
		self.desc = "Pozornost písmen"
		self.instruction = "TENTO TEST ZPRACOVÁVÁ TESTUJÍCÍ!\nPřečtu Vám řadu písmen. \nPokaždé, když řeknu písmeno A, ťukněte rukou o stůl. \nKdyž řeknu jiné písmeno, neťukejte."
		self.instruction_audio = "sounds/ins5-1.mp3"
		self.test_field = GridLayout(cols=1, pos_hint={"x":.05, "y":.3}, size_hint=(.9, .25), spacing=[5, 5]) 
		self.letters_lb = Label(text="F B A C M N A A J K L B A F A K D E A A A J A M O F A A B", 
								size_hint=(.7, .3), markup=True, font_size="60px", opacity = 0)
		self.start_btn = Button(text="START", size_hint=(.1,.4))
		#self.hide_btn = Button(text="Skrýt", size_hint=(.1,.4))
		self.clap_btn = Button(text=u"Ťuk")
		self.errors = 0

		self.start_btn.bind(on_press=partial(self.start_callback, self))
		#self.hide_btn.bind(on_press=partial(self.hide_callback, self))
		self.clap_btn.bind(on_press=partial(self.button_callback, self))
		
		self.audio_files = {'A' : SoundLoader.load("sounds/ins5-a.mp3"),
							'B' : SoundLoader.load("sounds/ins5-b.mp3"),
							'C' : SoundLoader.load("sounds/ins5-c.mp3"),
							'D' : SoundLoader.load("sounds/ins5-d.mp3"),
							'E' : SoundLoader.load("sounds/ins5-e.mp3"),
							'F' : SoundLoader.load("sounds/ins5-f.mp3"),
							'J' : SoundLoader.load("sounds/ins5-j.mp3"),
							'K' : SoundLoader.load("sounds/ins5-k.mp3"),
							'L' : SoundLoader.load("sounds/ins5-l.mp3"),
							'M' : SoundLoader.load("sounds/ins5-m.mp3"),
							'N' : SoundLoader.load("sounds/ins5-n.mp3"),
							'O' : SoundLoader.load("sounds/ins5-o.mp3")}
		
		self.letters = ['F', 'B', 'A', 'C', 'M', 'N', 'A', 'A', 'J', 'K', 'L', 
						'B', 'A', 'F', 'A', 'K', 'D', 'E', 'A', 'A', 'A', 'J', 
						'A', 'M', 'O', 'F', 'A', 'A', 'B']

		self.let = 0

		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)

	def draw_uix(self):
		self.test_field.add_widget(utils.microgrid(False, self.start_btn, self.letters_lb)) # self.hide_btn, self.letters_lb))
		self.test_field.add_widget(self.clap_btn)
		self.add_widget(self.test_field)
		super(LettersTest, self).draw_uix()
		

	#def hide_callback(self, inst, button):
	#	if self.letters_lb.opacity == 0:
	#		self.letters_lb.opacity = 1
	#	else:
	#		self.letters_lb.opacity = 0


	def start_callback(self, inst, button):
		if self.let == 0:
			Clock.schedule_interval(self.reader, 1)

	def reader(self, cosik):
		if self.let == 0 and self.errors > 1:
			self.errors = 0;
		
		if self.audio_files[self.letters[self.let]].state == "play":
			self.audio_files[self.letters[self.let]].stop()
		text = self.letters[:]
		text[self.let] = "[color=ff0000]{l}[/color]".format(l=self.letters[self.let])
		self.letters_lb.text = ' '.join(text)
		self.audio_files[self.letters[self.let]].play()
		if self.let + 1 < len(self.letters):
			self.let += 1
		else: 
			Clock.unschedule(self.reader)
			self.let = 0

		self.errors += 1
		print(self.errors)
		self.check()


	def button_callback(self, inst, button):
		if self.letters[self.let-1] == 'A':
			self.errors -= 1
		else:
			self.errors +=1


# kolik chybně z 29 kdyz 2 chybne tak nic 
	def check(self):
		self.points = 0 if self.errors > 19 else 1

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))


class SpeachRepeatTest(Test):
	"""Speach repeating test"""
	def __init__(self, screen, **kwargs):
		super(SpeachRepeatTest, self).__init__(screen, **kwargs)
		self.desc = "Opakování"
		self.instruction = "TENTO TEST ZPRACOVÁVÁ TESTUJÍCÍ!\nŘekněte: „Přečtu vám větu a Vy jí po mně zopakujete \npřesně tak slovo od slova jak jsem jí řekl.“"
		self.instruction_audio = "sounds/ins6-1.mp3"
		self.test_field = GridLayout(cols=3, size_hint=(.8, .5), row_force_default=True, row_default_height=70, pos_hint={"x":.1})
		self.sent_1 = Label(text=u"Pouze vím, že je to Jan, kdo má dnes pomáhat.", font_size="55px")
		self.sent_1_chb = CheckBox(size_hint_x=None, width=20)
		self.sent_2 = Label(text=u"Když jsou v místnosti psi, kočka se vždy schová pod gauč.", font_size="55px")
		self.sent_2_chb = CheckBox(size_hint_x=None, width=20)

		self.sent_1_chb.bind(active=partial(self.checkbox_callback, self))
		self.sent_2_chb.bind(active=partial(self.checkbox_callback, self))
		

		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)


	def draw_uix(self):
		self.test_field.add_widget(utils.AudioButton("sounds/ins6-2.mp3"))
		self.test_field.add_widget(self.sent_1)
		self.test_field.add_widget(self.sent_1_chb)
		self.test_field.add_widget(utils.AudioButton("sounds/ins6-3.mp3"))
		self.test_field.add_widget(self.sent_2)
		self.test_field.add_widget(self.sent_2_chb)
		self.add_widget(self.test_field)
		super(SpeachRepeatTest, self).draw_uix()


	def checkbox_callback(self, inst, button, state):
		if state == True:
			self.points +=1
		else:
			self.points -=1

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))



class KTest(Test):
	"""Say soooo much K words"""
	def __init__(self, screen, **kwargs):
		super(KTest, self).__init__(screen, **kwargs)
		self.desc = "Slova na K"
		self.instruction = "TENTO TEST ZPRACOVÁVÁ TESTUJÍCÍ!!! \nVaším úkolem bude vyjmenovat co nejvíce slov, která začínají na písmeno, \nkteré Vám za chvíli prozradím. Můžete vyjmenovávat jakákoliv slova. \nNesmíte však říkat vlastní jména a názvy (např. Barbora, Bratislava), \nčísla a slova, která se liší pouze koncovkou (např. \nmalba, malíř, malovat). Po 1 minutě Vás zastavím. Jste připraven/a? (pauza) \nVyjmenujte co nejvíce slov, která začínají písmenem K.“ \nPo uplynutí 60 sekund: Stop."
		self.instruction_audio = "sounds/ins8.mp3" 
		self.words = []  
		self.words.append("Vaše slova od K")
		self.counter_button = Button(text="+", font_size="60px", size_hint_x=.4 , size_hint_y=1 , pos_hint={"x":.80,"y":.01})
		self.undo_button = Button(text="Zpět", font_size="60px", size_hint_x=.4 ,  size_hint_y=1 , pos_hint={"x":.20,"y":.01})
		self.wordlist = ListView(item_strings=self.words, size_hint_x=.4, size_hint_y=1, font_size = "60px") #
		self.test_field = GridLayout(rows=3, size_hint=(.65,.9), pos_hint={"x":.35}, row_force_default=True, row_default_height=80 ,font_size = "60px")
		self.text_field = TextInput(multiline=False, font_size="60px" )
		
		self.count = 0
		self.count_lb = Label(text=str(self.count), font_size="60px", size_hint_x=.8) 
		self.counter_button.bind(on_press=partial(self.word_callback, self))
		self.undo_button.bind(on_press=partial(self.undo_callback, self))

		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)


	def word_callback(self, button, state):
		if len(self.text_field.text) > 0 and (self.text_field.text[0] == 'k' or self.text_field.text[0] == 'K'):
			self.words.append(self.text_field.text)
			self.wordlist.item_strings = self.words
			self.count += 1
			self.count_lb.text = str(self.count)
			self.text_field.text = ""

			self.points += 1 if self.count > 10 else 0

	def undo_callback(self, button, state):
		if len(self.words) > 0:
			del self.words[-1]
			self.wordlist.item_strings = self.words
			self.count -= 1
			self.count_lb.text = str(self.count)



	def draw_uix(self):
		self.add_widget(self.wordlist)
		self.test_field.add_widget(self.text_field)
		self.test_field.add_widget(utils.microgrid(False,self.undo_button,self.count_lb, self.counter_button))
		self.add_widget(self.test_field)
		super(KTest, self).draw_uix()

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))

class AdvancedRememberTest(Test):   
	"""Remember test... duh again"""

	def __init__(self, screen, **kwargs):
		super(AdvancedRememberTest, self).__init__(screen, **kwargs)
		self.instruction = "TENTO TEST ZPRACOVÁVÁ TESTUJÍCÍ!!!\nPřed chvílí jsem Vám přečetl/a seznam slov, \nkterá jste si měl(a) zapamatovat. Řekněte mi co nejvíce slov, \nkterá si z něj pamatujete."
		self.instruction_audio = "sounds/ins9.mp3"
		self.test_field = GridLayout(cols=2, size_hint=(1,.5), pos_hint={"y":.25})
		self.words = {u"TVÁŘ":"Kategorie: část těla\nVýběr ze tří: nos, tvář, ruka",
					  u"SAMET": "Kategorie: druh látky\nVýběr ze tří: pytlovina, bavlna, samet", 
					  u"KOSTEL":"Kategorie: typ stavby\nVýběr ze tří: kostel, škola, nemocnice", 
					  u"KOPRETINA": "Kategorie: druh květiny\nVýběr ze tří: růže, kopretina, tulipán", 
					  u"ČERVENÁ": "Kategorie: barva\nVýběr ze tří: červená, modrá, zelená" }
		self.f_try = {}
		self.s_try = {}
		self.t_try = {}
		
		self.labels = []

		for word in self.words:
			label = Label(text=u"[ref={re}]{re}[/ref]".format(re=word), markup=True)
			self.t_try[label] = CheckBox() 
			self.s_try[label] = CheckBox()
			self.f_try[label] = CheckBox()
			self.f_try[label].bind(active=partial(self.checkbox_callback, self))
			self.s_try[label].bind(active=partial(self.checkbox_callback, self))
			label.bind(on_ref_press=partial(self.label_callback, self))
			self.labels.append(label)
			

		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)

	def label_callback(self, inst, label, ref):
		utils.PopupHint(self.words[ref]).open()
		
	def checkbox_callback(self, inst, button, state):
		if state == True:
			self.points +=1
		else:
			self.points -=1
 
	def draw_uix(self):
		self.test_field.add_widget(Label(text="Bez nápovědy", size_hint_x=.3))

		""" This is cheaky and i like it. Basicly, iterates thru all labels, create microgrid from 
			Label and first try, which is important... not really, and from all this, create new microgrid,
			so i can easily add labels to side.
		"""
		self.test_field.add_widget(utils.microgrid(False, *[utils.microgrid(True, x, self.f_try[x]) for x in self.labels]))
		self.test_field.add_widget(Label(text="Kategoriální", size_hint_x=.3))
		self.test_field.add_widget(utils.microgrid(False, *[self.s_try[x] for x in self.labels]))
		self.test_field.add_widget(Label(text="Výběr", size_hint_x=.3))
		self.test_field.add_widget(utils.microgrid(False, *[self.t_try[x] for x in self.labels]))
		
		self.add_widget(self.test_field)
		super(AdvancedRememberTest, self).draw_uix()



class OrientationTest(Test):
	"""Last orientation test"""
	
	def __init__(self, screen, **kwargs):
		super(OrientationTest, self).__init__(screen, **kwargs)
		
		self.test_field = GridLayout(rows=2, size_hint_y=.3, pos_hint={"y":.2}) 
		self.instruction = "TESTO TEST ZPRACOVVÁVÁ TESTUJÍCÍ!!!\nZeptejte se: Kolikátého je\nDoplňující otázky: Řekněte mi, jaký je rok, \nměsíc, přesné datum a den v týdnu?\nNyní mi řekněte název tohoto místa a města, \nve kterém jsme."

		self.labels = [Label(text="Datum"),
					   Label(text="Měsíc"),
					   Label(text="Rok"),
					   Label(text="Den"),
					   Label(text="Místo"),
					   Label(text="Město")]
		self.ch_boxes = {}

		for label in self.labels:
			chb = CheckBox()
			chb.bind(active=partial(self.checkbox_callback, self))
			self.ch_boxes[label] = chb

		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)

		

	def draw_uix(self):
		self.test_field.add_widget(utils.microgrid(False, *[utils.microgrid(False, self.ch_boxes[label], label) for label in self.labels]))
		self.test_field.add_widget(Label(text=datetime.datetime.now().strftime("%H:%M %d. %h")))
		self.add_widget(self.test_field)
		super(OrientationTest, self).draw_uix() 

	def checkbox_callback(self, inst, button, state):
		if state == True:
			self.points +=1
		else:
			self.points -=1

# zkontrolovat hodnoceni viz fb + 5 poli -> tlacitko vyhodnotit

class SevenTest(Test):
	"""Last, Finally, thanks god, #nomoretabletapps, everything is app... appdate... i hate my life"""
	
	def __init__(self, screen, **kwargs):
		super(SevenTest, self).__init__(screen, **kwargs)
		self.desc = "Odečítání sedmiček"
		self.instruction = "Odečtěte od čísla 100 číslo 7 a pak pokračujte v odčítání 7."
		self.instruction_audio = "sounds/ins7.mp3"
		self.points = 0
		self.pomoc1 = 0
		self.pomoc2 = 0
		self.pomoc3 = 0
		self.pomoc4 = 0
		self.pomoc5 = 0
		self.test_field = GridLayout(cols=1, size_hint=(.2, .8), pos_hint={"x":.4})
		self.prvni = TextInput(hint=u"první", font_size="60px", size_hint_y = .6)
		self.druhy = TextInput(hint=u"druhy", font_size="60px", size_hint_y = .6)
		self.treti = TextInput(hint=u"třetí", font_size="60px", size_hint_y = .6)
		self.ctvrty = TextInput(hint=u"čtvrtý", font_size="60px", size_hint_y = .6)
		self.paty = TextInput(hint=u"pátý", font_size="60px", size_hint_y = .6)
		self.number_list = ListView(item_strings=[])

		self.prvni.bind(text=self.prvni_callback)
		self.druhy.bind(text=self.druhy_callback)
		self.treti.bind(text=self.treti_callback)
		self.ctvrty.bind(text=self.ctvrty_callback)
		self.paty.bind(text=self.paty_callback)

		with self.canvas.before:
			Color(0,0,0,1) 
			self.rec = Rectangle(size=Window.size)

	

	def prvni_callback(self, instance, text):
		if text == "93":
			self.pomoc1 =1
		else:
			self.pomoc1 =0
		self.calc()
	
	def druhy_callback(self, instance, text):
		if text == "86":
			self.pomoc2 =1
		else:
			self.pomoc2 =0
		self.calc()


	def treti_callback(self, instance, text):
		if text == "79":
			self.pomoc3=1
		else:
			self.pomoc3=0
		self.calc()


	def ctvrty_callback(self, instance, text):
		if text == "72":
			self.pomoc4 =1
		else:
			self.pomoc4 =0
		self.calc()

	def paty_callback(self, instance, text):
		if text == "65":
			self.pomoc5 =1
		else:
			self.pomoc5=0
		self.calc()

	def calc(self):
		if self.pomoc1 + self.pomoc2 + self.pomoc3 + self.pomoc4 + self.pomoc5 == 1:
			self.points = 1
		elif self.pomoc1 + self.pomoc2 + self.pomoc3 + self.pomoc4 + self.pomoc5 == 2 or self.pomoc1 + self.pomoc2 + self.pomoc3 + self.pomoc4 + self.pomoc5 == 3 :
			self.points = 2
		elif self.pomoc1 + self.pomoc2 + self.pomoc3 + self.pomoc4 + self.pomoc5  == 4 or self.pomoc1 + self.pomoc2 + self.pomoc3 + self.pomoc4 + self.pomoc5 == 5:
			self.points = 3
		else:
			self.points = 0


	def draw_uix(self):
		self.test_field.add_widget(utils.microgrid(False, self.prvni))
		self.test_field.add_widget(utils.microgrid(False, self.druhy))
		self.test_field.add_widget(utils.microgrid(False, self.treti))
		self.test_field.add_widget(utils.microgrid(False, self.ctvrty))
		self.test_field.add_widget(utils.microgrid(False, self.paty))
		self.test_field.add_widget(self.number_list)
		self.add_widget(self.test_field)
		super(SevenTest, self).draw_uix()
	
	# nemyslim ze funguje

	def export_layout(self):
		return utils.microgrid(True, Label(text=self.desc),
									 Label(text=str(self.points)))



