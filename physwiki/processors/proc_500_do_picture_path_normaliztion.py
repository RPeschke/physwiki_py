from physwiki.generic import read_text_file ,write_text_file


def do_picture_path_normalization(filename, args):
    print('do_picture_path_normalization')
    content = read_text_file(filename)
    
    
    content = content.replace(r'){width="\\textwidth"}', ".jpg)")
    content = content.replace("![image](20", "\n![image](src/images/20")
    write_text_file(filename, content)
    
    

import physwiki as pwiki 

@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(do_picture_path_normalization)
