def title_clean(ti_string):

    # Get rid of any left whitespace and check for the 'TI:' that appears at the 
    # start of a CENTRAL title field, and remove it:

    foreign_lang = False
    ti_string = ti_string.strip()
    if ti_string.startswith('TI:'):
        ti_string = ti_string[3:]
    else:
        pass

    # Split the title by a '.' if it exists. Check for a square bracket at the start
    # of the title, which would indicate a foreign language publication.  Remove the
    # square bracket and set the foreign language flag True (not used at the moment 
    # but may come in useful) 

    ti_list = ti_string.split('.')
    ti_main = ti_list[0]

    # If there is more than one item in the title split by '.', then assign the 
    # remaining data to 'ti_notes':

    if len(ti_list) < 1:
        ti_notes = ti_list[1:]
    else:
        ti_notes =[]

    if ti_main.startswith('['):
        foreign_lang = True
        ti_main = ti_main.strip(' [').rstrip('] ')
    else:
        pass
   
    return(ti_main)

