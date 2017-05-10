def find_author_medline(medline_file):
    """Finds the start of "Author" fields in Medline text files, and constructs
an author list in a consistent format, which can be used to construct an
instance of the Reference class. Assumes UTF-8 coding for the input file."""
    
    try:
        with open(medline_file) as f:
            for line in f:
                if "Authors" in line:
                    authorlist = []
                    au = f.readline()
                    au = au.strip()
                    authorlist = au.split(".")
                    authorlist_clean = []
                    try:
                        for item in authorlist:
                            if item != "\n":
                                item = item.strip()
                                authorlist_clean.append(item)
                        print(authorlist_clean)
                    except ValueError as verr:
                        print("Endline not found:" + str(verr))
    except IOError as ioerr:
          print("File not found:" + str(ioerr))


def find_author_embase(embase_file):
    """Finds the start of "Author" fields in Medline text files, and constructs
an author list in a consistent format, which can be used to construct an
instance of the Reference class. Assumes UTF-8 encoding in the input file.
Similar to the Medline version, but with EMBASE delimiters."""

    try:
        with open(embase_file) as f:
            for line in f:
                if "Authors" in line:
                    au = f.readline()
                    au = au.strip()
                    author_list=""
                    # Remove all full-stops from the author list string.
                    for char in au:
                                if char != ".":
                                    author_list = author_list + char
                                else:                                
                                    pass
                    # Split at spaces.
                    au_blocks = author_list.split(" ")
                    authorlist_clean = []
                    for block in au_blocks:
                        if block.isupper() == False:
                            surname = block
                            name_flag=True
                            continue
                        else:
                            initials = block
                            name = surname + " " + initials
                            authorlist_clean.append(name)

                    print(authorlist_clean)


                            
        authorlist = au.split(".")
        authorlist_clean = []
                
    except IOError as ioerr:
        print("File not found:" + str(ioerr))

    return authorlist_clean




def find_author_central(central_file):
    """Reads the author fields from a CENTRAL text file and uses them to
assemble an author list in standard format, which can be used to construct an
instance of the Reference class.  Assumes iso-8859-15 (Western) coding in the
input file."""

    try:
        with open(central_file, encoding="iso8859_15") as f:
            authorlist_clean = []
            for line in f:
                if line.startswith("AU:"):
                    authorlist_clean.append(line.strip("AU:").strip())
                elif authorlist_clean != []:
                    print(authorlist_clean)
                    authorlist_clean = []
                else:
                    pass
`                    
            #print(authorlist_clean)
    except IOError as ioerr:
        print("Error: can't find file" + str(ioerr))
                            



find_author_medline("Medline_3refs.txt")
print()
find_author_embase("embase1.txt")
print()
find_author_central("Clonidine_CENTRAL.txt")
