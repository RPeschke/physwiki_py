from physwiki.generic import read_text_file ,write_text_file
import physwiki as pwiki 


def adjust_title_level(filename, args):
    print("adjust_title_level")
    content = read_text_file(filename)
    content = content.replace("# ", "## ")
    write_text_file(filename, content)
    
    


@pwiki.configuration
def config(obj: pwiki.physwiki_script_base_class):
    obj.add_processor(adjust_title_level)