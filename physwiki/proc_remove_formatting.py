
from physwiki.generic import read_text_file ,write_text_file, physwiki_processors
import re



def remove_formatting(filename, args):
    content = read_text_file(filename)

    # find pattern ::: widetext  ... :::
    pattern = r"::: center.*?:::"
    matches = re.findall(pattern, content, re.DOTALL)
    for match in matches:
        print(match)
        print("-------------------------------------")
        begin = match.find("\n")
        end = match.find(":::", begin+1)
        print(match[begin:end])
        print("=====================================")
        content = content.replace(match, match[begin:end])
        
    
    
    write_text_file(filename, content)


physwiki_processors["remove_formatting"] = remove_formatting