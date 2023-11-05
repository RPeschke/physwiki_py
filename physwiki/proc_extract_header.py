from physwiki.generic import read_text_file ,write_text_file, physwiki_processors
import re, os
import pandas as pd

class groupping:
    def __init__(self) -> None:
        self.counter = 0
        
    def __call__(self, contition) :
        if contition:
            self.counter += 1
        return self.counter
    

def extract_header(filename, args):
    header = ""
    content = read_text_file(filename)
    
    content_sp = content.split("---")
    if len(content_sp) < 3:
        return ""
    
    groupping1 = groupping()
    
    grp = [[groupping1( len(x)>0 and x[0] != " " and x[0] != "-") , x  ] for x in content_sp[1].split("\n")]
    
    df = pd.DataFrame(grp, columns=["grp", "content"])
    
    df1 = df.groupby("grp").agg({"content": lambda x: "\n".join(x)})
    df1 = df1[ df1.content.apply(len) >0].copy()


    
    # convert to dict

    
    # find first character that is a letter or number
    def find_first_letter(x):
        for i, c in enumerate(x):
            if c.isalnum():
                return i
        return -1
    
    def remove_prefix(x):
        return x[find_first_letter(x):]
    
    
    df1["key"] = df1.content.apply(lambda x: x.split(":")[0].strip())
    df1["value"] = df1.content.apply(lambda x: remove_prefix(x.split(":")[1].strip()) )
    header_dict = dict(zip(df1.key, df1.value))
    
    
    year_journal = content[content.find('---', 10):content.find('##')]
    content = content[content.find('##'):]
    
    title = " ".join(str(header_dict.get("title")).replace("\n"," ").split())
    
    content = "# " + title + "\n\n" +str(header_dict.get("author")) + "\n\n" +year_journal+  '\n\n## Abstract\n\n' + str(header_dict.get("abstract")) + "\n\n" + content
    
    write_text_file(filename, content)
    
    
physwiki_processors['extract_header'] = extract_header
