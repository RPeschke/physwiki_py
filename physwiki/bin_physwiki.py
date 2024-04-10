from  physwiki.generic import physwiki_processors
from physwiki.generic import get_path_from_name
import argparse
import sys
import os
import pyConfigFiles as pcf 

from physwiki.physwiki_script_base_class import physwiki_script_base_class
import inspect


default_processors = [
    "zip_to_md",
    "adjust_title_level",
    "extract_header",
    "remove_formatting", 
    "do_picture_path_normalization", 
    "extract_eq", 
    "remove_line_endings", 
    "do_latex_to_text", 
    "replace_ref", 
    "standard_replacements"
]

def get_all_files_in_folder(folder_path):
    # Check if the path is a folder
    if os.path.isdir(folder_path):
        # Find all .py files in the folder
        py_files = [os.path.join(folder_path, f ) for f in os.listdir(folder_path) if f.endswith('.py')]
    else:
        py_files = []


    return py_files


def get_filename():
    caller_filepath = inspect.stack()[1].filename
    
    return os.path.dirname(caller_filepath) 


def main(debug_path = None):
    parser = argparse.ArgumentParser(description='physwiki')
    parser.add_argument('--md', help='Markdown File',default="2023 test")
    #parser.add_argument('--processors', help='List of Processors (can be empty)',default="None")
    parser.add_argument('--zip', help='zip file with the latex',default="None")    
    parser.add_argument('--std', help='standard replacements',default="replacements1.csv")    
    parser.add_argument('--script', help='script folder',default="None")    
    args = parser.parse_args()
    filename = get_path_from_name(args.md, debug_path ).replace("\\","/")
    filename = filename + "/" +args.md + ".md"
    #proc = default_processors if args.processors == "None" else args.processors.split(",")
    path = os.path.join(get_filename(), "./processors" )
    obj = physwiki_script_base_class()
    obj.add_modules(
        get_all_files_in_folder(path)
    )
    
    
    obj.add_modules(
        get_all_files_in_folder(args.script),
        os.getcwd()
    )

    obj.processors.sort(key=lambda x: x[0])

    for p in obj.processors:
        p[1](filename, args)
