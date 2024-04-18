
import os
import re
from collections import Counter
from physwiki.md_updater_base import md_updater_base

# This dictionary will map identifiers to figure numbers

class md_reference_updater(md_updater_base):
    def __init__(self, reference_type, display_str, display_ref_str) -> None:
        self.reference_type = reference_type
        self.diplay_type = display_str
        self.display_type_ref = display_ref_str
        self.identifier_to_figure = {}
        # Pattern for initial figure declarations
        
        self.declaration_pattern = fr'\[([^\]]*)\]\s*\((#\w+@{self.reference_type}@new)\)'
        self.reference_pattern = fr'\[([^\]]*)\]\s*\((#\w+@{self.reference_type})\)'
        
        self.identifier_pattern = fr'\(#(\w+@{self.reference_type}@new)\)'

        self.ref_suffix = f'@{self.reference_type}'
        self.dec_suffix = f'@{self.reference_type}@new'

        #self.declaration_pattern = r'\[([^\]]*)\]\s*\((#\w+@figure@new)\)'
        
        # Pattern for figure references that need updating
        #self.reference_pattern = r'\[([^\]]*)\]\s*\((#\w+@figure)\)'



    def check_for_duplicate_identifiers(self, content):
        # Pattern to find all figure:new and figure identifiers
        identifiers = re.findall(self.identifier_pattern, content)
        
        # Count occurrences of each identifier
        identifier_counts = Counter(identifiers)
        
        # Find duplicates
        duplicates = [identifier for identifier, count in identifier_counts.items() if count > 1]
        return duplicates


    def update_figure_declarations_and_collect_identifiers(self, content):
        # Counter for figure numbers
        figure_count = 1

        def declaration_replacer(match):
            nonlocal figure_count
            identifier = match.group(2)  # Extract the identifier
            new_text = f"{self.diplay_type}{figure_count}"
            self.identifier_to_figure[identifier] = figure_count  # Map identifier to figure number
            figure_count += 1
            return f"[{new_text}]({identifier})"

        # Update figure declarations and collect identifiers
        updated_content, _ = re.subn(self.declaration_pattern, declaration_replacer, content)
        return updated_content

    def update_figure_references(self, content):
        def reference_replacer(match):
            identifier = match.group(2)  # Extract the identifier
            # Replace with the corresponding figure number, keep original identifier
            new_figure_count = self.identifier_to_figure.get(identifier.replace(self.ref_suffix, self.dec_suffix), -1)
            
            return f"[{self.display_type_ref}{new_figure_count}]({identifier})"

        # Update figure references based on collected identifiers
        updated_content, _ = re.subn(self.reference_pattern, reference_replacer, content)
        return updated_content

    def process_file(self, content):
        duplicates = self.check_for_duplicate_identifiers(content)
        if duplicates:
            print(f"Error: Duplicate identifiers found: {', '.join(duplicates)}")
            return content
        
        # Update figure declarations and collect identifiers
        content = self.update_figure_declarations_and_collect_identifiers(content)
        
        # Update references to those figures
        content = self.update_figure_references(content)

        return content
        
