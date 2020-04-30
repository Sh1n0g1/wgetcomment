#! python3
import sys
import requests
import re

#1.Get the URL from the command line argument
if len(sys.argv) < 2:
  print("Usage: wgetcomment <url>")
  exit()
  
url=sys.argv[1]

#2.Fetch the contents from the URL
try:
  result=requests.get(url)
except:
  print("An error is happening when accessing the URL:" + url)
  exit()
  
if result.status_code >= 400:
  print("An error is happening when accessing the URL:%s\nStatus code is %s." % (url, result.status_code ))
contents=result.text

#3.Extract the comment
#html comment <!--  -->
comments=re.findall("<!--(.*?)-->", contents, flags=re.DOTALL)

#4.Print the comment
for comment in comments:
  print("[HTML]: " + comment)
