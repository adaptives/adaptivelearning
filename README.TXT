==========
Adaptive Learning Online
==========
An application to manage open courses and interactions within the courses

==========
Installation
==========
1. Download and install django 1.1
2. Download and install Markdown version 2.0.1 available for download from http://pypi.python.org/pypi/Markdown
3. Download django-markitup 0.2.8 (available at https://code.launchpad.net/django-markitup, or http://pypi.python.org/pypi/django-markitup/0.2.8) and put it on the PYTHONPATH
4. Download adaptivelearning and make sure the directory containing it (as well as adaptivelearning) is in the PYTHONPATH
5. Comment out the height and width preferences for .MarkItUpEditor (this is causing the question title textbox to have a large height even though it should only be 1 line)
6. Create a symlink to django-markitup/markitup/media/markitup from site-media/ma


