# -*- coding: utf-8 -*-
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

from kivy.uix.button import Button
from kivy.uix import image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton


from functools import partial

class Painter(FloatLayout):
	""" Layer for user input (drawing suprisingly) """

	def __init__(self, **kwargs):
		super(Painter, self).__init__(**kwargs)
		self.line = None

	def on_touch_down(self, touch):
		with self.canvas:
			Color(1,0,1)
			self.line = Line(points=(touch.x, touch.y), width=10)

	def on_touch_move(self, touch):
		self.line.points += [touch.x, touch.y]

class DrawLayer(FloatLayout):

	def __init__(self, **kwargs):
		super(DrawLayer, self).__init__(**kwargs)
		self.painter = Painter()
		self.add_widget(self.painter)
		self.erase = Button(text="Smazat", font_size="40px")
		self.erase.bind(on_press=self.erase_callback)

	def erase_callback(self, b):
		self.painter.canvas.clear()




class PopupHint(Popup):
	"""Popup window created for instructions"""

	def __init__(self, text, **kwargs):
			super(PopupHint, self).__init__(**kwargs)           
			self.title = "Instrukce"
			self.text = text
			self.content = GridLayout(rows=2)
			self.create_content()

	def create_content(self):
			ins_l = Label(text=self.text, font_size="40px")
			close_b = Button(text=u"Zavřít", size_hint=(1,.25), font_size="30px")
			close_b.bind(on_press=self.dismiss)
			self.content.add_widget(ins_l)
			self.content.add_widget(close_b)

	def modify(self, *args):
			for widget in args:
				self.content.add_widget(widget)


class Hidden(Popup):
	"""Hidden popup for controling 'dumb' tests"""

	def __init__(self, test,  **kwargs):
		super(Hidden, self).__init__(**kwargs)
		self.controls = GridLayout(cols=3)
		self.title = "Možnosti"
		self.test = test
		self.create_content()

	def open(self):
		self.poi_l.text = str(self.test.points)
		super(Hidden, self).open()

	def create_content(self):
		self.poi_l = Label(text=str(self.test.points),opacity=1)
		self.plus_b = Button(text="+",opacity=1, disabled=False )
		#self.plus_b.disabled = True
		self.min_b = Button(text="-",opacity =1)
		self.prev_b = Button(text="Předchozí test")
		self.close_b = Button(text="Zavřít")
		self.next_b = Button(text="Další test")

		def plusbtn_callback(self, button):
			 self.test.points += 1
			 self.poi_l.text = str(self.test.points)

		def minbtn_callback(self, button):
			if self.test.points > 0:
				self.test.points -= 1
			self.poi_l.text = str(self.test.points)

		def nextbtn_callback(self, button):
			self.test.screen.load_next(mode="next")
			if self.test.screen.next_slide is not None:
				self.test.screen.next_slide.popup_instruction.open()
			self.dismiss()

		def prevbtn_callback(self, button):
			self.test.screen.load_previous()
			if self.test.screen.previous_slide is not None:
				self.test.screen.previous_slide.popup_instruction.open()
			self.dismiss()

		self.plus_b.bind(on_press=partial(plusbtn_callback, self))
		self.min_b.bind(on_press=partial(minbtn_callback, self))
		self.next_b.bind(on_press=partial(nextbtn_callback, self))
		self.prev_b.bind(on_press=partial(prevbtn_callback, self))
		self.close_b.bind(on_press=self.dismiss)

	
		
		self.controls.add_widget(self.prev_b)
		self.controls.add_widget(self.close_b)
		self.controls.add_widget(self.next_b)	
		self.content = self.controls
		self.controls.add_widget(self.min_b)
		self.controls.add_widget(self.poi_l)
		self.controls.add_widget(self.plus_b)	
	def modify(self, *args):
		for widget in args:
			self.controls.add_widget(widget)
			self.content = self.controls	


		


class AudioButton(Button):
	"""Simple button widget for playing given sound"""
	def __init__(self, filepath, **kwargs):
		super(AudioButton, self).__init__(**kwargs)
		self.sound_file = SoundLoader.load(filepath)
		self.background_normal = "images/speaker.png"
		self.background_down = "images/speaker_press.png"
		self.bind(on_press=partial(self.play_callback, self))
		self.width = 40
		self.height = 40
		self.size_hint = (None, None) 
		
	def play_callback(self, button, state):
		if self.sound_file.state == "stop":
			self.sound_file.play()


def microgrid(vertical, *wgts, **kwargs):
	layout = BoxLayout(orientation = "vertical" if vertical == True else "horizontal", **kwargs)
	for widget in wgts:
		layout.add_widget(widget)
	return layout

