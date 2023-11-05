from physwiki.generic import read_text_file ,write_text_file, physwiki_processors



def remove_line_endings(filename, args):
    
    content = read_text_file(filename)
    content = content.replace("\n\n", "$$$$$$$$$$$")
    content = content.replace("\n", " ")
    content = content.replace("$$$$$$$$$$$", "\n\n")
    write_text_file(filename, content)
    

physwiki_processors['remove_line_endings'] = remove_line_endings
