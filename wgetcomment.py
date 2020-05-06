#!/usr/bin/env python3
import sys
import os
import requests
import re
import csv

USER_AGENT = 'wgetcomment 1.0'

def analyze_comment(comment):
  symbol_count = 0;
  for c in comment:
    if (ord(c) > 0x20 and ord(c) < 0x30) or (ord(c) > 0x39 and ord(c) < 0x41) or (ord(c) > 0x5A and ord(c) < 0x61) or (ord(c) > 0x7A and ord(c) < 0x7F):
      symbol_count += 1
  
  if len(comment) > 0:
    return symbol_count/ len(comment)
  else:
    return 0
  
def output(type, comments):
  if output.csvoutput:
    try:
      with open(output.filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for comment in comments:
          output.counter +=1
          
          csvwriter.writerow([output.counter, type, analyze_comment(comment), comment])
    except Exception as e:
      print("[-] Can not access to the file \"%s\"\n    Error:%s" % (output.filename, e))
      exit()
  else:
    for comment in comments:
      output.counter += 1
      print("[%s %3d]: %s" % (type.ljust(4), output.counter, comment.strip()))
output.counter=0

#.Get the URL from the command line argument
if len(sys.argv) < 2:
  print("usage: wgetcomment [url]\n       wgetcomment [url] [csvfilename]", file=sys.stderr)
  exit()
  
url=sys.argv[1]
if len(sys.argv) == 3:
  output.csvoutput = True
  output.filename = sys.argv[2]
  if os.path.exists(output.filename):
    print("[-] The file \"%s\" is already existing" % (output.filename))
    exit()
else:
  output.csvoutput = False
  filename = ""
  
#2.Fetch the contents from the URL
print("[+] Accessing to %s" % url, file=sys.stderr)
try:
  response=requests.get(url, headers={'User-agent': USER_AGENT})
except Exception as e:
  print("[-] An error is happening when accessing the URL:%s\n    %s" % (url, e), file=sys.stderr)
  exit()
  
if response.status_code >= 400:
  print("[-] An error is happening when accessing the URL:%s\n    Status code is %s." % (url, response.status_code), file=sys.stderr)
  exit()

contents = response.text

#3.Extract the comment
#html comment <!--  -->
print("[+] Extracting comments")
htmlcomments = re.findall("<!--(.*?)-->", contents, flags=re.DOTALL)

#js <script > </script> /* */, //
javascripts = re.findall("<script[^>]*>(.*?)</script>", contents, flags=re.DOTALL)
jscomments = []
for javascript in javascripts:
  jscomments += re.findall("/\*(.*?)\*/", javascript, flags=re.DOTALL)
  jscomments += re.findall("[^:'\"\\\\]//(.*)", javascript)

#css /* */
csss = re.findall("<style[^>]*>(.*?)</style>", contents, flags=re.DOTALL)
csscomments = [];
for css in csss:
  csscomments += re.findall("/\*(.*?)\*/", css, flags=re.DOTALL)

#4.Print the comment
output("HTML", htmlcomments)
output("JS", jscomments)
output("CSS", csscomments)
