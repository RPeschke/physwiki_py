import os, requests
from physwiki.generic import read_text_file 

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
