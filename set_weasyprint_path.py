"""
    sitecustomize.py
    ================

    To ensure the correct GTK3 Runtime

    - To activate the GTK for Anaconda and all its environments:
      put the file into **sys.base_prefix**,
      i.e. the path where Anaconda's master python.exe is located.
      i.e. your Anaconda install directory

    - To activate the GTK only in a dedicated environment:
      put the file into the **./Lib/site-packages** folder of that
      environemt
"""
import os

# insert the GTK3 Runtime folder at the beginning
GTK_FOLDER = r'C:\Program Files\GTK3-Runtime Win64\bin'
os.environ['PATH'] = GTK_FOLDER + os.pathsep + os.environ.get('PATH', '')
