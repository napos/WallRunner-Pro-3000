#!/usr/bin/env python
# coding=utf-8

#
# WallRunner Pro 3000
# VERSION: 1.1
# FILE: wallrunner.py
#
# Copyright 2014 Siim Orasmäe
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
import random
from sys import exit
from operator import itemgetter
from multiprocessing import Process

import lib.lcd.lcddriver as lcddriver
import RPi.GPIO as GPIO

import lib.animation
import lib.userinterface
import lib.soundengine
import lib.gameengine

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(18, GPIO.OUT)
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

lcd = lcddriver.lcd()
ui = lib.userinterface.UserInterface()
draw = lib.animation.DrawFrames()
sound = lib.soundengine.SoundEngine()
engine = lib.gameengine.GameEngine()

#########################################################################################

#
# Read settings
#
settings_file = shelve.open("data/settings")
for values in sorted(settings_file.items(), key=itemgetter(0)):
	if (values[0] == "Sounds"):
		global g_set_sounds
		g_set_sounds = values[1][0]
	elif (values[0] == "Avatar"):
		global g_set_avatar
		if (values[1][0] == 0):
			g_set_avatar = "@"
		elif (values[1][0] == 1):
			g_set_avatar = "$"
		elif (values[1][0] == 2):
			g_set_avatar = "&"
settings_file.close()

#
# Start with some animations.
# They are run in parallel with the corresponding sfx/music.
#
jobs = []
process = Process(target=draw.animation, args=("logo_walk",))
jobs.append(process)
process.start()

def loop_sfx():
	i = 0;
	while i < 14:
		sound.sfx(g_set_sounds, "walk")
		time.sleep(0.5)
		i += 1

process = Process(target=loop_sfx)
jobs.append(process)
process.start()

for p in jobs:
	p.join()

time.sleep(0.5)

jobs = []
process = Process(target=sound.music, args=(g_set_sounds, "intro"))
jobs.append(process)
process.start()

process = Process(target=draw.animation, args=("logo_text",))
jobs.append(process)
process.start()

for p in jobs:
	p.join()

lcd.lcd_clear()
time.sleep(0.5)
draw.game_title(g_set_sounds)
time.sleep(2)

#########################################################################################

#
# - Then display the MAIN MENU
#
mainmenu = [
				"  >",
				" New Game    ",
				" Settings    ",
				" High Scores ",
				" About       ",
				" Quit        "
				]

loc_number = 1
loc_disp = 1
loc_arrowup = mainmenu[0]
loc_arrowdn = "   "

while True:

	# press "DOWN" button
	if (GPIO.input(9) and loc_number < len(mainmenu) - 1):
		time.sleep(0.1) # debounce
		sound.sfx(g_set_sounds, "menu_move")
		if (loc_arrowup == mainmenu[0]):
			loc_arrowup = "   "
			loc_arrowdn = mainmenu[0]
			loc_number += 1
		else:
			loc_disp += 1
			loc_number += 1

	# press "UP" button
	elif (GPIO.input(10) and loc_number > 1):
		time.sleep(0.1) # debounce
		sound.sfx(g_set_sounds, "menu_move")
		if (loc_arrowdn == mainmenu[0]):
			loc_arrowup = mainmenu[0]
			loc_arrowdn = "   "
			loc_number -= 1
		else:
			loc_disp -= 1
			loc_number -= 1

	# press "A" button
	if (GPIO.input(11)):
		time.sleep(0.2) # debounce
		sound.sfx(g_set_sounds, "menu_enter")

		# The menu items have to be in the correct order for this to work.
		if (loc_number == 1): # new game
			engine.run_game(g_set_sounds, g_set_avatar)
		elif (loc_number == 5): # quit
			ui.question_yesno("  Really quit?", "No", g_set_sounds)
		else:
			if (loc_number == 2): # settings
				ui.settings_view(g_set_sounds)
			elif (loc_number == 3): # high scores
				ui.highscores_view(g_set_sounds)
			elif (loc_number == 4): # about
				ui.about_view(g_set_sounds)

	lcd.lcd_display_string(loc_arrowup + str(mainmenu[loc_disp]), 1)
	lcd.lcd_display_string(loc_arrowdn + str(mainmenu[loc_disp+1]), 2)

#########################################################################################

# make clean
lcd.lcd_clear()
GPIO.cleanup()