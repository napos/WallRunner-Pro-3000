#!/usr/bin/env python

#
# High Score ZERO-INSERTION-FORCE Utility-thingy v1.0
# Enables you to manually add/view high scores
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

# TODO: * Check if input name is [A-Z] and score is [0-9] etc.
#       * Make run location independent from db location.
#       * Ability to delete by user/last-n-entries/whatever.
#       * Graceful handling of whatever input for menu choice.

import shelve
import random
from sys import exit
from operator import itemgetter

try:
	print "\nWallRunner Pro 3000"
	print "High Score ZERO-INSERTION-FORCE Utility\n"
	print " 1. View high scores"
	print " 2. Enter a new high score"
	print " 3. Delete ALL high scores"
	print " 0. Quit\n"

	while True:

		choice = input("Choice: ")

		if (choice == 1):
			# Read current high scores from the database,
			# order them by score (descending).
			print "\n## NAME   SCORE"
			print "---------------"

			highscore_file = shelve.open("highscores")
			user_nr = 1
			for value in sorted(highscore_file.values(), key=itemgetter(1), reverse=True):
				print str(user_nr).rjust(2), value[0], str(value[1]).rjust(8)
				user_nr += 1
			highscore_file.close()
			print " " # what, i like newlines

		elif (choice == 2):
			# Manually add a new high score to the database.
			# Name is truncated to 3 characters and capitalized.
			# Score is truncated to 7 characters.
			# A pseudo-random id is used for key as not to overwrite any entries (not the best solution).
			print "\nEnter a new high score"
			user_name = raw_input("Enter name (3 char max): ")
			user_score = raw_input("Enter score (7 char max): ")

			highscore_file = shelve.open("highscores")
			uid = "id" + str(random.randint(1, 99999999))
			highscore_file[uid] = str(user_name[:3].upper()), int(user_score[:7])
			highscore_file.close()

		elif (choice == 3):
			# Delete all entries from the database.
			print "\nReally delete ALL high scores?"
			yesno = raw_input("Enter YES (uppercase) to continue: ")
			if (yesno == "YES"):
				highscore_file = shelve.open("highscores")
				for each in highscore_file.keys():
					del highscore_file[each]
				highscore_file.close()
			else:
				print "\nNot deleting anything...\n"

		elif (choice == 0 or choice == 4):
			print "\nBye-bye!"
			exit()

except KeyboardInterrupt:
	print "\nBye!"