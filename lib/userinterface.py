#!/usr/bin/env python

#
# WallRunner Pro 3000
# VERSION: 1.0
# FILE: lib/userinterface.py
#
# Copyright 2014 Siim Orasmae
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import time
import shelve
import lcd.lcddriver
import RPi.GPIO as GPIO
lcd = lcd.lcddriver.lcd()
from sys import exit
from operator import itemgetter

import soundengine
sound = soundengine.SoundEngine()

GPIO.setmode(GPIO.BCM)

#########################################################################################

class UserInterface:
	"""Everything to do with the UI input/output, such as high scores and quit messages."""

#
# - Display the QUIT dialog
#
#	A quick and dirty implementation, but it works. Will have to make it a proper function
#	one day. Also, selecting 'No' and moving back to the parent menu relies on the Quit
#	option being the last entry in the parent menu, which is not nice at all.
#
	def question_yesno(self,question,default_answer,loc_number,mainmenu, g_set_sounds):
			lcd.lcd_clear()
			self.soundon = g_set_sounds
			self.question = question
			self.default = default_answer
			self.loc_number = loc_number
			self.mainmenu = mainmenu
			self.loc_empty = "   "

			lcd.lcd_display_string(self.question, 1)
			if (self.default == "No"):
				lcd.lcd_display_string("  > No    Yes   ", 2)
				self.answer_yesno = 0
			elif (self.default == "Yes"):
				lcd.lcd_display_string("    No  > Yes   ", 2)
				self.answer_yesno = 1

			#sleep(0.2) # debounce
			while True:
				if (GPIO.input(10) and self.answer_yesno != 0):
					sound.sfx(self.soundon, "menu_move")
					lcd.lcd_display_string("  > No    Yes   ", 2)
					self.answer_yesno = 0
				elif (GPIO.input(9) and self.answer_yesno != 1):
					sound.sfx(self.soundon, "menu_move")
					lcd.lcd_display_string("    No  > Yes   ", 2)
					self.answer_yesno = 1
				elif (GPIO.input(11)):
					sound.sfx(self.soundon, "menu_enter")
					if (self.answer_yesno == 0):
						# This relies on "Quit" being the last item in the parent menu,
						# which is not that nice. Will fix in post, eh..
						lcd.lcd_display_string(self.loc_empty + self.mainmenu[self.loc_number-1], 1)
						lcd.lcd_display_string(self.mainmenu[0] + self.mainmenu[self.loc_number], 2)
						return
					elif (self.answer_yesno == 1):
						lcd.lcd_clear()
						time.sleep(0.3)
						lcd.lcd_display_string("    Bye-bye!    ",1)
						time.sleep(1.6)
						lcd.lcd_clear()
						GPIO.cleanup()
						exit()
				time.sleep(0.1)
			return

#
# - View the HIGH SCORES ordered by score.
#
	def highscores_view(self, g_set_sounds):	
		self.soundon = g_set_sounds	
		self.highscores_file = shelve.open("data/highscores")
		self.highscores = sorted(self.highscores_file.values(), key=itemgetter(1), reverse=True)
		self.highscores_file.close()
		
		lcd.lcd_clear()
		
		if not self.highscores:
			while True:
				lcd.lcd_display_string("No high scores..", 1)
				lcd.lcd_display_string("  Go and play!  ", 2)
				if (GPIO.input(11)):
					break
					return
		elif (len(self.highscores) == 1):
			while True:
				lcd.lcd_display_string(" #1" + str(self.highscores[0][0]).rjust(4) + str(self.highscores[0][1]).rjust(8), 1)
				if (GPIO.input(11)):
					break
					return

		self.player_nr = 0
		while True:
			if (GPIO.input(9) and self.player_nr < len(self.highscores) - 2):
				time.sleep(0.1)
				sound.sfx(self.soundon, "menu_move")
				self.player_nr += 1
			elif (GPIO.input(10) and self.player_nr > 0):
				time.sleep(0.1)
				sound.sfx(self.soundon, "menu_move")
				self.player_nr -= 1
			elif (GPIO.input(11)):
				time.sleep(0.1)
				sound.sfx(self.soundon, "menu_enter")
				return

			lcd.lcd_display_string("#" + str(self.player_nr+1).rjust(2) + str(self.highscores[self.player_nr][0]).rjust(4) + str(self.highscores[self.player_nr][1]).rjust(8), 1)
			lcd.lcd_display_string("#" + str(self.player_nr+2).rjust(2) + str(self.highscores[self.player_nr+1][0]).rjust(4) + str(self.highscores[self.player_nr+1][1]).rjust(8), 2)
		return

#
# - A simple ABOUT text to display the version and copyright info.
#
	def about_view(self, g_set_sounds):
		self.soundon = g_set_sounds
		self.about_txt = [
					"WallRunner Pro3k",
					"by  Siim Orasmae",
					"    (C) 2014    ",
					"                ",
					"Dodge the walls,",
					" get the points!",
					"                ",
					"   Version 1.0  ",
					"                ",
					"   serenity.ee  "
					]
		lcd.lcd_clear()
		
		self.txt_nr = 0
		while True:
			
			if (GPIO.input(9) and self.txt_nr < len(self.about_txt) - 2):
				time.sleep(0.1)
				sound.sfx(self.soundon, "menu_move")
				self.txt_nr += 1
			elif (GPIO.input(10) and self.txt_nr > 0):
				time.sleep(0.1)
				sound.sfx(self.soundon, "menu_move")
				self.txt_nr -= 1
			elif (GPIO.input(11)):
				time.sleep(0.1)
				sound.sfx(self.soundon, "menu_enter")
				return
		
			lcd.lcd_display_string(self.about_txt[self.txt_nr], 1)
			lcd.lcd_display_string(self.about_txt[self.txt_nr+1], 2)
		return

#
# - The absolutely mandatory SETTINGS menu.
#
#	Displays stuff, saves stuff.
#
	def settings_view(self, g_set_soundss):
		self.soundon = g_set_soundss ###########------- FIX ---------------------------------------------------------
		lcd.lcd_clear()

		# The first entry (eg [0]) in the menu list is always the active selection
		# indicator, so you could use different kinds in each menu, etc.
		self.menu_list = [
				" > "
				]
		# Read the settings database and populate the rest of the list with keys
		# and values. Sort by uid set in db.
		# This one has a special condition for "Avatar", which I should rewrite..
		self.settings_file = shelve.open("data/settings")
		for self.values in sorted(self.settings_file.items(), key=itemgetter(0)):
				
				if (self.values[0] == "Avatar"):
					if (self.values[1][0] == 0):
						self.setting_value = "@  "
					elif (self.values[1][0] == 1):
						self.setting_value = "$  "
					elif (self.values[1][0] == 2):
						self.setting_value = "&  "
				elif (self.values[1][0] == 0):
					self.setting_value = "NO "
				elif (self.values[1][0] == 1):
					self.setting_value = "YES"
				
				self.menu_list.append((str(self.values[0]).ljust(8) , self.setting_value))
		self.settings_file.close()
		# And append an option to go back at the end of the list. Value not important.
		self.menu_list.append(("Back..       ","1"))

		# Define some defaults
		self.loc_arrowup = self.menu_list[0]
		self.loc_arrowdn = "   "
		self.loc_item = 1
		self.loc_disp = 1

		# Navigation and all other handling of physical button-pressing happens here.
		while True:
			
			# press "DOWN" button
			if (GPIO.input(9) and self.loc_item < len(self.menu_list) - 1):
				time.sleep(0.1)
				sound.sfx(self.soundon, "menu_move")
				if (self.loc_arrowup == self.menu_list[0]):
					self.loc_arrowup = "   "
					self.loc_arrowdn = self.menu_list[0]
					self.loc_item += 1
				else:
					self.loc_disp += 1
					self.loc_item += 1

			# press "UP" button
			elif (GPIO.input(10) and self.loc_item > 1):
				time.sleep(0.1)
				sound.sfx(self.soundon, "menu_move")
				if (self.loc_arrowdn == self.menu_list[0]):
					self.loc_arrowup = self.menu_list[0]
					self.loc_arrowdn = "   "
					self.loc_item -= 1
				else:
					self.loc_disp -= 1
					self.loc_item -= 1

			# press "A" button
			elif (GPIO.input(11)):
				time.sleep(0.1)
				sound.sfx(self.soundon, "menu_enter")
				# The last item in the list should always be "Back"!
				if (self.loc_item == len(self.menu_list) - 1):
					return
				# Other items will change value state when "A" is pressed.
				else:
					self.settings_file = shelve.open("data/settings")
					# The first entry needs to be 'Avatar'.
					# Rest of the order is not important (besides 'Back' being last).
					if (self.loc_item == 1):
						if (self.menu_list[1][1] == "@  "): # Make this clean-n-tidy one day..
							self.settings_file[self.menu_list[1][0].strip()] = int(1), int(0)
							self.menu_list.insert(self.loc_item, (self.menu_list[self.loc_item][0], "$  "))
							del self.menu_list[self.loc_item + 1]
						elif (self.menu_list[1][1] == "$  "):
							self.settings_file[self.menu_list[1][0].strip()] = int(2), int(0)
							self.menu_list.insert(self.loc_item, (self.menu_list[self.loc_item][0], "&  "))
							del self.menu_list[self.loc_item + 1]
						elif (self.menu_list[1][1] == "&  "):
							self.settings_file[self.menu_list[1][0].strip()] = int(0), int(0)
							self.menu_list.insert(self.loc_item, (self.menu_list[self.loc_item][0], "@  "))
							del self.menu_list[self.loc_item + 1]

					elif (self.menu_list[self.loc_item][1] == "YES"):
						self.settings_file[self.menu_list[self.loc_item][0].strip()] = int(0), int(self.loc_item - 1)
						
						#if (self.menu_list[self.loc_item][0].strip() == "Sounds"):
						#	global g_set_sounds
						#	g_set_sounds = 0
							
						self.menu_list.insert(self.loc_item, (self.menu_list[self.loc_item][0], "NO "))
						del self.menu_list[self.loc_item + 1]				
					elif (self.menu_list[self.loc_item][1] == "NO "):
						self.settings_file[self.menu_list[self.loc_item][0].strip()] = int(1), int(self.loc_item - 1)
						
						#if (self.menu_list[self.loc_item][0].strip() == "Sounds"):
						#	global g_set_sounds
						#	g_set_sounds = 1
							
						self.menu_list.insert(self.loc_item, (self.menu_list[self.loc_item][0], "YES"))
						del self.menu_list[self.loc_item + 1]
					self.settings_file.close()

			lcd.lcd_display_string(self.loc_arrowup + self.menu_list[self.loc_disp][0] + str(self.menu_list[self.loc_disp][1]), 1)
			lcd.lcd_display_string(self.loc_arrowdn + self.menu_list[self.loc_disp+1][0] + str(self.menu_list[self.loc_disp+1][1]), 2)

		return