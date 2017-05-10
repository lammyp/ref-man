"""This is a prototype program designed to read lines from a Medline .txt file,
determine where the records start, and assign the data for each record to an 
entry in a dictionary (MLRef).  
It includes a feature to determine which references are non-English and remove 
the square brackets from around them; at the same time, square-bracketed 
phrases within a title are left alone, while appended comments (which don't 
appear for the same reference in all databases) are removed."""


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
                    ti_clean.strip(".").strip()
            
    return(ti_clean)


def split_source(so_field):
    """This function takes the complete field under "Source" from the 
    Medline file and splits it into its component parts, returning these as a
    dictionary."""

    (journal, numbers) = so_field.split(".", 1)
    journal = journal.strip()
    (vol_issue, pages_date) = numbers.split(":")
    vol_issue = vol_issue.strip(")")
    (volume, issue) = vol_issue.split("(")
    (pages, date) = pages_date.split(",", 1)
    date_items = date.split(' ')

    # Search for the year in a date field of inconsistent formatting:
    
    for term in date_items:
        term = term.strip()
        if term[0:4].isdigit() == True:
            year = term[0:4]
        else:
            continue

    source_parts = {"journal":journal, "volume":volume, "issue":issue, 
                     "pages":pages, "year":year}
    return source_parts


from sys import argv
import sqlite3

script, input_file = argv

con1 = sqlite3.connect('ref1.db')
c1 = con1.cursor()

try:
    c1.execute('''CREATE TABLE ml1(id INT NOT NULL, Authors TEXT NOT NULL, 
               Year INT NOT NULL)''')
except sqlite3.OperationalError:
    print("Using existing table.")
    pass

try:
    with open(input_file) as f:

        # Find the first occurrence of "<" and remove it to allow future 
        # occurrences to function as flags to a loop that determines the start
        # of each new reference.  Set the reference index, ref_count, to 0:  

        for line in f:
            if line.startswith("<") == True:
                line = line[1:-1]
                ref_count = 0
                break

        # Now iterate through the lines in the file, looking for the terms
        # "Author", "Title" and "Source".  The actual data for each of these
        # terms starts on the next line, so use "readline()" to find them. The
        # "Source" field is split up into its components and the year (a four-
        # digit item) is retrieved. 
        # Each reference is temporarily stored in the dictionary, "current_ref".
        # current_ref starts with an index value, then follows with a list of 
        # authors, the title of the paper, and the source data including the year,
        # volume, issue, start page and finish page.

        current_ref = {}
        for line in f:
            line = line.strip()
            # Find the Authors field, set the Index value for the current reference,
            # and remove the punctuation before returning the author names as a string.
            if line.startswith("Authors") == True:
                current_ref["Index"] = ref_count
                au = f.readline().strip().strip(".")
                author_list = au.split(".")
                author_string = '' 
                for item in author_list:
                    author_string = author_string +'  '+ item.strip()
                current_ref["Authors"] = author_string
            # Return the title as a string, with external square brackets removed 
            # in the case of foreign language references:
            elif line.startswith("Title") == True:
                ti = f.readline().strip()
                ti_clean = squ_bracket_check(ti)
                current_ref["Title"] = ti_clean
            # Return the components of the source data:
            elif line.startswith("Source") == True:
                source = f.readline()
                current_ref["Source"] = source
                current_ref["pubdata"] = split_source(source)
                current_ref["Journal"] = current_ref["pubdata"]["journal"]
                current_ref["Year"] = current_ref["pubdata"]["year"]
                current_ref["Volume"] = current_ref["pubdata"]["volume"]

            # Presently the best (least worst) way of signalling the end of a 
            # reference is by finding the "Link" reference to the url, which is
            # the last field in each reference.  The "<" character that leads 
            # the next reference could be used, but then there would be nothing
            # to signal the program to output the results from the last record,
            # as there is no "<" at the very end of the file.  This portion of 
            # the code may change when I find a better solution:

            elif line.startswith("Link") == True: 
                #print(current_ref, "\n")
                ref_data = (current_ref["Index"], current_ref["Authors"], 
                            current_ref["Journal"], current_ref["Year"], current_ref["Title"])
                print(ref_data)
                short_data = (ref_count, current_ref["Authors"], int(current_ref["Year"]),)
                # print(short_data)
                c1.execute('INSERT INTO ml1 VALUES (?, ?, ?)', short_data)
                con1.commit()
            elif line.startswith("<") == True:
                ref_count = ref_count + 1
            else:
                pass


except IOError as ioerr:
    print("Unable to read file: "+str(ioerr))
print("\n\n")

con1.close()

