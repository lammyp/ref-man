
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

