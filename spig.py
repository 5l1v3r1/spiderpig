#!/usr/bin/python
#
#

import sys

from makepdf import make_pdf


def fuzzer(name,js):
#	js = ""
#	f = file(jsname,"r")
#	js =f.read()
#	f.close()
#	print(js)
	make_pdf(name,js)
	return 1

def fuzzer1(name,jsname):
	js = ""
	f = file(jsname,"r")
	js =f.read()
	f.close()
	print(js)
	make_pdf(name,js)


def start():
	if len(sys.argv) <3:
		print("Usage:./spig <file-name> <script-file>")
		return 0
	fuzzer1(sys.argv[1],sys.argv[2])
	

if __name__=='__main__':
	start()

