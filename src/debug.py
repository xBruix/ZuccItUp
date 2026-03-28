# Author: Caleb
#
# This file enables debugging for any class or file.
# It contains a global variable called DEBUG_MODE that is True when you run a file in debug-mode -- like this:
# > python3 main.py debug
#
# Otherwise, debug mode is always turned off. As an example for how to use Debug Mode, do something like this:

# from debug import DEBUG_MODE
# ...some code...
# if DEBUG_MODE:
# 		print("Some debug statement")
# ...more code...

import sys

DEBUG_MODE = False
if len(sys.argv) > 1:
	if sys.argv[1].lower() == "debug":
		DEBUG_MODE = True