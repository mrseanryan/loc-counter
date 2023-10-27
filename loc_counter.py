#!/usr/bin/env python
#
# File: $Id: what.py,v 1.11 2006/04/28 11:00:52 gnn Exp $
#
# Copyright (c) 2005, Neville-Neil Consulting
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# Neither the name of Neville-Neil Consulting nor the names of its 
# contributors may be used to endorse or promote products derived from 
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author: George V. Neville-Neil
#
# URL: http://www.codespelunking.org/downloads/what.py
#
# Description: This python script will recursively descend a source
# tree and print out several relevant statistics



"""This script is  meant to be run the first time  you encounter a new
source base.  It recursively descends  a file tree and reports several
statistics of interest to code spelunkers.  These include:

- The total number of directories that contain code
- The total number of files in all directories.
- The total number of files in each of the following programming
  languages: Awk, C, C++, HTML, IDL, Java, Perl, PHP, Java, Python, TCL

The code that determines what computer language a file contains is
flexible in how it does its checking.  Right now this is done based on
the file's extension, but can be extended to call an interpreter to
determine if the file is valid code of a particular type.

There are two arguments that can be used.

The -w or --where argument tells the program that for each type of
code it is to list all the directories that contain that type of code.

The -e or --exclude argument excludes certain sub-directories from the
search.  The exclude argument can be used several times on the same
line like this:

The -l or --language option says to only find one language, and not
all of them.

The -p or --pretty option allows the user to select HTML or LaTeX
table output format instead of plain text.

loc_counter.py -e HTML -e DoxyFiles

The program automatically ignores any file in a CVS diretory.
"""

import os
from os import F_OK

import mimetypes # help to avoid parsing binary files

unknownExtensions = []

# This is the file extension mapping code.  Change this array if you
# wish to change the determination of the files.  The format is "key",
# "value" in which the key is the extension and the value is the file
# type.  Both the key and value are strings.
def filetype(name):

    file_ext_map = { "awk" : "AWK",
                     "p" : "Perl",
                     "py" : "Python",
                     "pyl" : "Python",
                     "el" : "Emacs Lisp",
                     "elc" : "Emacs Lisp",
                     "scala" : "Scala",
                     "rs" : "Rust",
#                    ### C++ ###
                     "h" : "C or C++ Header",
                     "hpp" : "C or C++ Header",
                     "c" : "C",
                     "cc" : "C++",
                     "cpp" : "C++",
                     "c++" : "C++",
                     "m" : "Objective C",
#                    ### END C++ ###
                     "tcl" : "TCL",
                     "html" : "HTML",
                     "htm" : "HTML",
                     "java" : "Java",
                     "idl" : "Interface Definition Language",
                     "xml" : "XML",
                     "xsl" : "XML",
                     "php" : "PHP",
                     "inc" : "PHP include",
                     "sh" : "Shell Script",
                     "ksh" : "Shell Script",
                     "bash" : "Shell Script",
                     "csh" : "Shell Script",
                     "tcsh" : "Shell Script",
                     "mk" : "Makefile",
                     "am" : "Automake",
                     "m4" : "M4",
#                    ### SQL ###
                     "sql" : "SQL",
#                    ### VB6 ###
                     "frm" : "VB6",
                     "bas" : "VB6",
                     "cls" : "VB6",
#                    ### .NET ###
                     "config" : "config",
                     "cs" : "C#",
                     "rc" : "VS Resource",
                     "xaml": "XAML file",
#                    ### Powershell ###
                     "ps1" : "Powershell",
                     ### Web ###
                     "css" : "CSS",
                     "sass": "SASS",
                     "scss": "SCSS",
                     "js" : "JavaScript",
                     "json" : "JSON",
                     "asax" : "ASP.NET handler",
                     "ashx" : "ASP.NET handler",
                     "aspx" : "ASP.NET page",
                     "ascx" : "ASP.NET user control",
                     "cshtml" : "MVC View Razor",
                     "ts": "TypeScript"
                     }

    file_name_parts_to_skip = [ "ai.0.", "bootstrap.", "jquery.", "jquery-", "modernizr", ".min.js",  ".min.css", "\\Lib\\", "\\External\\", "ASPxScriptIntelliSense.js", "jquery", "\\packages\\", "\\node_modules\\", "Silverlight.js", "\\bower_components\\", "\\tmp\\", "\\temp\\", ".git" ]

    binary_mime_types = [ "application/octet-stream", "application/pdf" ]
    binary_mime_type_parts = [ "application/vnd" ]

    (root, extension) = os.path.splitext(name)

    # Special case the search for Makefiles as these are important but
    # do not have an extension
    if (len(extension) <= 0):
        if (root == "Makefile"):
            return "Makefile"
        else:
            if (root == "configure"):
                return "Autoconf"
            else:
                return "Unknown"

    for exclude in file_name_parts_to_skip:
        if exclude.lower() in name.lower():
            return "Excluded:file_name_part"

    mime = mimetypes.guess_type(name)
    if (mime[0] is not None and mime[0] in binary_mime_types) or mime[1] == 'gzip':
        return "Excluded:mime-binary"
    for exclude in binary_mime_type_parts:
        if mime[0] is not None and mime[0] in exclude:
            return "Excluded:mime:binary-part"

    # According to the rules if we have an extension then it ALWAYS has
    # a . at the beginning.  Strip that .
    extension = extension[1:len(extension)]
    if (extension not in file_ext_map):
        if not extension in unknownExtensions:
            unknownExtensions.append(extension)
        return "Unknown"

    return file_ext_map[extension]

# Find out how many lines are in a file.
# We know that "name" is a file because it was passed to us by
# os.walk() in main().

def filelines(name, encoding):
    try:
        file = open(name, 'r', encoding=encoding)
    except:
        return -1
    lines = file.readlines()
    file.close()
    return len(lines)

def main():

    file_map = {} # The map of file type to the number that exist.
    size_map = {} # The map of file type to the number of lines.
    location_map = {} # A map of the file type to a list of directories
    dir_num = 0 # How many directories are there?
    exclude_list = [] # List of directories to exclude, can be empty
    
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-c", "--encoding", action="store", type="string",
                      default = "utf-8", dest="encoding",
                      help="The file encoding to use when reading (default is utf-8)")
    parser.add_option("-e", "--exclude", action="append", default=[],
                      dest="exclude_dir", help="Directory to exclude")
    parser.add_option("-l", "--language", action="store", type="string",
                      dest="language",
                      help="Find only code of a particular language")
    parser.add_option("-p", "--pretty", action="store", type="string",
                      dest="pretty",
                      help="Pretty print in HTML or LaTeX table format")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Verbose output")
    parser.add_option("-w", "--where",
                      action="store_true", dest="where", default=False,
                      help="Print where files are located")
    
    (options, args) = parser.parse_args()

    where = options.where
    exclude_list_default = [ "$tf", ".git", ".hg", "coverage", "External", "apps_out", "bin", "bower_components", "css_out", "dist", "jquery", "js_out", "lib", "node_modules", "obj", "packages", "published", "temp", "tmp", "typings" ]
    exclude_list = exclude_list_default + options.exclude_dir
    language = options.language
    pretty = options.pretty
    extensions_to_always_skip = [".png", ".gif", ".jpg", ".jpeg", ".bmp", ".mpr", ".zip", ".tar", ".jar", ".gz", ".ico", ".eot", ".docx"]

    for root, dirs, files in os.walk("."):
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories

        if exclude_list:
            dirsLower = []
            for dir in dirs:
                dirsLower.append(dir.lower())
            #print "dirs: " + ",".join(dirs)
            #print "excluded dirs:" + ",".join(exclude_list)
            for dir in exclude_list:
                if dir.lower() in dirsLower:
                    i = dirsLower.index(dir.lower())
                    if(options.verbose):
                        print("excluding: " + dir.lower() + " at " + str(i))
                    dirsLower.remove(dirsLower[i])
                    dirs.remove(dirs[i])
            #print "dirs after exclude: " + ",".join(dirs)

        for name in files:
            fullname = os.path.join(root, name)
            if not os.access(fullname, F_OK):
                continue
            type = filetype(fullname)

            #print (f"{fullname} - [{type}]")

            # Avoid trying to read binary files
            (root2, extension2) = os.path.splitext(name)
            if extension2.lower() in extensions_to_always_skip or type.startswith("Excluded") or type == "Unknown":
                if(options.verbose):
                    print(f"excluding: {fullname} [type = {type}]")
                continue

            if options.verbose:
                mime = mimetypes.guess_type(name)[0]
                print(f"{fullname} [{mime}]")

            if (language and (type != language)):
                continue

            if type not in file_map:
                file_map[type] = 1
            else:
                file_map[type] += 1
            lines = filelines(fullname, options.encoding)

            if lines == -1:
                continue

            if type not in size_map:
                size_map[type] = lines
            else:
                size_map[type] += lines

            if type == "Unknown":
                continue
            
            if type not in location_map:
                location_map[type] = {root : 1}
                dir_num += 1
                continue

            if root not in location_map[type]:
                location_map[type][root] = 1
                dir_num += 1
                continue
            
            location_map[type][root] += 1
            dir_num += 1
            
    # Now do our fancy printing
    if (pretty == "HTML"):
        print("<table><tr><td>Type</td><td>Number</td><td>Lines</td></tr>")
    elif (pretty == "LaTeX"):
        print("\\begin{tabular}{|l|l|c|}\n\\hline\nType & Number & Lines\\\\\n\\hline")
    else:
        print("Type\t\tFiles\tLines")

    types = file_map.keys()
    types = sorted(types)

    total_files = 0
    total_lines = 0

    for key in types:
        if key == "Unknown":
            continue
        total_files += file_map[key]
        total_lines += size_map[key]

        if (pretty == "HTML"):
            print("<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % \
                  (key, file_map[key], size_map[key]))
        elif (pretty == "LaTeX"):
            print("%s & %d & %d\\\\" % (key, file_map[key], size_map[key]))
        else:
            print("%s\t\t%d\t%d" % (key, file_map[key], size_map[key]))
        
        if (where == True):
            dirs = location_map[key].keys()
            dirs.sort()
            for dir in dirs:
                if (pretty == "HTML"):
                    print("<tr><td>%s</td><td>%d</td></tr>" % \
                          (dir, location_map[key][dir]))
                elif (pretty == "LaTeX"):
                    print("%s&%d\\\\" % (dir, location_map[key][dir]))
                else:
                    print("\t%s\t%d" % (dir, location_map[key][dir]))

    if (pretty == "HTML"):
        print("</table><br>")
        print("<table>")
        print("<tr><td></td><td>Files</td><td>Lines</td></tr>")
        print("<tr><td>Identified Code</td><td>%d</td><td>%d</td></tr>" % \
              (total_files, total_lines))
    elif (pretty == "LaTeX"):
        print("\\hline \\hline\n&Files & Lines\\\\")
        print("Identified Code & %d & %d\\\\" % (total_files, total_lines))
    else:
        print("\n\t\tFiles\tLines")
        print("Identified Code\t\t%d\t%d\n" % (total_files, total_lines))

    if "Unknown" in file_map.keys() and "Unknown" in size_map.keys():
        if (pretty == "HTML"):
            print("<tr><td>Unknown</td><td>%d</td><td>%d</td></tr>" % \
                  (file_map["Unknown"], size_map["Unknown"]))
        elif (pretty == "LaTeX"):
            print("Skipped & %d & %d\\\\\n\\hline" % \
                  (file_map["Unknown"], size_map["Unknown"]))
        else:
            print("Skipped\t\t%d\t%d" % \
                (file_map["Unknown"], size_map["Unknown"]))
            unknownExtensions.sort()
            print("Skipped extensions:\t\t" + ", ".join(unknownExtensions))
            print("\n")
        total_files += file_map["Unknown"]
        total_lines += size_map["Unknown"]

    if (pretty == "HTML"):
        print("<tr><td>Total</td><td>%d</td><td>%d</td></tr>" % \
              (total_files, total_lines))
    elif (pretty == "LaTeX"):
        print("Total & %d & %d\\\\\\hline" % (total_files, total_lines))
    else:
        print("Total\t\t%d\t%d\n" % (total_files, total_lines))

    if (where == True):
        if (pretty == "HTML"):
            print("<tr><td>Number of directories</td><td>%d</td></tr>" % \
                  dir_num)
        elif (pretty == "LaTeX"):
            print("Number of directories & %d" % dir_num)
        else:
            print("Number of directories\t%d" % dir_num)

    if (pretty == "HTML"):
        print("</table>")
    elif (pretty == "LaTeX"):
        print("\\end{tabular}")
        
main()        
