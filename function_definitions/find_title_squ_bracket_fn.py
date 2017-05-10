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
                    # input string, adding its characters to ti_clean until a "]
                    # " is found.  If "]" is found, determine whether it is the
                    # terminal character of the reference title (in which case
                    # the loop exits and we go looking for the next reference
                    # title), or whether it is closing a pair of square brackets
                    # within the title itself (in which case we continue along
                    # the current line):

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


def find_title_medline(medline_file):
    """Searches a Medline text file and returns a string to the "ti_clean"
variable, to be assigned to the "title" field of an instance of class
"Reference".
The result is a string representing the actual title; the field is truncated at
the occurrence of the character "[" (which marks the start of a comment, which
is not standard for all database formats), unless it appears as the first
character (which is a characteristic of foreign-language publications). If a
set of square brackets is encountered within the title itself, this is
allowed for and the string is continued."""

    try:
        with open(medline_file) as f:
            for line in f:
                if "Title" in line:
                    ti = f.readline().strip()
                    ti_clean = squ_bracket_check(ti)                    
                    print(ti_clean)

                else:
                    pass

    except IOError as ioerr:
        print("Error: " + str(ioerr))


def find_title_embase(embase_file):
    """Uses the same code as for Medline file handling; imports and calls the
function find_title_medline."""

    from find_title import find_title_medline


def find_title_central(central_file):
    """Uses the "TI: " motif to determine the title field of records in a CENTRAL
text file.  Assumes iso-8859-15 (Western) encoding but will handle UTF-8 if
found."""

    from find_title_squ_bracket_fn import squ_bracket_check

    try:
        with open(central_file, encoding="iso8859_15") as f:
            ti_clean = ''
            for line in f:
                if line.startswith("TI:"):
                    ti_text = line.strip("TI:").strip()
                    ti_clean = squ_bracket_check(ti_text)
                else:
                    continue
                
                print(ti_clean)
                
    except IOError as ioerr:
        print("Error: "+str(ioerr))


    

#print("Here are the Medline titles:")   
find_title_medline("Clonidine_Medline_results_290910.txt")
#print("Here are the EMBASE titles: \n")
#find_title_embase("Clonidine_EMBASE_results_290910.txt")
#print("here are the CENTRAL titles: \n")
#find_title_central("Clonidine_CENTRAL_results_030910_2.txt")




                
