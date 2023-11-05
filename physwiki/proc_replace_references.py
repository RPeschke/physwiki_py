from physwiki.formula_as_file import formula_as_file_internal
from physwiki.generic import read_text_file ,write_text_file, physwiki_processors
import re, os


def replace_ref(filename, args):
    # find pattern \[ number \]]    
    content = read_text_file(filename)
    ref_index = content.find("## References")
    content_1 = content[:ref_index]
    content_2 = content[ref_index:]
    
    for i, u in enumerate(uni):
        content_1 = content_1.replace( "\["+str(i+1)+"\]" , "["+u+"](#ref_"+str(i+1)+")")
        
    
    for i, u in enumerate(uni):
        content_2 = content_2.replace( "\["+str(i+1)+"\]" , "### ref_"+str(i+1)+"\n\n" + u + " "  ) 
        
    content = content_1 + content_2    
    write_text_file(filename, content) 
    


physwiki_processors['replace_ref'] = replace_ref