"""This is a prototype program designed to read lines from a Medline .txt file,
determine where the records start, and assign the data for each record to an 
entry in a dictionary (MLRef).  
It includes a feature to determine which references are non-English and remove 
the square brackets from around them; at the same time, square-bracketed 
phrases within a title are left alone, while appended comments (which don't 
appear for the same reference in all databases) are removed."""


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
    ti_main = ti_list[0].strip()

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


def split_central_source(so_field):
    """This function reads the data from the fields: SO, YR, VL, NO and PG and 
    uses them to construct a source field similar to those extracted from the 
    "Source" data in Medline and EMBASE."""

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
import sqlite3

script, input_file = argv

# Create a connection object to the database, ref1.db:
con1 = sqlite3.connect('ref2.db')
# Create a cursor object:
c1 = con1.cursor()

# Create a table to accept the reference data, unless it already exists:
try:
    c1.execute('''CREATE TABLE ml1(id INT NOT NULL, Authors TEXT NOT NULL, 
               Year INT NOT NULL)''')
except sqlite3.OperationalError:
    print("Using existing table.")
    pass

try:
    with open(input_file, encoding = "iso8859") as f:

        # Each reference is temporarily stored in the dictionary, "current_ref".
        # current_ref starts with an index value, then follows with a list of 
        # authors, the title of the paper, and the source data including the 
        # year, volume, issue, start page and finish page.

        current_ref = {}
        ref_count = 0
        AU = False
        for line in f:
            line = line.strip()
            # Look for Author (AU:) lines and extract the data into a list:
            if line.startswith("AU:"):
                AU = True
                current_ref["Index"] = ref_count
                author_list = []
                author_list.append(line[4:].strip())
                while AU == True:
                    line = f.readline()
                    if line.startswith("AU:"):
                        author_list.append(line[4:].strip())
                    # Needed to put the Title search line in here due to 
                    # problems with readline() advancing the line and missing
                    # it. 
                    elif line.startswith("TI:"):
                        ti = line.strip()
                        AU = False
                    else:
                        AU = False
                        break

                # Currently it is necessary to pass the author list to sqlite3 
                # as a string; this should be modified to pass the list just
                # created. The following 4 lines create the string:

                author_string = '' 
                print(author_list)
                for item in author_list:
                    author_string = author_string +'  '+ str(item)
                current_ref["Authors"] = author_string
                print(author_string)

                # Use the function ti_clean to process the title field to return
                # the basic title, stripped of any square brackets, field 
                # markers (TI:) and other comments:

                title = title_clean(ti)
                print(title)

            # Return the components of the source data:
            elif line.startswith("SO:"):
                current_ref["Journal"] = line[4:].strip()
                print(current_ref["Journal"])
            elif line.startswith("YR:"):
                current_ref["Year"] = line[4:].strip()
                print(current_ref["Year"])
            elif line.startswith("VL:"):
                current_ref["Volume"] = line[4:].strip()
                print(current_ref["Volume"])
            elif line.startswith("NO"):
                current_ref["Issue"] = line[4:].strip()
            elif line.startswith("PG"):
                current_ref["Pages"] = line[4:].strip()
            elif line.startswith("Link") == True: 
                #print(current_ref, "\n")
                ref_data = (current_ref["Index"], current_ref["Authors"], 
                            current_ref["Journal"], current_ref["Year"], 
                            current_ref["Title"])
                print(ref_data)
                print('')
                short_data = (ref_count, current_ref["Authors"], 
                              int(current_ref["Year"]),)
                # print(short_data)
                c1.execute('INSERT INTO ml1 VALUES (?, ?, ?)', short_data)
                con1.commit()
            elif line.startswith("<") == True:
                ref_count = ref_count + 1
            else:
                pass


except IOError as ioerr:
    print("Unable to read file: "+str(ioerr))
print("End of references.")

con1.close()

