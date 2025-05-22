from ._BaseHandler import BaseHandler
from typing import Any

class SectionManager(BaseHandler):
    def __init__(self):
        super().__init__() # Call BaseHandler's __init__ if it has one
        self.sections = {}
        self.current_fiber_section_tag = None
        # _COMMAND_RULES is defined as a property below

    def clear(self):
        """Reset internal data maintained by the handler."""
        self.sections = {}
        self.current_fiber_section_tag = None
        # If BaseHandler had a clear method that needs calling:
        # super().clear() 

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            'section': {
                "positional": ["secType", "secTag", "secArgs*"],
                "options": {} 
            },
            'patch': {
                "positional": ["patchType", "patchArgs*"], 
                "options": {}
            },
            'layer': {
                "positional": ["layerType", "layerArgs*"], 
                "options": {}
            }
        }

    def handles(self) -> list[str]:
        return ['section', 'patch', 'layer']

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        parsed_args = self._parse(func_name, *arg_map.get('args', ()), **arg_map.get('kwargs', {}))
        
        # print(f"SectionManager --- Raw input for {func_name}: args={arg_map.get('args')}, kwargs={arg_map.get('kwargs')}")
        # print(f"SectionManager --- Parsed args for {func_name}: {parsed_args}")

        if func_name == 'section':
            self._handle_section(parsed_args)
        elif func_name == 'patch':
            self._handle_patch(parsed_args)
        elif func_name == 'layer':
            self._handle_layer(parsed_args)
        else:
            print(f"SectionManager: Warning - Unknown function '{func_name}' was routed to SectionManager.")

    def _handle_section(self, parsed_args: dict[str, Any]):
        sec_type = parsed_args.get('secType')
        sec_tag_raw = parsed_args.get('secTag')

        if sec_type is None or sec_tag_raw is None:
            print(f"SectionManager: Error - 'secType' or 'secTag' is missing in parsed arguments for section. Args: {parsed_args}")
            return

        try:
            sec_tag = int(sec_tag_raw)
        except ValueError:
            print(f"SectionManager: Error - 'secTag' for section must be an integer. Got: {sec_tag_raw}")
            return

        self.sections[sec_tag] = {
            'type': sec_type,
            'data': parsed_args, 
            'patches': [],       
            'layers': []         
        }

        if sec_type == 'Fiber':
            self.current_fiber_section_tag = sec_tag
            print(f"SectionManager: Processed section {sec_tag} of type {sec_type}. Current Fiber context set to {sec_tag}.")
        else:
            if self.current_fiber_section_tag is not None: # If context was set
                 print(f"SectionManager: Changing active section context from Fiber section {self.current_fiber_section_tag} to section {sec_tag} of type {sec_type}.")
            self.current_fiber_section_tag = None 
            print(f"SectionManager: Processed section {sec_tag} of type {sec_type}. Fiber context cleared or not applicable.")


    def _handle_patch(self, parsed_args: dict[str, Any]):
        if self.current_fiber_section_tag is None:
            print("SectionManager: Warning - 'patch' command called outside of an active 'Fiber' section context. Patch ignored.")
            return
        
        self.sections[self.current_fiber_section_tag]['patches'].append(parsed_args)
        print(f"SectionManager: Processed patch for Fiber section {self.current_fiber_section_tag}. Patch data: {parsed_args}")

    def _handle_layer(self, parsed_args: dict[str, Any]):
        if self.current_fiber_section_tag is None:
            print("SectionManager: Warning - 'layer' command called outside of an active 'Fiber' section context. Layer ignored.")
            return

        self.sections[self.current_fiber_section_tag]['layers'].append(parsed_args)
        print(f"SectionManager: Processed layer for Fiber section {self.current_fiber_section_tag}. Layer data: {parsed_args}")
