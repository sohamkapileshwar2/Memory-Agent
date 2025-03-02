import json
import os

class AgentMemory:
    AGENT_MEMORY_PATH = "core_memory.json"

    def __init__(self) -> None:
        self.core_memory = {}
        self.read_agent_memory()
    
    def read_agent_memory(self) -> None:
        if not os.path.exists(self.AGENT_MEMORY_PATH):
            print(f"{self.AGENT_MEMORY_PATH} not found. Initializing empty agent memory.")
            self.core_memory = {}  # Initialize as empty
            return
    
        with open(self.AGENT_MEMORY_PATH, "r") as file:
            self.core_memory = json.load(file)

    def persist_agent_memory(self) -> None:
        with open(self.AGENT_MEMORY_PATH, "w") as file:
            print(f"Persisting {self.core_memory} to {self.AGENT_MEMORY_PATH}")
            json.dump(self.core_memory, file, indent=4)

