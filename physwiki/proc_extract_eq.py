from physwiki.formula_as_file import formula_as_file_internal
from physwiki.generic import read_text_file ,write_text_file, physwiki_processors

import re, os


def extract_eq(filename, args):
    content = read_text_file(filename)

    pattern = r"\$\$.*?\$\$"
    matches = re.findall(pattern, content, re.DOTALL)
    path = os.path.dirname(os.path.realpath(filename))
    try_create_dir(path + "/extracted")
    try_create_dir(path + "/generated") 
    
    for i, match in enumerate(matches):
        print(match)
        f = path + "/extracted/eq_" + str(i) +".tex"
        write_text_file(f, match[2:-2])
        formula = read_text_file(f)
        f_png = path + "/generated/eq_" + str(i) +".png"
        formula_as_file_internal(formula, f_png)
        content = content.replace(match, "\n\n![](generated/eq_" + str(i) +".png)\n\n")
        

        print("=====================================")
        
    write_text_file(filename, content)
    
    
    
physwiki_processors['extract_eq'] = extract_eq