from physwiki.generic import read_text_file ,write_text_file, physwiki_processors

def do_picture_path_normaliztion(filename, args):
    content = read_text_file(filename)
    
    
    content = content.replace(r'){width="\\textwidth"}', ".jpg)")
    content = content.replace("![image](2023", "\n![image](src/images/2023")
    write_text_file(filename, content)
    
    
physwiki_processors['do_picture_path_normaliztion'] = do_picture_path_normaliztion