#!/usr/bin/env python

#
# WallRunner Pro 3000
# VERSION: 1.0
# FILE: lib/animation.py
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
import soundengine
import lcd.lcddriver
lcd = lcd.lcddriver.lcd()
sound = soundengine.SoundEngine()

#########################################################################################

class DrawFrames:
	"""Draw animations. Requires (1) list with frames, (2) list with timings."""

	def __init__(self):
		
		# The walking penguin animation frames and timing
		self.logo_walk_t = [0.01]
		self.logo_walk_f = [
						"                ",
						"                ",
						"_               ",
						"o               ",
						"_               ",
						"o               ",
						" _              ",
						".o              ",
						" _              ",
						".o              ",
						"  _             ",
						"o.o             ",
						"  _             ",
						"o.o             ",
						"_ _             ",
						"o.o             ",
						"_  _            ",
						" o.o            ",
						"_  _            ",
						" o.o            ",
						" _ _            ",
						" o.o            ",
						" _  _           ",
						"  o.o           ",
						" _  _           ",
						"  o.o           ",
						"  _ _           ",
						"  o.o           ",
						"  _  _          ",
						"   o.o          ",
						"  _  _          ",
						"   o.o          ",
						"   _ _          ",
						"   o.o          ",
						"   _  _         ",
						"    o.o         ",
						"   _  _         ",
						"    o.o         ",
						"    _ _         ",
						"    o.o         ",
						"    _  _        ",
						"     o.o        ",
						"    _  _        ",
						"     o.o        ",
						"     _ _        ",
						"     o.o        ",
						"     _  _       ",
						"      o.o       ",
						"     _  _       ",
						"      o.o       ",
						"      _ _       ",
						"      o.o       ",
						"      _  _      ",
						"       o.o      ",
						"      _  _      ",
						"       o.o      ",
						"       _ _      ",
						"       o.o      ",
						"       _  _     ",
						"        o.o     ",
						"       _  _     ",
						"        o.o     ",
						"        _ _     ",
						"        o.o     ",
						"        _  _    ",
						"         o.o    ",
						"        _  _    ",
						"         o.o    ",
						"         _ _    ",
						"         o.o    ",
						"         _  _   ",
						"          o.o   ",
						"         _  _   ",
						"          o.o   ",
						"          _ _   ",
						"          o.o   ",
						"          _  _  ",
						"           o.o  ",
						"          _  _  ",
						"           o.o  ",
						"           _ _  ",
						"           o.o  ",
						"           _ _  ",
						"           o.o  ",
						"           _ _  "]

		# Little Penguin Games text frames and timings
		self.logo_text_t = [0.5, 1, 0.5, 1.5, 0.5, 0.5, 0.5, 0.5]
		self.logo_text_f =  [
						"                ",
						"           o.o  ",
						" little    _ _  ",
						" little    o.o  ",
						" penguin   _ _  ",
						" little    s.o  ",
						" penguin   _ _  ",
						" little    o.o  ",
						" penguin   _ _  ",
						" penguin   o.o  ",
						" games     _ _  ",
						" games     o.o  ",
						" presents  _ _  ",
						" presents  o.o  ",
						"           _ _  ",
						"           o.o  ",
						"           _ _  "]

		# The game's title animation
		self.title_t = [0.005]
		self.title_f = [
						"                ",
						"   W            ",
						"   Wa           ",
						"   Wal          ",
						"   Wall         ",
						"   WallR        ",
						"   WallRu       ",
						"   WallRun      ",
						"   WallRunn     ",
						"   WallRunne    ",
						"   WallRunner   ",
						"    Pro         ",
						"    Pro 3       ",
						"    Pro 30      ",
						"    Pro 300     ",
						"    Pro 3000    "]

	def animation(self, frames):
		"""Animate list items. Requires list var name."""
		self.frames = frames
		self.display_l1 = 1
		self.display_l2 = 2
		self.display_sleep = 0
		self.display_sound = 0

		if (self.frames == "logo_walk"):
			self.frames = self.logo_walk_f
			self.timing = self.logo_walk_t
		elif (self.frames == "logo_text"):
			self.frames = self.logo_text_f
			self.timing = self.logo_text_t

		# Every odd number in list gets row 1 and even numbered values go on row 2.
		# If the timings list has only one value, use it for all frames. Otherwise
		# each value in the timings list corresponds to same nr value in frames list.
		while (self.display_l1 < len(self.frames)):
			lcd.lcd_display_string(self.frames[self.display_l1], 1)
			lcd.lcd_display_string(self.frames[self.display_l2], 2)
			self.display_l1 += 2
			self.display_l2 += 2
			time.sleep(self.timing[self.display_sleep])
			if (len(self.timing) > 1):
				self.display_sleep += 1

	# This one is separate because I couldn't be bothered :D
	# I'll fix it in post..
	def game_title(self):
		"""Draw the game's title animation."""
		self.frames = 0
		lcd.lcd_clear()

		while (self.frames < 16):
			if (self.frames <= 10):
				lcd.lcd_display_string(self.title_f[self.frames], 1)
				sound.sfx(1, "walk")
				time.sleep(0.005)
			elif (self.frames == 11):
				time.sleep(0.5)
				lcd.lcd_display_string(self.title_f[self.frames], 2)
				sound.sfx(1, "menu_move")
				time.sleep(1)
			elif (self.frames > 11):
				lcd.lcd_display_string(self.title_f[self.frames], 2)
				sound.sfx(1, "menu_enter")
				time.sleep(0.5)
			self.frames += 1