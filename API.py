#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from word_finder import find_relatives
if __name__ == "__main__":
	
	for idx,arg in enumerate(sys.argv[1:]):
		if arg.startswith('-w'):
			word = arg.replace('-w','')
			print find_relatives(word)

		else:
			print "you should enter the command like: python API.py -wسلام" 