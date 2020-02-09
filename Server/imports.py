# This is the main imports folder!
# If you want to add your plugin to the system, you must address it here!
# Please do not import like corelib -- or at least make your functions non-ambiguous!
# Interference between functions will fuck up the program!

# Also, if you are running any non-standard plugin on a machine that is yours, beware!
# This is because a plugin could have additional malware on it. You have been warned.

# C would have been a much better choice.
# Python is horrible when trying to make clean directory and library systems!

from configuration import *
from constants import *
from functions import *

def dprint(text):
    """ Function for printing debug information """
    if not SHOW_DEBUG:
        return
    print('@DEBUG: ', text)

# To import
_imports = [
    "configuration",
    "constants",
    "functions.corelib.misc",
    "functions.corelib.io",
    "functions.corelib.os",
]

for item in _imports:
    try:
        exec("from {_import} import *".format(_import = item))
    except Exception as err:
        print(str(err))

