#!/usr/bin/python3

"""Define a class to represent references from any source:"""
class Reference:
	def __init__(self, ref_number = None, authors = None, title = None, source = None, uid = None, local_messages = None, abstract = None, url = None, db = None):
		self.ref_number = ref_number
		self.authors = authors
		self.title = title
		self.source = source
		self.uid = uid
		self.local_messages = local_messages
		self.abstract = abstract
		self.url = url
		self.db = db

	def generate_source(self):
		print("Journal: %s" % self.source["journal"])
		print("Year: %s" % self.source["year"])

	def __str__(self):
		return "Ref number: %d; Authors: %s; Title: %s; Source: %s" % (self.ref_number, self.authors, self.title, self.source)


def squ_bracket_check(ti_str):
    """Defines a function that scans titles for square brackets and determines
    whether they belong to a non-English language reference, or are a part of
    the title.  Removes square brackets from around non-English references, and
    any square-bracketed comments from the end of titles."""

    ti_clean = ''

    # Check to see whether the first character of the Title is a "[", which
    # indicates a non-English publication. If it is not found, append 
    # characters to the string "ti_clean". Keep adding characters until a "[" 
    # is found, which signals the start of a comment if there is a "." in the
    # preceding 2 positions, but otherwise is a part of the title:

    # Alternative coding (from 3rd line of next block):
    #   if char == "[":
    #       if "." in ti[ti.index("[") - 2:ti.index("[")]:
    #           break
    #   else:
    #       ti_clean = ti_clean + char

    if ti_str[0] != "[":
        for char in ti_str:
            if char != "[":
                ti_clean = ti_clean + char
            elif "." not in ti_str[ti_str.index("[") - 2:ti_str.index("[")]:
                ti_clean = ti_clean + char
            else:
                break
            
    # If the Title starts with a "[", then it is a non-English publication.
    # Remove the initial "[" and loop through the input string, adding 
    # characters until a "]" is found.  If it is found, determine whether it is
    # the terminal character of the reference title (in which case the loop 
    # exits and we go looking for the next reference title), or whether it is
    # closing a pair of square brackets within the title itself (in which case
    # we continue along the current line):

    else:
        sqbracket_level = 1
        ti_str = ti_str[1:-1]  # Having found the initial "[", remove it.
        while sqbracket_level > 0:
            for char in ti_str:
                if char != "]":
                    ti_clean = ti_clean + char
                    if char == "[":
                        sqbracket_level = sqbracket_level + 1
                    else:
                        pass
                else:
                    sqbracket_level = sqbracket_level - 1
                    if sqbracket_level > 0:
                        ti_clean = ti_clean + char
                    else:
                        break
#                    ti_clean.strip(".").strip()
            
    return(ti_clean)


def split_medline_source(so_field):
    """This function takes the complete field under "Source" from the 
    Medline file and splits it into its component parts, returning these as a
    dictionary."""

    (journal, numbers) = so_field.split(".", 1)
    journal = journal.strip()
    (vol_issue, pages_date) = numbers.split(":")
    vol_issue = vol_issue.strip(")")
    (volume, issue) = vol_issue.split("(")
    (pages, date) = pages_date.split(",", 1)
    (start_page, endpg) = pages.split("-")
    date_items = date.split(' ')

    # Search for the year in a date field of inconsistent formatting:
    
    for term in date_items:
        term = term.strip()
        if term[0:4].isdigit() == True:
            year = term[0:4]
        else:
            continue

    source_parts = {"journal":journal, "volume":volume, "issue":issue, 
                     "pages":pages, "start_page":start_page, "year":year}
    return source_parts


from sys import argv
script, input_file = argv


try:
	with open(input_file) as f:
		# ref_count is a running total of the references encountered, as judged by the appearance of a '<' at the start of the line.  This is different in origin to ref_number, which is read directly from the record entry (but they should give an equal result).  ref_list is a dictionary that will contain instances of class "Reference".
		ref_index = -1
		ref_list = {}
		
		for line in f:
			line = line.strip()
			if line.startswith("<"):
				ref_index += 1
				ref_number = int(line.strip("<").strip(">"))
				author_list=''
				title=''
				source=''
				ref_list[ref_index]={}


        # Now iterate through the lines in the file, looking for the terms
        # "Author", "Title" and "Source".  The actual data for each of these
        # terms starts on the next line, so use "readline()" to find them. The
        # "Source" field is split up into its components and the year (a four-
        # digit item) is retrieved. 
        # Each reference is temporarily stored in the dictionary, "current_ref".
        # current_ref starts with an index value, then follows with a list of 
        # authors, the title of the paper, and the source data including the year,
        # volume, issue, start page and finish page.


            # Find the Authors field, set the Index value for the current 
            # reference, and remove the punctuation before returning the author 
            # names as a list: 
			elif line.startswith("Authors"):
				au = f.readline().strip().strip(".")
				author_list = au.split(".")
				ref_list[ref_index]["Au"]=author_list
                # Currently it is necessary to pass the author list to sqlite3 
                # as a string; this should be modified to pass the list just
                # created. The following 4 lines form the string:
	#			author_string = '' 
	#			for item in author_list:
	#				author_string = author_string + item.strip() + ' '
	#				authors = author_string.strip()
            # Return the title as a string, with external square brackets removed 
            # in the case of foreign language references:
			elif line.startswith("Title"):
				ti = f.readline().strip()
				ti_clean = squ_bracket_check(ti)
				title = ti_clean
				ref_list[ref_index]["Ti"]=title
            # Return the components of the source data:
			elif line.startswith("Source"):
				source = f.readline()
				source = split_medline_source(source)
				ref_list[ref_index]["So"]=source
			elif line.startswith("Abstract"):
				abstr=f.readline().strip()
				ref_list[ref_index]["Ab"]=abstr
			else:
				continue
				
			#ref_list[ref_index] = Reference(ref_number=ref_index, authors=author_list, title=title, source=source)

		for ref in ref_list:
				print("Reference index (%d) = %s.\n" % (ref, ref_list[ref]))
		#	for key in ref.keys():
		#		print(ref[key])		
		#print(ref_list)

except IOError as ioerr:
	print("Unable to read file: "+str(ioerr))
	print("\n\n")




