from physwiki.generic import read_text_file ,write_text_file, latex_to_text
import re
from pylatexenc.latex2text import LatexNodes2Text
import os

def do_latex_to_text(filename, args):
    print("do_latex_to_text")
    content = read_text_file(filename)
    pattern = r"\$.*?\$"
    matches = re.findall(pattern, content, re.DOTALL)
    
    content += "\n\n## Latex Replacements\n\n"
    equation_getter_function = "get_eq"
    latex_replacements = ""
    for index, match in enumerate(matches):
        print(match)
        print("-------------------------------------")
        begin = match.find("$")
        end = match.find("$", begin+1)
        print(match[begin+1:end])
        print("=====================================")
        
        eq_string = 'r"""' + match[begin+1:end] +'"""'
        non_latex = LatexNodes2Text().latex_to_text(match[begin+1:end] )
        f = non_latex.find("\n")
        end_str = "" if f == -1 else "\n\n"
        non_latex = non_latex.strip()
        non_latex = " ".join(non_latex.split())
        

        
        # find pattern [...,...]
        non_latex_open = non_latex.find("[") 
        
        non_latex_close = non_latex.find("]") 
        
        non_latex_comma = non_latex.find(",") 
        eq_nr = f"{index}"
        if non_latex_close != -1 and non_latex_open != -1 and non_latex_comma != -1:
            non_latex = non_latex[non_latex_open+1:non_latex_close]
            non_latex_sp = non_latex.split(",")
            txt = "["+"][".join(non_latex_sp)+"]"
            
        else:
            txt = f"[{non_latex}](#python@{equation_getter_function}({eq_nr}))" + end_str
        
        content = content.replace(match, txt)
        latex_replacements += f"{eq_string},\n"
        
        
        
        
       # ret += "\n\n### inline_eq_"+ str(index)  + "\n\n" + match + "\n\n"

    
    latex_replacements_filename = "generated/latex_replacements.py"
    content += "\n"    
    content += f'''[python]:include "{latex_replacements_filename}"'''
    
    latex_replacements = f"""
from physwiki.generic import  latex_to_text


latex_replacements__=[
    {latex_replacements}
  ]

def {equation_getter_function}(x):
    return latex_to_text(latex_replacements__[x])

"""
    directory_path = os.path.dirname(filename)
    joined_path = os.path.join(directory_path, latex_replacements_filename)
    write_text_file(joined_path, latex_replacements)
    
    
        
        
    
    
    write_text_file(filename, content)
    


import physwiki as pwiki 

@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(do_latex_to_text)