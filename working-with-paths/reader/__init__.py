from reader.reader import Reader
"""
without importing Reader here to use it you would have to use the ugly:

import reader.reader
r = reader.reader.Reader('my_file.extension')
r.read()

but now you could just do:

import reader
r = reader.Reader('my_file.extension')
r.read()

"""
