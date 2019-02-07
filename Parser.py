'''
Created on Jan 29, 2019

@author: Kristen Tan
I pledge my Honor that I have abided by the Stevens Honor System. Kristen Tan
'''

import sys

VALID_TAGS = {"0":["INDI","FAM", "HEAD", "TRLR", "NOTE"],
              "1":["NAME", "SEX", "BIRT", "DEAT", "FAMC",
                   "FAMS","MARR", "HUSB", "WIFE", "CHIL", "DIV"],
              "2":["DATE"], "3":[], "4":[]}

def get_lines(arg_array):
    """Get the lines of a GEDCOM file and return them in a list"""
    try:
        with open(sys.argv[1], "r") as gedcom_file:   
            gedcom_lines = gedcom_file.readlines()
            return gedcom_lines 
    except FileNotFoundError:
        print("The file cannot be found.")
        sys.exit(1)

def check_line_validity(gedcom_line):
    """Check validity based on dictionary: if <tag> in VALID_TAGS[level]"""
    line_elements = gedcom_line.split()
    level = line_elements[0]
    if (line_elements[1].isupper()):
        tag = line_elements[1]
        arguments = "".join(line_elements[2:])
    else:
        tag = line_elements[2]
        arguments = line_elements[1]
    # Check if tag is valid for a given level
    level_validity = tag in VALID_TAGS[level]
    order_validity = True
    # Check if level, tag, and argument are in correct order
    if (tag == "INDI" or tag == "FAM"):
        if (line_elements[1] == "INDI" or line_elements[1] == "FAM"):
            order_validity = False
    return level_validity and order_validity
        
def parse_single_line(gedcom_line):
    """Generate the desired output for a single line"""
    print("--> " + gedcom_line.strip())
    # Now split line by spaces into elements
    line_elements = gedcom_line.split()
    # Get the level, tag, and args
    level = line_elements[0]
    if (len(line_elements) > 1):
        if (line_elements[1].isupper()):
            tag = line_elements[1]
            arguments = ""
            for word in line_elements[2:]:
                arguments += word + " "
        else:
            tag = line_elements[2]
            arguments = line_elements[1]
        if check_line_validity(gedcom_line):
            # if the line is valid
            print(f"<-- {level}|{tag}|Y|{arguments}")
        else:
            # if the line is NOT valid
            # only difference is we are printing an "N" here
            print(f"<-- {level}|{tag}|N|{arguments}")
    else:
        if level == "0" or level == "1" or level == "2":
            print(f"<-- {level}|Y|")
        else:
            print(f"<-- {level}|N|")
        
if __name__ == "__main__":
    file_lines = get_lines(sys.argv[1])
    for line in file_lines:
        parse_single_line(line)