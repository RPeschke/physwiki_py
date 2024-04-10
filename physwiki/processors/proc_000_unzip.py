from physwiki.generic import read_text_file ,write_text_file, try_create_dir, get_path_from_name


import physwiki as pwiki 

import re, os
import time



def unzip_archive(filename, path):
    import zipfile
    #path = os.path.dirname(os.path.realpath(filename))
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(path)







def unzip(Filename, args):
    print('unzip')

    zip_path = args.zip
    md_path  = args.md
    f2 = get_path_from_name(md_path)
    try_create_dir(f2)
    try:
        unzip_archive(zip_path, f2)
        os.rename(f2 + "/" + os.listdir(f2)[0], f2 + "/src")
    except:
        print("Error in unzipping: ", zip_path)
        pass
    

    time.sleep(1)




@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(unzip)

