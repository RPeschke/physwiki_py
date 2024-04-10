from physwiki.generic import read_text_file ,write_text_file
import re
from pylatexenc.latex2text import LatexNodes2Text


def do_latex_to_text(filename, args):
    print("do_latex_to_text")
    content = read_text_file(filename)
    pattern = r"\$.*?\$"
    matches = re.findall(pattern, content, re.DOTALL)
    
    #content += "\n\n## Latex Replacements\n\n"
    #ret = ""
    for index, match in enumerate(matches):
        print(match)
        print("-------------------------------------")
        begin = match.find("$")
        end = match.find("$", begin+1)
        print(match[begin+1:end])
        print("=====================================")
        
        
        non_latex = LatexNodes2Text().latex_to_text(match[begin+1:end])
        f = non_latex.find("\n")
        end_str = "" if f == -1 else "\n\n"
        non_latex = non_latex.strip()
        non_latex = " ".join(non_latex.split())
        
        # find pattern [...,...]
        non_latex_open = non_latex.find("[") 
        
        non_latex_close = non_latex.find("]") 
        
        non_latex_comma = non_latex.find(",") 
        
        if non_latex_close != -1 and non_latex_open != -1 and non_latex_comma != -1:
            non_latex = non_latex[non_latex_open+1:non_latex_close]
            non_latex_sp = non_latex.split(",")
            txt = "["+"][".join(non_latex_sp)+"]"
            
        else:
            txt = "[`" + non_latex + "`](#inline_eq_"+ str(index) + ")" + end_str
        
        content = content.replace(match, txt)
        
       # ret += "\n\n### inline_eq_"+ str(index)  + "\n\n" + match + "\n\n"
        
    #content += ret
    
        
        
    
    
    write_text_file(filename, content)
    


import physwiki as pwiki 

@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(do_latex_to_text)