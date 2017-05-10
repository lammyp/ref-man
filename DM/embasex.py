"""This is a prototype program designed to read lines from an EMBASE .txt file,
determine where the records start, and assign the data for each record to an 
entry in a dictionary (EMRef). 
The title string in EMBASE is not surrounded by square brackets, so the 
'squ_bracket_check' function that appears in Medline_extract.py is not needed here. 
Author initials are presented with full stops following each initial character; 
hyphens are frequently used for dual foreign given names; these need to be parsed 
appropriately and converted to the common format (initials in a contiguous string, 
with punctuation marks removed.""" 



def split_embase_source(so_field):
    """This function takes the complete field under "Source" from the 
    Medline file and splits it into its component parts, returning these as a
    dictionary."""

    (journal, pub_data) = so_field.split(".", 1)
    journal = journal.strip()
    pub_data = pub_data.strip()
    print(journal+'\n'+pub_data)
    if not pub_data.startswith("Conference"):
        (pub_data_core, pub_date) = pub_data.split(".", 1)
        print(pub_data_core+'\n'+pub_date)
    else:
        pub_data=pub_data.replace('var.pagings', 'var pagings')
        pub_data=pub_data.replace('SUPPL.', 'SUPPL')
        print(pub_data)
        (confname, confdates, confpub, pub_data_core, pub_date)=pub_data.split('.',4)
    (vol_issue, pages_year) = pub_data_core.split(" (pp ")
    (volume, issue)=vol_issue.split(' (')
    issue = issue.strip(')')
    (pages, year)=pages_year.split('), ')
    if '-' in pages:
        (start_page, endpg)=pages.split('-')
    else:
        start_page=pages

    source_parts = {"journal":journal, "volume":volume, "issue":issue, 
                     "pages":pages, "year":year}
    return source_parts


from sys import argv
import sqlite3

script, input_file = argv

# Create a connection object to the database, ref1.db:
con1 = sqlite3.connect('ref1.db')
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
                # Using '. ' as the separator for the split method removes only 
                # the '.' from the last initial and leaves the initials and 
                # surname together:
                author_list = au.split(". ")
                # Now remove the remaining '.'s and '-'s from the initials and call
                # the new list 'author_list_clean':
                author_list_clean = []
                for author in author_list:
                    author_clean = author.replace('.', '').replace('-', '')
                    author_list_clean.append(author_clean)
                print(author_list_clean)
                # Currently it is necessary to pass the author list to sqlite3 
                # as a string; this should be modified to pass the list just
                # created. The following 4 lines form the string:
                author_string = '' 
                for item in author_list_clean:
                    author_string = author_string +'  '+ item.strip()
                current_ref["Authors"] = author_string
            # Return the title as a string, with external square brackets removed 
            # in the case of foreign language references:
            elif line.startswith("Title") == True:
                ti=f.readline().strip()
                current_ref["Title"]=ti
            # Return the components of the source data:
            elif line.startswith("Source") == True:
                source = f.readline()
                current_ref["Source"] = source
                current_ref["pubdata"] = split_embase_source(source)
                current_ref["Journal"] = current_ref["pubdata"]["journal"]
                current_ref["Year"] = current_ref["pubdata"]["year"]
                current_ref["Volume"] = current_ref["pubdata"]["volume"]

            # Presently the best (least worst) way of signalling the end of a 
            # reference in EMBASE is by finding the "Publication Type", which is
            # the last field in each reference.  The "<" character that leads 
            # the next reference could be used, but then there would be nothing
            # to signal the program to output the results from the last record,
            # as there is no "<" at the very end of the file.  This portion of 
            # the code may change when I find a better solution:

            elif "Publication Type" in line: 
                # print(current_ref, "\n")
                ref_data = (current_ref["Index"], current_ref["Authors"], 
                            current_ref["Journal"], current_ref["Year"], 
                            current_ref["Title"])
                print(ref_data)
                short_data = (ref_count, current_ref["Authors"], 
                              int(current_ref["Year"]),)
                print(short_data)
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

