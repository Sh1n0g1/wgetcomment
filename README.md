# wgetcomment
A tool to collect comments from websites

# How to use
## Print the result
python3 wgetcomment.py url
## Save the result in csv
python3 wgetcomment.py url csvfilename

# Features
1. Get the URL from the command line argument
2. Fetch the contents from the URL
3. Extract the comment
4. Print the comment

![Example](https://github.com/Sh1n0g1/wgetcomment/raw/master/example.png "Example")


![CSVExample](https://github.com/Sh1n0g1/wgetcomment/raw/master/csvexample.png "CSV Example")
The symbol rate means how many percent of comments are symbols.  
This number indicates wether the comment is a source code or a human comment.
Less than 10% are human comments, but it depends on the website.

