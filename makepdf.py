#!/usr/bin/python
#
# project SPIDERPIG -- a pdf javascript fuzzer.	
# by dgfish3r <sachinshinde11[at]gmail.com>
# makepdf.py creates pdf files of PDF 1.5 format.
# code is from Metasploit project and converted into python module.
#
#


from random import randrange 

def ioDef(id):
	return "%d 0 obj" % id

def ioRef(id):
	return "%d 0 R" % id

def RandomNonASCIIString(count):
	result = ""
	for i in range(count):
		result + chr(randrange(1,128)+128)
	return result

	#http://blog.didierstevens.com/2008/04/29/pdf-let-me-count-the-ways/
# we dont need obfuscation right now :)
"""def  str):
		result = ""
		str.scan(/./u) do |c|
			if rand(2) == 0 and c.upcase >= 'A' and c.upcase <= 'Z'
				result + "#%x" % c.unpack("C*")[0]
			else
				result + c
			end
		end
		result
	end

	def ASCIIHexWhitespaceEncode(str)
		result = ""
		whitespace = ""
		str.each_byte do |b|
			result + whitespace + "%02x" % b
			whitespace = " " * (rand(3) + 1)
		end
		result + ">"
	end"""

def make_pdfstream(js):
	xref = []
	eol = "\x0d\x0a"
	endobj = "endobj" + eol
	pdf = "%PDF-1.5" + eol
	pdf += "%" + RandomNonASCIIString(4) + eol
	xref.append(len(pdf))
	pdf += ioDef(1) +  "<</Type/Catalog/Outlines " + ioRef(2) +  "/Pages " + ioRef(3) +  "/OpenAction " + ioRef(5) + ">>" + endobj
	xref.append(len(pdf))
	pdf += ioDef(2) +  "<</Type/Outlines/Count 0>>" + endobj
	xref.append(len(pdf))
	pdf += ioDef(3) +  "<</Type/Pages/Kids[" + ioRef(4) +  "]/Count 1>>" + endobj
	xref.append(len(pdf))
	pdf += ioDef(4) +  "<</Type/Page/Parent " + ioRef(3) +  "/MediaBox[0 0 612 792]>>" + endobj
	xref.append(len(pdf))
	pdf += ioDef(5) +  "<</Type/Action/S/JavaScript/JS " + ioRef(6) + ">>" + endobj
	xref.append(len(pdf))
	pdf += ioDef(6) +  "<</Length %s>>" % str(len(js)) + eol
	pdf += "stream" + eol
	pdf += js + eol
	pdf += "endstream" + eol
	pdf += endobj
	xrefPosition = len(pdf)
	pdf += "xref" + eol
	pdf += "0 %d" % (len(xref) + 1) + eol
	pdf += "0000000000 65535 f" + eol
#	xref.each do
# 	for index in range(len(xref)):
	for index in xref:
		pdf += "%010d 00000 n" % index + eol
	pdf += "trailer" +  "<</Size %d/Root " % (len(xref) + 1) + ioRef(1) + ">>" + eol
	pdf += "startxref" + eol
	pdf += str(xrefPosition) + eol
	pdf += "%%EOF" + eol
	return pdf




def make_pdf(name,js):
	pdf = make_pdfstream(js)
	f=file(name,"w")
	f.write(pdf)
	f.close()





if __name__ == '__main__':
	make_pdf('test.pdf','var a= app.viewerVersion;app.alert(\'version of viewer:\'+a)')
	print ioRef(12)
