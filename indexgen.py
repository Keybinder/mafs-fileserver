# HTML directory index generator
# Originally programmed March 2020 by Jonah Hopkin

# This program is designed to be run at the root directory of a web server. 
# It generates index.html pages for each and every directory/subdirectory recursively (with some hardcoded exceptions).
# Each index.html presents the user with a table that lists and links to all files in the directory it's in, as well as displays some metadata about them.
# It's basically a very crappy custom generator for those "open directories" you sometimes find on the web.
# This program expects a html template for the index and a txt template for the html for each row to be in the "HIDDEN" subdirectory.

import os
import time

with open("HIDDEN/index-template.html", 'r') as template:
	template_html = template.read()

with open("HIDDEN/table-row-template.txt", 'r') as infile:
	template_row = infile.read()
    
file_type_id = {
	".pdf" : "PDF",
	".txt" : "TXT"
}
file_type_desc = {
	".pdf" : "PDF File",
	".txt" : "Text Document"
}
spec_dir_icons = {
	"Biology" : "BIODIR",
	"Chemistry" : "CHYDIR",
	"English-Standard" : "EN1DIR",
	"English-Advanced" : "EN2DIR",
	"English-Extension" : "EN3DIR",
	"Mathematics-Standard" : "MM1DIR",
	"Mathematics-Advanced" : "MM2DIR",
	"Mathematics-Extension" : "MM3DIR",
	"Physics" : "PHYDIR"
}

def format_size(bytes):
	suffixes = ["B", "KiB", "MiB", "GiB"]
	suffix = 0
	while bytes > 1:
		bytes /= 1024
		suffix += 1
	bytes *= 1024
	suffix -= 1
	return "{:.1f}".format(bytes) + suffixes[suffix]

class IndexTemplate:
	# invariant -- self.htmlfile is a valid html file
	def __init__(self, path):
		# always initialise with absolute path
		self.htmlfile = template_html
		self.htmlfile = self.htmlfile.replace("$INDEXPATH", "/"+path)
		self.abs_base_path = path
	def add_row(self, file):
		fullpath = self.abs_base_path + file
		self.htmlfile = self.htmlfile.replace("<!-- $INSERTROW -->", template_row+"\n<!-- $INSERTROW -->")
		if os.path.basename(file) == "index.html":
			self.htmlfile = self.htmlfile.replace("$FILETYPEID", spec_dir_icons.get(os.path.dirname(file),"DIR"))
			self.htmlfile = self.htmlfile.replace("$FILETYPEDESC", "Directory")
			self.htmlfile = self.htmlfile.replace("$FILENAME", os.path.dirname(file))
		else:
			filename, fileext = os.path.splitext(fullpath)
			self.htmlfile = self.htmlfile.replace("$FILETYPEID", file_type_id.get(fileext, "UNK"))
			self.htmlfile = self.htmlfile.replace("$FILETYPEDESC", file_type_desc.get(fileext, "Unknown"))
			self.htmlfile = self.htmlfile.replace("$FILENAME", file)

		self.htmlfile = self.htmlfile.replace("$FILEPATH", file)
		self.htmlfile = self.htmlfile.replace("$LASTMODIFIED", time.strftime("%a %d %b %H:%M %Y", time.localtime(os.path.getmtime(fullpath))))
		self.htmlfile = self.htmlfile.replace("$FILESIZE", format_size(os.path.getsize(fullpath)))
	
def index_dir(cur_dir):
	index = IndexTemplate(cur_dir)
	for filename in os.listdir("./"+cur_dir):
		# hardcoding ignores because lazy
		fname, fext = os.path.splitext(filename)
		if fext == ".html" or fname == "HIDDEN" or filename == "indexgen.py":
			continue
		if cur_dir == "":
			if fname == "images" or fname == "styles" or fname == "scripts":
				continue
		if os.path.isdir(filename):
			index_dir(cur_dir+filename+"/")
			index.add_row(filename+"/index.html")
		else:
			index.add_row(filename)
	with open(cur_dir+"index.html", 'w', encoding="utf-8") as outfile:
		outfile.write(index.htmlfile)
	return

index_dir("")
