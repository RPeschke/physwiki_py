from physwiki.generic import read_text_file ,write_text_file, physwiki_processors,try_create_dir, get_path_from_name
import re, os
import time



def unzip_archive(filename, path):
    import zipfile
    #path = os.path.dirname(os.path.realpath(filename))
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(path)







def zip_to_md(Filename, args):
    
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
    tex = os.listdir(f2+"/src")[0]
    md = f2 + "/" + md_path + ".md"
    cmd = 'pandoc -s "' + f2+"/src/" + tex + '"  -o "' + md +'"'
    os.system(cmd)  
    return md


physwiki_processors['zip_to_md'] = zip_to_md