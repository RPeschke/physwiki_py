from physwiki.generic import read_text_file ,write_text_file



def remove_line_endings(filename, args):
    print(remove_line_endings)

    content = read_text_file(filename)
    content = content.replace("\n\n", "$$$$$$$$$$$")
    content = content.replace("\n", " ")
    content = content.replace("$$$$$$$$$$$", "\n\n")
    write_text_file(filename, content)
    



import physwiki as pwiki 

@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(remove_line_endings)