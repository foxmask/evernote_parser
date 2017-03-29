Evernote Parser
===============

Split all Evernote notes in its own file from the our .enex file 


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
