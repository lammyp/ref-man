#!/usr/bin/python3


"""This module identifies the original database from which a file was generated.  It uses characteristic formats found in files from Medline, EMBASE and CENTRAL.  
These are:
	Medline: first reference starts with '<'; next line has 'Unique Identifier'
	EMBASE: first reference starts with '<'; next line has 'Authors'
	CENTRAL: author fields start with 'AU:' """


#Determine the encoding of the input file.  This will be either utf-8 or latin-1 (or one of its synonyms).  Do this by attempting to open the file and read a line assuming utf-8 encoding; if this fails, close the file and reopen with latin-1.  If this fails, return an error and exit.  This may change as file encoding tools are incorporated (which may allow a greater range of input encodings.)


def find_encoding(infile):
	try: 
		with open(infile) as source:
			line=source.readline()
			file_type='utf-8'
	except UnicodeDecodeError:
		source.close()
		try:
			with open(infile, encoding='latin-1') as source:
				line=source.readline()
				file_type='latin-1'
		except UnicodeDecodeError:
			file_type='unknown'
	source.close()
	return file_type		


def db_origin(infile, file_type):
	print("%s is of type %s." % (infile, file_type))
	try:
		with open(infile, encoding=file_type) as source_file:
			db = ''
			for line in source_file:
				if not line:
					break
				if "AU" in line:
					db = 'CE'
					print("Original db was CENTRAL.")
					break
				elif "<" in line:
					next_line=source_file.readline()
					if "Authors" in next_line:
						db = 'EM'
						print("Original db was EMBASE.")
						break
					elif "Unique" in next_line:
						db = 'ML'
						print("Original db was Medline.")
						break
					else:
						continue
				else:
					continue
			if db == '':
				db = None
				print("Unable to determine database origin.")
			return db

	except IOError:
		print("File not found.")

from sys import argv
script, infile = argv


if __name__ == "__main__":
	file_type = find_encoding(infile)
	if file_type == 'unknown':
		print("Unable to open file. Exiting.")
	else:
		db_origin(infile, file_type)
		print(db_origin(infile, file_type))
						




