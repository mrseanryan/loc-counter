# :memo: loc (Lines Of Code) counter

Counts how many lines of code are in a code base, by programming language.
The programming languages are determined via the file extensions.

## Dependencies

- Python 2.x

## Usage

```
./loc_counter.py
```

### Example output

```
Type            Files   Lines
Python          1       377

                Files   Lines
Identified Code         1       377

Skipped         2       75
Skipped extensions:             md


Total           3       452
```

### Detailed Usage

This script scans the current directory and reports several
statistics of interest to code spelunkers:

- total number of directories that contain code
- total number of files in all directories.
- total number of files in each of the following programming
  languages: 
  - SQL, .NET, C#, PowerShell, JavaScript, CSS, SCSS, JSON, ASP.NET, TypeScript.
  Also other languages including:
  - Awk, C, C++, HTML, IDL, Java, Perl, PHP, Java, Python, TCL, VB6.

The programming language is determined via the file extension(s).

The script automatically ignores any file in typical 'not source code' directories, such as `node_modules` or `.git`.

#### options

The -w or --where argument tells the program that for each type of
code it is to list all the directories that contain that type of code.

The -e or --exclude argument excludes certain sub-directories from the
search.  The exclude argument can be used several times on the same
line like this:

The -l or --language option says to only find one language, and not
all of them.

The -p or --pretty option allows the user to select HTML or LaTeX
table output format instead of plain text.

`
loc_counter.py -e HTML -e DoxyFiles
`

## origin

This is an updated version of `what.py` by George V. Neville-Neil.

The original version is here: http://www.codespelunking.org/downloads/what.py

## License

See the [original license](LICENSE) or the same text in the source file.
