#!/usr/local/bin/python3

import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

keep_heic = (sys.argv.count("--keep-heic") > 0)

class ConvertNewHeicToJpg(FileSystemEventHandler):
    def on_created(self, event):
        super().on_created(event)

        path = event.src_path
        file_extension = path.split(".")[-1]

        if event.is_directory or (file_extension != "HEIC" and file_extension != "heic"): 
            print("Ignoring " + path)
            return
        
        # handle if the path has spaces in the file name
        path = "\"" + path + "\""

        print("Converting " + path)
        cmd = "heic-to-jpg "
        if(keep_heic):
            cmd += "--keep "
        cmd += "-s " + path
        os.system(cmd)

        if(not(keep_heic)):
            os.remove(path)
            print("Removed " + path)

if __name__ == "__main__":
    paths = []

    if(len(sys.argv) == 1):
        keep_heic = True
        paths.append("/Users/haricharan/Downloads")
    else:
        for i in range(1, len(sys.argv)):
            if(sys.argv[i] != "--keep-heic"):
                paths.append(sys.argv[i])
        
        if(len(paths) == 0):
            paths.append(".")

    for path in paths:
        event_handler = ConvertNewHeicToJpg()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()