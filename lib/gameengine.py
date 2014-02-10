#!/usr/bin/env python
# coding=utf-8

#
# WallRunner Pro 3000
# VERSION: 1.0
# FILE: lib/gameengine.py
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
import random
import shelve
from operator import itemgetter
from multiprocessing import Process

import lcd.lcddriver as lcddriver
import RPi.GPIO as GPIO

import soundengine
sound = soundengine.SoundEngine()

lcd = lcddriver.lcd()

#########################################################################################

class GameEngine:
	"""What this does"""
	
	# def runInParallel(*fns):
	#   proc = []
	#   for fn in fns:
	#     p = Process(target=fn)
	#     p.start()
	#     proc.append(p)
	#   for p in proc:
	#     p.join()
	#runInParallel(draw.animation("logo_text"), sound.music(1, "intro"))
	
	def run_parallel(self, *function):
		self.fnc = function
		self.jobs = []
		for i in self.fnc:
			print i
			#self.run = Process(target=, args=(fnc[i][1]))
			#self.append(self.fnc[i][0])
		for p in self.jobs:
			p.join()

#
# SCORE input
#
	def score_input(self, score):
		self.alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
		self.name = ["A","A","A"]
		self.score = score
		
		self.count_a = 0
		self.count_n = 0
		self.blink = 0
		
		while True:
			if (self.blink == 1):
				self.name[self.count_n] = " "
				self.blink = 0
			else:
				self.name[self.count_n] = self.alphabet[self.count_a]
				self.blink = 1
		
			if (GPIO.input(9)):
				self.name[self.count_n] = self.alphabet[self.count_a + 1]
				self.count_a += 1
			elif (GPIO.input(10)):
				self.name[self.count_n] = self.alphabet[self.count_a - 1]
				self.count_a -= 1
			
			if (GPIO.input(11) and self.count_n < 2):
				self.name[self.count_n] = self.alphabet[self.count_a]
				self.count_n += 1
				self.count_a = 0
			elif (GPIO.input(11) and self.count_n == 2):
				self.name[self.count_n] = self.alphabet[self.count_a]
				self.highscore_file = shelve.open("data/highscores")
				self.uid = "id" + str(random.randint(1, 99999999))
				self.highscore_file[self.uid] = str("".join(self.name)), int(self.score)
				self.highscore_file.close()
				
				lcd.lcd_display_string("  Thank you     ", 1)
				lcd.lcd_display_string("   for playing! ", 2)
				time.sleep(2)
				break
			
			lcd.lcd_display_string("  Name:   " + "".join(self.name), 1)
			lcd.lcd_display_string(" Score: " + str(self.score).center(7), 2)
			time.sleep(0.1)

#
# Run the game, man!
#
	def run_game(self, character="@", difficulty="hard"):
		lcd.lcd_clear()
		
		time.sleep(0.4)
		lcd.lcd_display_string("    Level  1    ", 1)
		time.sleep(0.8)
		lcd.lcd_display_string("     Start!     ", 2)
		time.sleep(0.5)
		
		self.player = character
		self.difficulty = difficulty
		self.stage_row_up = [" ", " ", self.player, " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "E"]
		self.stage_row_dn = [" ", " ", " ",         " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "E"]
		
		self.score = 0

		# Some initial setup
		self.last_wall_up = 0
		self.last_wall_dn = 0
		self.loc_wall_up = 16
		self.loc_wall_dn = 16
		self.loc_laser_up = 16
		self.loc_laser_dn = 16

		# Difficulty settings
		if (self.difficulty == "easy"):
			self.ammo = 3
			self.sleeptime = 0.2
			self.rand_wall_max = 8
			self.rand_wall_interval = 5
			self.rand_score_max = 22
			self.rand_score_multiply_l = 6
			self.rand_score_multiply_h = 9
		elif (self.difficulty == "medium"):
			self.ammo = 2
			self.sleeptime = 0.1
			self.rand_wall_max = 6
			self.rand_wall_interval = 4
			self.rand_score_max = 26
			self.rand_score_multiply_l = 8
			self.rand_score_multiply_h = 12
		elif (self.difficulty == "hard"):
			self.ammo = 1
			self.sleeptime = 0
			self.rand_wall_max = 4
			self.rand_wall_interval = 3
			self.rand_score_max = 32
			self.rand_score_multiply_l = 11
			self.rand_score_multiply_h = 16

		# Debug settings
		self.debug = 0
		self.debug_count = 1
		
		# Start the game!
		while True:
			
			# Each frame needs a random number for wall generation
			self.random_row = random.randint(1, self.rand_wall_max)
			#self.random_wall = random.randint(1, 3)

			# Make walls happen based on random nr, distance from last wall on same row and opposite row as well
			self.last_wall_up += 1
			self.last_wall_dn += 1
			if (self.random_row == 1 and self.last_wall_up > random.randint(3, self.rand_wall_interval) and self.last_wall_dn >= 3):
				self.stage_row_up[16] = "#"
				#debuggery info
				#print "-------------------------"
				#print "nr.    ", self.debug_count
				#print "random ", self.random_row
				#print "last up", self.last_wall_up
				#print "last dn", self.last_wall_dn
				#self.debug_count += 1
				self.last_wall_up = 0
			if (self.random_row == 2 and self.last_wall_dn > random.randint(3, 5) and self.last_wall_up >= 3):
				self.stage_row_dn[16] = "#"
				self.last_wall_dn = 0

			# Move the walls one tile to the left with each passing frame.
			# If at 0, delete the wall. Also delete any explosions.
			self.count_up = 0
			while (self.count_up <= 16):
				for value in self.stage_row_up:
					if (value == "#" or value == "*"):
						if (self.count_up == 0):
							self.stage_row_up[self.count_up] = " " # DEL WALL IF AT LOC 0
						elif (self.stage_row_up[self.count_up] == "*"):
							self.stage_row_up[self.count_up] = " "
						else:
							self.stage_row_up[self.count_up] = " "
							self.stage_row_up[self.count_up - 1] = "#"
					self.count_up += 1
			# row_dn
			self.count_dn = 0
			while (self.count_dn <= 16):
				for value in self.stage_row_dn:
					if (value == "#" or value == "*"):
						if (self.count_dn == 0):
							self.stage_row_dn[self.count_dn] = " "
						elif (self.stage_row_dn[self.count_dn] == "*"):
							self.stage_row_dn[self.count_dn] = " "
						else:
							self.stage_row_dn[self.count_dn] = " "
							self.stage_row_dn[self.count_dn - 1] = "#"
					self.count_dn += 1
				
 			# See if the laser has been fired and move the beam
 			if (self.stage_row_up[self.loc_laser_up] == "-" and self.loc_laser_up < 16):
 				self.stage_row_up[self.loc_laser_up] = " "
 				self.stage_row_up[self.loc_laser_up + 1] = "-"
 				if (self.loc_laser_up != 16):
 					self.loc_laser_up += 1
 				else:
 					self.loc_laser_up = 16
 			# row_dn
 			if (self.stage_row_dn[self.loc_laser_dn] == "-" and self.loc_laser_dn < 16):
 				self.stage_row_dn[self.loc_laser_dn] = " "
 				self.stage_row_dn[self.loc_laser_dn + 1] = "-"
 				if (self.loc_laser_dn != 16):
 					self.loc_laser_dn += 1
 				else:
 					self.loc_laser_dn = 16

			# Handle physical input
			if (GPIO.input(9)): #down
				time.sleep(0.1)
				# move the player
				self.stage_row_up[2] = " "
				self.stage_row_dn[2] = self.player
				sound.sfx(1, "walk")
			elif (GPIO.input(10)): #up
				time.sleep(0.1)
				# move the player
				self.stage_row_up[2] = self.player
				self.stage_row_dn[2] = " "
				sound.sfx(1, "walk")
			elif (GPIO.input(11)): #a
				time.sleep(0.1)
				# Locate player and shoot laser
				if (self.ammo > 0):
					self.ammo -= 1
					sound.sfx(1, "lasershoot")
					if (self.stage_row_up[2] == self.player):
						self.stage_row_up[3] = "-"
						self.loc_laser_up = 3
					if (self.stage_row_dn[2] == self.player):
						self.stage_row_dn[3] = "-"
						self.loc_laser_dn = 3
			
			# Laser collision detection ----------------------------- a bit borked -----------------------------
			if (self.loc_laser_up != 16):
				if (self.stage_row_up[self.loc_laser_up + 1] == "#" and self.loc_laser_up < 15):
					sound.sfx(1, "laserhit")
					self.stage_row_up[self.loc_laser_up + 1] = "*"
					self.stage_row_up[self.loc_laser_up] = " "
					self.loc_laser_up = 16
			elif (self.loc_laser_dn != 16):
				if (self.stage_row_dn[self.loc_laser_dn + 1] == "#" and self.loc_laser_dn < 15):
					sound.sfx(1, "laserhit")
					self.stage_row_dn[self.loc_laser_dn + 1] = "*"
					self.stage_row_dn[self.loc_laser_dn] = " "
					self.loc_laser_dn = 16
				
			
			# Calculate the score based on difficulty, level nr, and random numbers
			if (self.stage_row_up[2] == self.player and self.stage_row_dn[2] == "#"):
				self.score += random.randint(14, self.rand_score_max)
				sound.sfx(1, "menu_enter")
			elif (self.stage_row_dn[2] == self.player and self.stage_row_up[2] == "#"):
				self.score += random.randint(16, self.rand_score_max)
				sound.sfx(1, "menu_enter")

			# Player collision detection and 'game over'/'high score' handling
			if (self.stage_row_up[2] == self.player and self.stage_row_up[3] == "#"):
				self.stage_row_up[2] = "X"
				lcd.lcd_display_string("".join(self.stage_row_up), 1)
				lcd.lcd_display_string("".join(self.stage_row_dn), 2)
				sound.sfx(1, "gameover")
				time.sleep(1)
				lcd.lcd_clear()
				self.finalscore = self.score * random.randint(self.rand_score_multiply_l, self.rand_score_multiply_h)
				lcd.lcd_display_string("   Game Over!   ", 1)
				
				# Is there a new high score?
				self.highscores_file = shelve.open("data/highscores")
				self.highscores = sorted(self.highscores_file.values(), key=itemgetter(1), reverse=True)
				self.highscores_file.close()
				self.scorecountup = 0
				while (self.scorecountup < self.finalscore):
					lcd.lcd_display_string(str(self.scorecountup).center(16), 2)
					self.scorecountup += random.randint(82, 101)
				lcd.lcd_display_string(str(self.finalscore).center(16), 2)
				time.sleep(1)
				if (int(self.finalscore) > int(self.highscores[0][1])): # -------------- borked if ![0][1] --------------
					time.sleep(0.6)
					lcd.lcd_display_string("  High  score!  ", 2)
					sound.sfx(1, "newhighscore")
				
				time.sleep(2)
				if (int(self.finalscore) > 0):
					self.score_input(str(self.finalscore))
				lcd.lcd_display_string("  > New Game    ", 1) # a cop-out
				lcd.lcd_display_string("    Settings    ", 2) # which i'll fix in post
				break
			elif (self.stage_row_dn[2] == self.player and self.stage_row_dn[3] == "#"):
				self.stage_row_dn[2] = "X"
				lcd.lcd_display_string("".join(self.stage_row_up), 1)
				lcd.lcd_display_string("".join(self.stage_row_dn), 2)
				sound.sfx(1, "gameover")
				time.sleep(1)
				self.finalscore = self.score * random.randint(self.rand_score_multiply_l, self.rand_score_multiply_h)
				lcd.lcd_display_string("   Game Over!   ", 1)
				# Is there a new high score?
				self.highscores_file = shelve.open("data/highscores")
				self.highscores = sorted(self.highscores_file.values(), key=itemgetter(1), reverse=True)
				self.highscores_file.close()
				self.scorecountup = 0
				while (self.scorecountup < self.finalscore):
					lcd.lcd_display_string(str(self.scorecountup).center(16), 2)
					self.scorecountup += random.randint(82, 101)
				lcd.lcd_display_string(str(self.finalscore).center(16), 2)
				time.sleep(1)
				if (int(self.finalscore) > int(self.highscores[0][1])):
					time.sleep(0.6)
					lcd.lcd_display_string("  High  score!  ", 2)
					sound.sfx(1, "newhighscore")
				time.sleep(2)
				if (int(self.finalscore) > 0):
					self.score_input(str(self.finalscore))
				lcd.lcd_display_string("  > New Game    ", 1) # a cop-out
				lcd.lcd_display_string("    Settings    ", 2) # which i'll fix in post
				break

			# Draw the frame
			lcd.lcd_display_string("".join(self.stage_row_up), 1)
			lcd.lcd_display_string("".join(self.stage_row_dn), 2)
			
			# And end the frame
			time.sleep(self.sleeptime)