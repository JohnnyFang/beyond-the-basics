import sys
import reader
'''
 to run this you can do while being under working-with-paths and run:
 python reader reader\__init__.py
'''

r= reader.Reader(sys.argv[1])
try:
    print(r.read())
except:
    pass
