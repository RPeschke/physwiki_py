from physwiki.generic import read_text_file ,write_text_file, try_create_dir
import os, requests
import re, os


def formula_as_file_internal( formula, file):
    
    formula = formula.replace('\n', ' ')
    r = requests.get( 'http://latex.codecogs.com/png.latex?\dpi{{300}} {formula}'.format(formula=formula))
    f = open(file, 'wb')
    f.write(r.content)
    f.close()
    
    

def formula_as_file(filename):
    path = os.path.dirname(os.path.realpath(filename))

    #base name 
    base = os.path.basename(filename)
    base = os.path.splitext(base)[0]

    print(path)
    print(base)


       


    formula = read_text_file(filename)
    formula_as_file_internal(formula, path+"/" + base + ".png")


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
    
    
    

import physwiki as pwiki 

@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(extract_eq)
