import os, requests
from physwiki.generic import read_text_file 

def formula_as_file_internal( formula, file):
    
    formula = formula.replace('\n', ' ')
    r = requests.get( 'http://latex.codecogs.com/png.latex?\dpi{{300}} {formula}'.format(formula=formula))
    #print('http://latex.codecogs.com/gif.latex?%5Cdpi%7B300%7D%20%5Cbegin%7Bbmatrix%7D%202%20%26%200%20%5C%5C%200%20%26%202%20%5C%5C%20%5Cend%7Bbmatrix%7D')
    #print(r.url)
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
