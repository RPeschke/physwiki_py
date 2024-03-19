import argparse
import os
import re
from collections import Counter
# This dictionary will map identifiers to figure numbers

class md_reference_updater:
    def __init__(self, reference_type, display_str, display_ref_str) -> None:
        self.reference_type = reference_type
        self.diplay_type = display_str
        self.diplay_type_ref = display_ref_str
        self.identifier_to_figure = {}
        # Pattern for initial figure declarations
        
        self.declaration_pattern = fr'\[([^\]]*)\]\s*\((#\w+@{self.reference_type}@new)\)'
        self.reference_pattern = fr'\[([^\]]*)\]\s*\((#\w+@{self.reference_type})\)'
        
        self.identifier_pattern = fr'\(#(\w+@{self.reference_type}@new)\)'

        self.ref_suffix = f'@{self.reference_type}'
        self.dec_suffix = f'@{self.reference_type}@new'

        #self.declaration_pattern = r'\[([^\]]*)\]\s*\((#\w+@figure@new)\)'
        
        # Pattern for figure references that need updating
        #self.reference_pattern = r'\[([^\]]*)\]\s*\((#\w+@figure)\)'



    def check_for_duplicate_identifiers(self, content):
        # Pattern to find all figure:new and figure identifiers
        identifiers = re.findall(self.identifier_pattern, content)
        
        # Count occurrences of each identifier
        identifier_counts = Counter(identifiers)
        
        # Find duplicates
        duplicates = [identifier for identifier, count in identifier_counts.items() if count > 1]
        return duplicates


    def update_figure_declarations_and_collect_identifiers(self, content):
        # Counter for figure numbers
        figure_count = 1

        def declaration_replacer(match):
            nonlocal figure_count
            identifier = match.group(2)  # Extract the identifier
            new_text = f"{self.diplay_type}{figure_count}"
            self.identifier_to_figure[identifier] = figure_count  # Map identifier to figure number
            figure_count += 1
            return f"[{new_text}]({identifier})"

        # Update figure declarations and collect identifiers
        updated_content, _ = re.subn(self.declaration_pattern, declaration_replacer, content)
        return updated_content

    def update_figure_references(self, content):
        def reference_replacer(match):
            identifier = match.group(2)  # Extract the identifier
            # Replace with the corresponding figure number, keep original identifier
            new_figure_count = self.identifier_to_figure.get(identifier.replace(self.ref_suffix, self.dec_suffix), -1)
            
            return f"[{self.diplay_type_ref}{new_figure_count}]({identifier})"

        # Update figure references based on collected identifiers
        updated_content, _ = re.subn(self.reference_pattern, reference_replacer, content)
        return updated_content

    def process_file(self, content):
        duplicates = self.check_for_duplicate_identifiers(content)
        if duplicates:
            print(f"Error: Duplicate identifiers found: {', '.join(duplicates)}")
            return content
        
        # Update figure declarations and collect identifiers
        content = self.update_figure_declarations_and_collect_identifiers(content)
        
        # Update references to those figures
        content = self.update_figure_references(content)

        return content
        

def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        return content
    

def save_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    


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
]

def transform_headlines(content):
    # Define a pattern that matches the headlines with identifiers and optional classes
    pattern = r'^(#+\s.*?)(\s*\{#.*?\})(\s*\..*?)?$'
    
    # Replace the matched headlines with just the text part (group 1 captured by the pattern)
    transformed_content = re.sub(pattern, r'\1', content, flags=re.MULTILINE)
    
    return transformed_content

def update_file(path):
    content = load_file(path)
    for up in figure_updaters:
        content = up.process_file(content)
    
    content = transform_headlines(content)

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
    
    args = parser.parse_args()
    if args.md != "None":
        update_file(args.md)
        return 

    if args.path != "None":
        pwd = args.path if args.path != "." else os.getcwd()
        start_monitoring(pwd)
        return 
    
    print("no Argument was provided")

    



main()