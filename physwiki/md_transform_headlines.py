from physwiki.md_updater_base import md_updater_base
import re

class transform_headlines(md_updater_base):
    def process_file(self, content):

        # Define a pattern that matches the headlines with identifiers and optional classes
        pattern = r'^(#+\s.*?)(\s*\{#.*?\})(\s*\..*?)?$'
        
        # Replace the matched headlines with just the text part (group 1 captured by the pattern)
        transformed_content = re.sub(pattern, r'\1', content, flags=re.MULTILINE)
        
        return transformed_content
