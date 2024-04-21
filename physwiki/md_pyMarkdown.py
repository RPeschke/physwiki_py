import re

import re
import pandas as pd
from datetime import datetime
import importlib.util
import sys
import base64
import inspect
import os


import hashlib

from physwiki.pyMarkdown import set_Env, get_Env
from physwiki.md_updater_base import md_updater_base




class new_scope():
    def __init__(self) -> None:
        self.local_scope = []
        self.local_scope1 = {}
        self.result_var = "result"
        exec('def get_arguments(*args, **kargs): return [args, kargs]', globals(), self.local_scope1 )
        script_path = os.path.abspath(__file__)
        script_path = os.path.dirname(script_path)
        script_path =os.path.join(script_path,  "./md_py/md_defaults.py") 
        self.import_from_filepath_full(script_path)
        
    def import_from_filepath_full(self, filepath):
        # Extract module name from filepath
        module_name = filepath.split('/')[-1].split('.')[0]
    
        # Create a module spec from the filepath
        spec = importlib.util.spec_from_file_location(module_name, filepath)
    
        # Create a new module based on the spec
        module = importlib.util.module_from_spec(spec)
    
        # Add the module to sys.modules
        sys.modules[module_name] = module
        
        
        # Execute the module (run its code)
        spec.loader.exec_module(module)
        self.local_scope.append(module)


        
    
    def get_object_from_scope(self, function_name):
        function_name = function_name.strip()
        x = self.local_scope1.get(function_name)
        if x is not None:
            return x
        
        for obj in self.local_scope:
            # Try to get the function directly instead of iterating over all attributes
            func = getattr(obj, function_name, None)
            if func is not None:
                return func  # Call the function with args and return its result
        raise ValueError(f"Function {function_name} not found in any scope objects.")


    def split_function_call(self, function_call):
        # Regular expression to match 'function_name(arguments)'
        match = re.match(r'(\w+)\((.*)\)', function_call)
        if match:
            function_name = match.group(1)
            arguments = match.group(2)
            exec(f'{self.result_var} = get_arguments({arguments})', globals(),  self.local_scope1 )
            return function_name, self.local_scope1[self.result_var]
        elif "(" in function_call:
            return function_call.split("(")[0], [[],{}]
        else:
           return function_call, None 
            



    def __call__(self, code, Environment):
        set_Env(Environment)
        x = self.split_function_call(code)
        if x[1] is not None:
            return self.get_object_from_scope(x[0])(*x[1][0],**x[1][1] )

        return self.get_object_from_scope(x[0])
        
        
class md_text_replacement_base:

    def update_function(self, scope, env)    :
        pass

    def run_code(self, scope):
        pass

    def skip_update(self):
        return False

    





class md_update_md_links(md_text_replacement_base):
    
    pattern = re.compile(
        r'\[!\[([^\]]+)\]\(([^)]+)\)\]\(([^\)]+?\))'
    )
    def __init__(self, call, call_str) -> None:
        self.call = call
        self.call_str = call_str

    def update_function(self, scope, env):
        
        return f"[{scope(self.call, env)}]({self.call_str})"
    


class md_physwiki(md_text_replacement_base):
    def __init__(self, call) -> None:
        self.call = call


    def update_function(self, scope, env):
        textblock = scope(self.call, env)
        for i in range(10 , -1 ,-1 ):
            textblock = textblock.replace(f"filelevel{i}",f"filelevel{i+1}")
        
        if  textblock.find("<filelevel0>") != -1:
            raise Exception("to many levels of nesting")
        
        return f'<physwiki call="{self.call}"><filelevel0>\n{textblock}\n</filelevel0></physwiki>\n'

class md_physwiki_include(md_text_replacement_base):
    def __init__(self, fileName) -> None:
        self.fileName = fileName
    


    def run_code(self, scope):
        scope.import_from_filepath_full(self.fileName)

    def skip_update(self):
        return True

class md_physwiki_define(md_text_replacement_base):
    def __init__(self, attributes) -> None:
        self.attributes = attributes
        

    


    def run_code(self, scope):
        attributes = self.attributes
        first_position = attributes.find('"')
        last_position = attributes.rfind('"')
        definition = attributes[first_position+1:last_position]
        d = definition.split("=")    
        
        x1 = scope.split_function_call( d[1])
        if x1[1] is None and "'" in d[1]:
            exec(definition, globals(), scope.local_scope1)
        elif x1[1] is None:
            scope.local_scope1[d[0].strip()]  = scope.get_object_from_scope(x1[0])
        else:
            scope.local_scope1[d[0].strip()]  = scope.get_object_from_scope(x1[0])(*x1[1][0],**x1[1][1] )




    def skip_update(self):
        return True

    

class md_uplinks(md_text_replacement_base):
    def __init__(self, url, score) -> None:
        super().__init__()
        self.url = url
        call  = url.replace("#python@" , "")
        self.call  =call.replace("python@" , "")
        self.call_str = url if score != 10 else "#python@" + url


    def update_function(self, scope, env):
        return f"[{scope(self.call, env)}]({self.call_str})"
        





def update_markdown(content):
    scope = new_scope()
    

    links = extract_links_with_positions(content)
    for i, x in links.iterrows():
        x["obj"].run_code(scope)

    content = update_content(content , links, scope)

    return content


def update_markdown_file(filename, outFilename = None):
    
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()   
    
    content = update_markdown(content)
    
    file_path = outFilename if  outFilename is not None else filename

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    


def extract_complex_markdown_links(markdown_text, score):

    links = []
    for match in md_update_md_links.pattern.finditer(markdown_text):
        img_alt_text = match.group(1)  # Alt text of the nested image
        img_url = match.group(2)       # URL of the image
        link_url = match.group(3)      # URL of the outer link
        start_pos = match.start()
        if "#python@" not in link_url:
            continue

        offset = 1
        if  not "("  in link_url:
            offset = 0
            link_url = link_url[:-1]
        

        end_pos = match.end()+offset
        # Store details in a dictionary for better structure
        call  = link_url.replace("#python@" , "")
        call  = call.replace("python@" , "")
        call_str = link_url if score != 10 else "#python@" + link_url

        links.append({
                'start_pos': start_pos,
                'end_pos': end_pos,
                "score" : score,
                "obj"  : md_update_md_links(call,  call_str)

        })
       

    return links



    
    

def updated_custom_tags(markdown_text, score):
    def find_tags_and_content(text, tag):
        # Regex pattern to match tags and extract content
        pattern = re.compile(r'<{}>(.*?)</{}>'.format(tag, tag), re.DOTALL)
        
        # Find all matches in the provided text
        matches = pattern.finditer(text)
        
        return matches
    



    # Find all matches in the provided text
    matches = find_tags_and_content(markdown_text, "filelevel0")
    physwiki_endtag = "</physwiki>"
    code_blocks = []
    for match in matches:
        start_pos = markdown_text[:match.start()].rfind("<physwiki")
        end_pos   = markdown_text.find(physwiki_endtag, match.end())
        if end_pos == -1 or start_pos == -1:
            raise Exception("cant find begin or end tags")
        end_pos = end_pos+ len(physwiki_endtag)
        
        call_begin = markdown_text[: match.start()].find('"',start_pos)
        call_end = markdown_text[: match.start()].rfind('"')
        call = markdown_text[call_begin+1:call_end]

        code_blocks.append({
            'start_pos':start_pos,
            'end_pos': end_pos,
            "score" : score,
            "obj" : md_physwiki(call)

        })
    return code_blocks

def handle_physwiki_call(markdown_text, match, score):
    attributes = match.group(2)
    first_position = attributes.find('"')
    last_position = attributes.rfind('"')
    call = attributes[first_position+1:last_position]
    return {
            'start_pos':match.start(),
            'end_pos': match.end(),
            "score" : score,
            "obj" : md_physwiki(call)

        }

def handle_physwiki_include(markdown_text, match, score):
    attributes = match.group(2)
    first_position = attributes.find('"')
    last_position = attributes.rfind('"')
    file_path = attributes[first_position+1:last_position]
    return {
            'start_pos':match.start(),
            'end_pos': match.end(),
            "score" : score,
            "obj" : md_physwiki_include(file_path)

        }
    

def handle_physwiki_define(markdown_text, match, score):
    attributes = match.group(2)

    return {
            'start_pos':match.start(),
            'end_pos': match.end(),
            "score" : score,
            "obj" : md_physwiki_define(attributes)

        }


            
            

def find_custom_tags(markdown_text, score):
    
    # Regex pattern to match custom tags like <physwiki call="myFunction()"/>
    # This pattern captures the tag name and its attributes.
    pattern = re.compile(r'<(\w+)\s+([^>]+?)/>')

    # Find all matches in the provided text
    matches = pattern.finditer(markdown_text)
    code_blocks = []
    for match in matches:
        tag = match.group(1)
        attributes = match.group(2)
        if "physwiki" not in tag:
            continue
        
        attribute_name = attributes.split("=")[0]
        if attribute_name == "call":
            code_blocks.append( handle_physwiki_call(markdown_text, match , score) )
            
        
        if attribute_name == "include":
            code_blocks.append( handle_physwiki_include(markdown_text, match, score))
            

        if attribute_name == "define":
            code_blocks.append(  handle_physwiki_define(markdown_text, match, score) )
            
            
                               

    return code_blocks




def extract_links_with_positions(content):
    def get_links(content, regex, score):
        matches = regex.finditer(content)
        links = []
        for match in matches:
            start_pos = match.start()
            end_pos = match.end()
            if "#python@" not in content[start_pos: end_pos]:
                continue

            link_text = match.group(1)
            url = match.group(2)
            call  = url.replace("#python@" , "")
            call  =call.replace("python@" , "")
            call_str = url if score != 10 else "#python@" + url

            links.append({
                'start_pos': start_pos,
                'end_pos': end_pos,
                "score" : score,
                "obj" : md_uplinks(url ,score),
            })

        return links

    # This regex matches Markdown links in the format [Link Text](URL)
    link_pattern = re.compile(
        r'\[([^\]]+)\]\s*\(([^)]+)\)'
    )
    
    links = []
    links.extend(

        get_links(content, link_pattern,0 )
    )

    link_pattern = re.compile(
        r'\[([^\]]+)\]\s*\(\#python@([^\s]+?\([^\)]+\))\)'
    )
    
    links.extend(

        get_links(content, link_pattern,10)
    )
    
    

    links.extend(

        extract_complex_markdown_links(content, 20)
    )


    links.extend(
        find_custom_tags(content, 40)
    )
    links.extend(
        updated_custom_tags(content , 50)
    )
    df = pd.DataFrame(links)
    df = df.sort_values(by=['start_pos', 'score'], ascending=[True, False])
    df = df.drop_duplicates(subset='start_pos', keep='first')
    





    return df







class relative_string:
    def __init__(self, content) -> None:
        self.offset = 0
        self.content = content

    def replace(self, start_index, end_index, new_string):
        # Ensure indices are within the string length
        start_index +=  self.offset
        end_index   +=  self.offset
        if start_index < 0 or end_index > len(self.content) or start_index > end_index:
            raise ValueError("Invalid indices for the provided string.")
        
        # Construct the new string
        self.content = self.content[:start_index] + new_string + self.content[end_index:]
        self.offset += len(new_string) - (end_index - start_index )   
        return self.content       

    def __str__(self) -> str:
        return self.content

def update_content(content, links, scope):
    content1 = relative_string(content)
    for i, link in links.iterrows():
        obj = link["obj"]
        if obj.skip_update():
            continue
        
        
        env = {
            'line' :  content[:link['start_pos']].count('\n') + 1        
            }
        
        newString         = obj.update_function(scope, env) 
        content1.replace(link['start_pos'], link['end_pos'], newString)
        

    return str(content1)



class md_pyMarkdown(md_updater_base):
    def process_file(self, content):
        return update_markdown(content)
    