
"""This is a prototype program designed to read lines from an EMBASE .txt file,
determine where the records start, and assign the data for each record to an 
entry in a dictionary (EMRef). 
The title string in EMBASE is not surrounded by square brackets, so the 
'squ_bracket_check' function that appears in Medline_extract.py is not needed here. 
Author initials are presented with full stops following each initial character; 
hyphens are frequently used for dual foreign given names; these need to be parsed 
appropriately and converted to the common format (initials in a contiguous string, 
with punctuation marks removed.""" 



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

