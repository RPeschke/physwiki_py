import pyConfigFiles as pcf 
import re
import inspect

class physwiki_script_base_class(pcf.base):
    def __init__(self) -> None:
        super().__init__()
        self.processors = []
    
    def add_processor(self, p,  level=None):
        """
        Add a processor to the processors list with a specified level.
        If the level is None, determine the level based on the calling file's name.

        :param p: Processor name
        :param level: The level of the processor, if already known
        """
        if level is None:
            # Get the calling file's path
            caller_filepath = inspect.stack()[1].filename

            # Check if the filename starts with 'proc_' followed by numbers
            match = re.match(r'.*proc_(\d+)_', caller_filepath)
            if match:
                # Use the number in the filename as the level
                level = int(match.group(1))
            else:
                # Set level to infinity if the filename pattern does not match
                level = float('inf')

        self.processors.append( [level , p ] )
    