#!/usr/bin/env python

#custom self-containment-------------------------------
#ensure running as file
try:
    __file__
except NameError:
    raise AssertionError("Epic Fail")

#imports
from os import path
import sys
import site

#setting absolute base_path - should be git repo
site_path = path.dirname( path.dirname( path.abspath(__file__) ) )
# paths:    git repo        <- pongking      <- settings.py

#load custom lib first by clearing sys.path, then reloading @ end
sys_path  = sys.path                        #hold temp
sys.path = []                               #clear
site_path = path.join(site_path, 'lib')     #set local
site.addsitedir(site_path)                  #add to list
sys.path.extend(sys_path)                   #add back all others

#back to your regularly scheduled programming-----------
from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
