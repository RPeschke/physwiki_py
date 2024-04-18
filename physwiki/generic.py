#function that reads in text file 
import os
import numpy as np




def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        return content
    

def save_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
        
def read_text_file(text_file):
    # read in unicode text file
    
    
    f = open(text_file, 'r' , encoding='utf-8')
    text = f.read()
    f.close()
    return text

def write_text_file(text_file, text):
    f = open(text_file, 'w' , encoding='utf-8')
    f.write(text)
    f.close()
    
    
def try_create_dir(path):
    try:
        os.mkdir(path)
    except:
        pass
    
    
def get_path_from_name(md_name , path =None ):
    
    
    global_path = os.getcwd() if path == None else path
    
    year_path = str(int(np.floor(int(md_name.split()[0])/10)*10))
    ret = global_path + "\\" + year_path + "\\" + md_name
    return ret
    
physwiki_processors = {}