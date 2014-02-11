## WallRunner Pro 3000

A symphony of emotions, written in Python.

WallRunner Pro 3000 is actually a game written in Python for a *very* specific platform.
It started out as a way for me to learn more about Python and at the same time utilize a
16x2 LCD that I had lying around. And so, the best game this side of Jupiter was born!

Your mission is to dodge the evil walls.. that's it. We're not even sure if the walls are
actually evil or not, but they'll kill you regardless. That's just the way they were made.

### See it in action!

[![A Video!](http://img.youtube.com/vi/BxakTJtw0Tw/0.jpg)](http://www.youtube.com/watch?v=BxakTJtw0Tw)

### How to play it

There's no easy way to do this. First of all, take a look at the system requirements below.
To get this game running on your system without having to rewrite anything, those are the
thing you'll need.

I'll let you figure out how to connect the LCD to your RPi. The libraries to run it are
included with the game, but you'll have to include the kernel modules, etc. LCD address
should be 0x27, port 1. The piezo speaker is connected to GPIO pin nr 18.

UP button is GPIO pin 10, DOWN button is 9 and A/ENTER is pin nr 11 (all use internal pull-down resistors).

After all of those things are hooked up/working, start it with `sudo ./wallrunner.py`

*Note: sudo is required for GPIO to work.*

### System requirements

* A Raspberry Pi
* 16x2 LCD with an I2C backpack
* Piezo speaker
* 3 buttons
* a couple of breadboards
* some misc wires and stuff

### Contact

Visit [serenity.ee](http://www.serenity.ee)

---

### Changelog

**Version 1.0**

* Initial release

---

### Licence

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).