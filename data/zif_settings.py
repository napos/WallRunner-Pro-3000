#!/usr/bin/env python

#
# Settings ZERO-INSERTION-FORCE Utility-thingy v1.0
# Enables you to manually add/change settings
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

# TODO: * Change a specific setting.
#       * Delete a specific setting.
#       * Make run location independent from db location.
#       * Graceful handling of whatever input for menu choice.


import shelve
import random
from sys import exit
from operator import itemgetter

try:
	print "\nWallRunner Pro 3000"
	print "Settings ZERO-INSERTION-FORCE Utility\n"
	print " 1. View settings"
	print " 2. Enter a new key/value"
	print " 3. Delete ALL settings"
	print " 0. Quit\n"

	while True:

		choice = input("Choice: ")

		if (choice == 1):
			# Read current settings keys/values from the database,
			# order them by time of insertion (ascending).
			print "\n## KEY     VALUE,ID"
			print "-------------------"

			settings_file = shelve.open("settings")
			#print settings_file.items() #debug
			key_nr = 1
			for value in sorted(settings_file.items(), key=itemgetter(0)):
				print str(key_nr).rjust(2), value[0].ljust(9), str(value[1]).rjust(4)
				key_nr += 1
			settings_file.close()
			print " " # what, i like newlines

		elif (choice == 2):
			# Manually add a new key/value to the database.
			# Name is truncated to 7 characters.
			# Values truncated to 1 char long int and should be [0-9].
			# A unique incremental id is used for list ordering.
			print "\nEnter a new key/value"
			set_key = raw_input("Enter key (7 char max): ")
			set_value = raw_input("Enter value (0/1): ")

			settings_file = shelve.open("settings")
			uid = 0
			for each in settings_file.keys():
				uid += 1
			settings_file[str(set_key[:7])] = int(set_value[:1]), uid
			settings_file.close()

		elif (choice == 3):
			# Delete all entries from the database.
			print "\nReally delete ALL settings?"
			yesno = raw_input("Enter YES (uppercase) to continue: ")
			if (yesno == "YES"):
				settings_file = shelve.open("settings")
				for each in settings_file.keys():
					del settings_file[each]
				settings_file.close()
			else:
				print "\nNot deleting anything...\n"

		elif (choice == 0 or choice == 4):
			print "\nBye-bye!"
			exit()

except KeyboardInterrupt:
	print "\nBye!"