import argparse
import re
from physwiki.md_reference_updater import md_reference_updater
from physwiki.md_transform_headlines import transform_headlines
from physwiki.generic import load_file, save_file
from physwiki.md_pyMarkdown import md_pyMarkdown   


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from datetime import datetime

# Get the current time


# Assuming your script is named update_figures.py and is in the same directory
#from update_figures import process_file

last_processed = {}

figure_updaters = [ 
    md_reference_updater(reference_type="figure", display_str="Figure ", display_ref_str="Figure "),
    md_reference_updater(reference_type="table", display_str="Table ", display_ref_str="Table "),
    md_reference_updater(reference_type="sector", display_str="", display_ref_str="Sector "),
    transform_headlines()
]


        

def update_file(path):
    content = load_file(path)
    for up in figure_updaters:
        content = up.process_file(content)

    save_file(path,  content)

class MarkdownUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if the modified file is a Markdown file
        if event.is_directory:
            return
        if not event.src_path.endswith('.md'):
            return
        
        last = last_processed.get(event.src_path)
        if last is not None and (datetime.now() - last).seconds < 1:
            return
        print(f"Markdown file changed: {event.src_path}")
        try:
            update_file(event.src_path)


            last_processed[event.src_path]  =  datetime.now()
            print(f"Processed updated file: {event.src_path}")
        except Exception as e:
            print(f"Error processing file {event.src_path}: {e}")


def start_monitoring(path='.'):
    event_handler = MarkdownUpdateHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitoring folder: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser(description='physwiki')
    parser.add_argument('--md', help='Markdown File',default="None") 
    parser.add_argument('--path', help='Markdown File',default="None") 
    parser.add_argument('--py', action='store_true', help='switches on python mode')

    
    args = parser.parse_args()

    if args.py:
        figure_updaters.clear()
        figure_updaters.append(
            md_pyMarkdown()
        )


    if args.md != "None":
        update_file(args.md)
        return 

    if args.path != "None":
        pwd = args.path if args.path != "." else os.getcwd()
        start_monitoring(pwd)
        return 
    
    print("no Argument was provided")

    



main()