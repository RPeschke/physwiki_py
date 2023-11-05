from physwiki.generic import read_text_file ,write_text_file, physwiki_processors



def adjust_title_level(filename, args):
    content = read_text_file(filename)
    content = content.replace("# ", "## ")
    write_text_file(filename, content)
    
    
physwiki_processors["adjust_title_level"] = adjust_title_level
