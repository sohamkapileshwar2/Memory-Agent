import json
import os

class AgentMemory:
    GENERAL_INFORMATION_PATH = "data/general_information.json"
    PERSISTENT_MEMORY_PATH = "data/persistent_memory.json"

    def __init__(self) -> None:
        # User and other agent preferences used for personalising the LLM. This will be a part of the system prompt and contents will be updated from the user input and persistent memory.
        self.general_information = {}
        self.relevant_retrieved_memory = {}
        self.read_general_information()
    
    def read_general_information(self) -> None:
        if not os.path.exists(self.GENERAL_INFORMATION_PATH):
            print(f"{self.GENERAL_INFORMATION_PATH} not found. Initializing empty agent memory.")
            self.general_information = {}  # Initialize as empty
            return
    
        try:
            with open(self.GENERAL_INFORMATION_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)  # Attempt to load JSON
                
                if isinstance(data, dict):  # Ensure it's a valid dictionary
                    self.general_information = data
                else:
                    print("Warning: JSON is valid but not a dictionary. Initializing empty data.")
                    self.general_information = {}

        except json.JSONDecodeError:
            print(f"Error: {self.GENERAL_INFORMATION_PATH} contains invalid JSON. Resetting to empty.")
            self.general_information = {}  # Reset on JSON error
        except Exception as e:
            print(f"Unexpected error reading {self.GENERAL_INFORMATION_PATH}: {e}")
            self.general_information = {}  # Handle other unknown errors

    def persist_general_information(self) -> None:
        with open(self.GENERAL_INFORMATION_PATH, "w") as file:
            print(f"Persisting {self.general_information} to {self.GENERAL_INFORMATION_PATH}")
            json.dump(self.general_information, file, indent=4)

    def read_data(self) -> None:
        if not os.path.exists(self.PERSISTENT_MEMORY_PATH):
            print(f"{self.PERSISTENT_MEMORY_PATH} not found. Initializing empty agent memory.")
            self.relevant_retrieved_memory = {}  # Initialize as empty
            return
    
        with open(self.PERSISTENT_MEMORY_PATH, "r") as file:
            self.relevant_retrieved_memory = json.load(file)

    def persist_data(self) -> None:
        with open(self.PERSISTENT_MEMORY_PATH, "w") as file:
            print(f"Persisting {self.relevant_retrieved_memory} to {self.PERSISTENT_MEMORY_PATH}")
            json.dump(self.relevant_retrieved_memory, file, indent=4)

        