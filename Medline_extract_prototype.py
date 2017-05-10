"""This is a prototype program designed to read lines from a Medline .txt file, determine where the records start, and assign the field data for each record to an instance of the class, "Reference".  It includes a feature to determine which references are non-English and remove the square brackets from around them; at the same time, square-bracketed phrases within a title are left alone, while appended comments (which don't appear for the same reference in all databases) are removed.
Finally, it allows testing of the methods for the Reference class."""

"""Define a class to represent Medline references:"""
class MLRef:
    def __init__(self, index, authors, title, source, uid = None,
                 local_messages = None, abstract = None, url = None):
        self.uid = uid
        self.index = index
        self.authors = authors
        self.title = title
        self.source = source
        self.local_messages = local_messages
        self.abstract = abstract
        self.url = url
        self.db = Medline


"""Define a function that scans titles for square brackets and determines
whether they belong to a non-English language reference, or are a part of
the title.  Removes square brackets from around non-English references, and
any square-bracketed comments from the end of titles."""

def squ_bracket_check(ti_str):
    ti_clean = ''

    # Check to see whether the first character of the Title is a
    # "[", which indicates a non-English publication. If it is
    # not found, append characters to the string "ti_clean". Keep
    # adding characters until a "[" is found, which signals the
    # start of a comment if there is a "." in the preceding 2
    # positions, but otherwise is a part of the title:

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
            
    # If the Title starts with a "[", then it is a non-English
    # publication. Remove the initial "[" and loop through the
    # input string, adding characters until a "]" is found.  If
    # it is found, determine whether it is the terminal character
    # of the reference title (in which case the loop exits and
    # we go looking for the next reference title), or whether it
    # is closing a pair of square brackets within the title
    # itself (in which case we continue along the current line):

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


from sys import argv

script, input_file = argv

try:
    with open(input_file) as f:
        # Find the first occurrence of "<" and remove it to allow future 
        # occurrences to function as flags to a loop that determines the
        # start of each new reference.  Set the reference index, ref_count,
        # to 0:  
        for line in f:
            if line.startswith("<") == True:
                print(line)
                line = line[1:-1]
                ref_count = 0
                break
        for line in f:
            line = line.strip()
            author_list_clean = []
            if line.startswith("Authors") == True:
                print(ref_count)
                au = f.readline().strip().strip(".")
                author_list = au.split(".")
                author_list_clean = []
                for item in author_list:
                    author_list_clean.append(item.strip())
                print(author_list_clean)
            elif line.startswith("Title") == True:
                ti = f.readline().strip()
                ti_clean = squ_bracket_check(ti)
                print(ti_clean)
            elif line.startswith("Source") == True:
                source = f.readline()
                (journal, numbers) = source.split(".", 1)
                (vol_issue, pages_year) = numbers.split(":")  
                print(journal.strip())
                print(vol_issue.strip())
                print(pages_year.strip("\n"))
            elif line.startswith("<") == True:
                ref_count = ref_count + 1
                #print(ref_count)
                pass
            else:
                pass
    #print(line)

except IOError as ioerr:
    print("Unable to read file: "+str(ioerr))




print("Found the file.")
