#Determine the encoding of the input file.  This will be either utf-8 or latin-1 (or one of its synonyms).  Do this by attempting to open the file and read a line assuming utf-8 encoding; if this fails, close the file and reopen with latin-1.  If this fails, return an error and exit.  This may change as file encoding tools are incorporated (which may allow a greater range of input encodings.)

from sys import argv

script, infile = argv


def find_encoding(infile):
	try: 
		with open(infile) as source:
			line=source.readline()
			file_type='utf-8'
			source.close()
	except UnicodeDecodeError:
		source.close()
		try:
			with open(infile, encoding='latin-1') as source:
				line=source.readline()
				file_type='latin-1'
				source.close()
		except UnicodeDecodeError:
			print("Unable to determine file type.")
			source.close()
			file_type='unknown'
	return file_type
	print("File type is: %s." % file_type)

