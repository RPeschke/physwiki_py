from physwiki.generic import read_text_file ,write_text_file, try_create_dir, get_path_from_name


import physwiki as pwiki 

import re, os
import time



def unzip_archive(filename, path):
    import zipfile
    #path = os.path.dirname(os.path.realpath(filename))
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(path)







def latex_to_md(Filename, args):
    print('latex to md')
    md_path  = args.md
    f2 = get_path_from_name(md_path)


    tex = os.listdir(f2+"/src")[0]
    md = f2 + "/" + md_path + ".md"
    cmd = 'pandoc -s "' + f2+"/src/" + tex + '"  -o "' + md +'"'
    os.system(cmd)  
    return md


@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(latex_to_md)

