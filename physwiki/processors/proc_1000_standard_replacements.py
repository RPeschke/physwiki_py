
from physwiki.generic import read_text_file ,write_text_file
import pandas as pd



def standard_replacements(filename, args):
    print("standard_replacements")

    content = read_text_file(filename)
    df_replacements = pd.read_csv(args.std )
    df_replacements.dropna(inplace=True)
    
    for i,x in df_replacements.iterrows():
        content = content.replace(x["origin"], x["replace"])
        

    
    write_text_file(filename, content)



import physwiki as pwiki 

@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(standard_replacements)