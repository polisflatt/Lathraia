import os
import sys
import json
import time
import datetime

from conf import *

def main():
    # Obtain the JSON file of choice.
    json_file = open(sys.argv[1], "r").read()
    json_file_obj = json.loads(json_file)

    # Iterate
    for iteration in json_file_obj:
        try:
            # Set the variables up
            window_name = iteration["windowname"] # The window name at that time
            window_proc_name = iteration["procname"] # The window's process name at that time
            keys = iteration["keys"] # The actual keys captured
            _time = int(iteration["time"]) # The UNIX Timestamp for reference at the beginning
            
            # Print them while abiding with the described format.
            print(keylog_format.format(
                window_name = window_name,
                window_proc_name = window_proc_name,
                keys = keys,
                time = datetime.datetime.fromtimestamp(_time)
            ))
        except:
            pass



if __name__ == "__main__":
    main()