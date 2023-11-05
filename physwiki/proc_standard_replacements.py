
from physwiki.generic import read_text_file ,write_text_file, physwiki_processors
import pandas as pd



def standard_replacements(filename, args):
    content = read_text_file(filename)
    df_replacements = pd.read_csv(args.std )
    df_replacements.dropna(inplace=True)
    
    for i,x in df_replacements.iterrows():
        content = content.replace(x["origin"], x["replace"])
        

    
    write_text_file(filename, content)


physwiki_processors['standard_replacements'] = standard_replacements
