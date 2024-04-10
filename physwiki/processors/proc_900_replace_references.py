
from physwiki.generic import read_text_file ,write_text_file
import re, os

uni = []

uni.extend( [chr(0x2474 + i) for i in range(20)] )
uni.extend( [chr(0x249C + i) for i in range(26)] )
uni.extend( [chr(0x1F110 + i) for i in range(26)] )
uni.extend( [chr(0x1F130 + i) for i in range(26)] )


def replace_ref(filename, args):
    print("replace_ref")

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
    


import physwiki as pwiki 

@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(replace_ref)