import os
import json
from typing import Optional

class SystemPromptManager:
    def __init__(self, prompt_file: str = "system_prompt.txt"):
        self.prompt_file = prompt_file
        self.prompt_path = os.path.join(os.path.dirname(__file__), "..", prompt_file)
    
    def get_prompt(self) -> str:
        """Get the current system prompt"""
        try:
            with open(self.prompt_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            # Return default prompt if file doesn't exist
            default_prompt = "You are a helpful assistant."
            self.set_prompt(default_prompt)
            return default_prompt
    
    def set_prompt(self, prompt: str) -> bool:
        """Set the system prompt"""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.prompt_path), exist_ok=True)
            
            with open(self.prompt_path, 'w') as file:
                file.write(prompt.strip())
            return True
        except Exception as e:
            print(f"Error setting prompt: {e}")
            return False
    
    def update_prompt(self, new_prompt: str) -> bool:
        """Update the system prompt (alias for set_prompt)"""
        return self.set_prompt(new_prompt)

# Global instance
prompt_manager = SystemPromptManager() 