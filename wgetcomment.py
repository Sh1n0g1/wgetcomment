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
  exit()
  
contents=result.text

#3.Extract the comment
#html comment <!--  -->
htmlcomments=re.findall("<!--(.*?)-->", contents, flags=re.DOTALL)

#js <script > </script> /* */, //
javascripts=re.findall("<script[^>]*>(.*?)</script>", contents, flags=re.DOTALL)

jscomments=[]
for javascript in javascripts:
  jscomments += re.findall("/\*(.*?)\*/", javascript, flags=re.DOTALL)
  jscomments += re.findall("[^:'\"\\\\]//(.*)", javascript)

#css /* */
csss=re.findall("<style[^>]*>(.*?)</style>", contents, flags=re.DOTALL)
csscomments=[];
for css in csss:
  csscomments+=re.findall("/\*(.*?)\*/", css, flags=re.DOTALL)


#4.Print the comment
if htmlcomments:
  for htmlcomment in htmlcomments:
    print("[HTML]: " + htmlcomment.strip())

if jscomments:
  for jscomment in jscomments:
    print("[JS  ]: " + jscomment.strip())

if csscomments:  
  for csscomment in csscomments:
    print("[CSS ]: " + csscomment.strip())
