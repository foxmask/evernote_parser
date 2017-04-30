Evernote Parser
===============

Split all Evernote notes in its own file from the our .enex file

Using:
-----
in the `settings.py` file, set the following parameters :

```python

# converting into this format
TO_FORMAT = 'markdown'
# file extension
TO_FORMAT_EXT = 'md'
# for the markdown H1 is #
HEADING1 = '# '

```

you could change the TO_FORMAT in any supported format by [Pandoc](http://pandoc.org/), for example you can choose in HTML etc
So the `HEADING1` would be set as `<h1>`


Once parsing is done:
---------------------
The files could me used as is without doing anything else. 
Or importing one by one, or with any script that will read them.


Requirements
------------

* python 3.6
* lxml 3.7.3
* pypandoc 1.3.3


How it works
------------
one folder is created by date, and note are created inside of them.
If (py)pandoc is not able to convert a note (because of the very heavy weight), a script will be created to manually run the conversion


([code based on this gist](https://gist.github.com/foxmask/7b29c43a161e001ff04afdb2f181e31c))
