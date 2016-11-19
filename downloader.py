#!/usr/bin/python
import MySQLdb
import shutil
import os
import codecs
import sys
import copy
import datetime

from dbvariables import *

# connect to mysql db hidden in dbvariables.py file
db = MySQLdb.connect(host=host,     # ex: my-site.com
                     user=user,     # ex: root
                     passwd=passwd, # ex: your root password
                     db=db)         # ex: wordpress_mysite

def to_snake_case(input_str, output_glue_char="_"):
    chars_to_remove = [' ', '-', '?', ':', '&', '%', '!', '_']
    _string = input_str
    for single_char in chars_to_remove:
        _string = _string.replace(single_char, output_glue_char)
    _array = _string.split(output_glue_char)
    _array = filter(None, _array)
    return output_glue_char.join(_array).lower()

# dupa = to_snake_case("Lagiewniki-dlA_nowergo prezesa.md")
# print dupa
# sys.exit()

def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + "".join(x.title() for x in components[1:])

def pelican_meta_info(title="", date="", modified="", status="", category="", tags="", summary=""):
    str="""Title:      %s
Date:       %s
Modified:   %s
Status:     %s
Category:   %s
Tags:       %s
Summary:    %s
""" % (title, date, modified, status, category, tags, summary)
    return str

cursor = db.cursor()

# execute SQL select statement
cursor.execute("set names 'utf8'") # properly read files encod from DB
cursor.execute("SELECT * FROM wp_posts")

# commit your changes
db.commit()

# get the number of rows in the resultset
numrows = int(cursor.rowcount)

# get and display one row at a time.
posts_dir = './posts'
if os.path.exists(posts_dir):
    print "remove previous " + posts_dir + " dir"
    shutil.rmtree(posts_dir)
os.makedirs(posts_dir)

print "importing files "
for x in range(0, numrows):
    row = cursor.fetchone()
    # every row number have its equivalent in the data base
    d = str(row[2])
    # _filename = to_snake_case('posts/' + row[5] + "(" + d + ').md')
    _filename = to_snake_case('posts/' + row[5] + '.md')
    _filename = _filename.strip('_')
    with open(_filename, 'w') as file_:
        file_.write(pelican_meta_info(row[5], row[2], row[3], row[7]))
        file_.write(row[4])
    sys.stdout.write('.')

print "\nDone :)"
