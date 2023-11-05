from  physwiki.generic import physwiki_processors
from physwiki.generic import get_path_from_name
import argparse
import sys




default_processors = [
    "zip_to_md",
    "adjust_title_level",
    "extract_header",
    "remove_formatting", 
    "do_picture_path_normaliztion", 
    "extract_eq", 
    "remove_line_endings", 
    "do_latex_to_text", 
    "replace_ref", 
    "standard_replacements"
]


def main(debug_path = None):
    parser = argparse.ArgumentParser(description='physwiki')
    parser.add_argument('--md', help='Markdown File',default="2023 test")
    parser.add_argument('--processors', help='List of Processors (can be empty)',default="None")
    parser.add_argument('--zip', help='zip file with the latex',default="None")    
    parser.add_argument('--std', help='standard replacements',default="replacements1.csv")    
    args = parser.parse_args()
    filename = get_path_from_name(args.md, debug_path ).replace("\\","/")
    filename = filename + "/" +args.md + ".md"
    proc = default_processors if args.processors == "None" else args.processors.split(",")
    for p in proc:
        print(p)
        physwiki_processors[p](filename, args)