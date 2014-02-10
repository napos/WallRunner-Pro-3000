#!/usr/bin/env python

#
# WallRunner Pro 3000
# VERSION: 1.0
# FILE: lib/soundengine.py
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
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

#########################################################################################

class SoundEngine:
	"""Make some noise."""

	def __init__(self):
		self.C = 244.1
		self.D = 274.1
		self.E = 304.8
		self.F = 325.5
		self.G = 365.4
		self.A = 405.8
		self.B = 456.2
		self.C2 = 488.2
		self.play = GPIO.PWM(18, self.C)
#
# Make SFX happen
#
	def sfx(self, soundon, effect, cycle=60):
		if (soundon == 1):
			if (effect == "menu_move"):
				self.play.start(cycle)
				self.play.ChangeFrequency(100)
				time.sleep(0.05)
				self.play.ChangeFrequency(200)
				time.sleep(0.01)
				self.play.stop()
			if (effect == "menu_enter"):
				self.play.start(cycle)
				self.play.ChangeFrequency(200)
				time.sleep(0.03)
				self.play.ChangeFrequency(800)
				time.sleep(0.03)
				self.play.stop()
			if (effect == "walk"):
				self.play.start(20)
				self.play.ChangeFrequency(100)
				time.sleep(0.01)
				self.play.stop()
			if (effect == "gameover"):
				self.play.start(90)
				self.play.ChangeFrequency(400)
				time.sleep(0.3)
				self.play.ChangeFrequency(300)
				time.sleep(0.2)
				self.play.ChangeFrequency(100)
				time.sleep(0.1)
				self.play.stop()
			if (effect == "newhighscore"):
				self.play.start(40)
				self.play.ChangeFrequency(800)
				time.sleep(0.05)
				self.play.stop()
				time.sleep(0.05)
				self.play.start(40)
				self.play.ChangeFrequency(800)
				time.sleep(0.1)
				self.play.stop()
				time.sleep(0.05)
				self.play.start(40)
				self.play.ChangeFrequency(800)
				time.sleep(0.1)
				self.play.stop()
				time.sleep(0.05)
				self.play.start(40)
				self.play.ChangeFrequency(1200)
				time.sleep(0.4)
				self.play.stop()
			if (effect == "lasershoot"):
				self.play.start(30)
				self.play.ChangeFrequency(2000)
				time.sleep(0.05)
				self.play.ChangeFrequency(900)
				time.sleep(0.05)
				self.play.stop()
			if (effect == "laserhit"):
				self.play.start(80)
				self.play.ChangeFrequency(400)
				time.sleep(0.1)
				self.play.ChangeFrequency(100)
				time.sleep(0.2)
				self.play.stop()
				

#
# This thing will play music!
#
	def music(self, soundon, track, cycle=60):
		if (soundon == 1):
		
			if (track == "intro"):
				self.track_n = [self.D,self.E,self.F,self.B,self.D,self.E, self.F,self.B,self.D,self.E,self.F,self.B, self.A,self.E,self.G,self.A,self.A, self.A,self.F,self.F,self.A,self.A]
				self.track_t = [0.27]
				self.track_s = 0.02
			elif (track == "level1"):
				self.track_n = [self.C,self.D]
				self.track_t = [0.2,0.2]
				self.track_s = 0.02

			i = 0
			while i < len(self.track_n):
				self.play.start(cycle)
				self.play.ChangeFrequency(self.track_n[i]) # make universal!
				if (len(self.track_t) > 1):
					time.sleep(self.track_t[i])
				else:
					time.sleep(self.track_t[0])
				self.play.stop()
				time.sleep(self.track_s)
				i += 1
			self.play.stop()