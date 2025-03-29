import json
import os

class AgentMemory:
    GENERAL_INFORMATION_PATH = "../data/general_information.json"
    PERSISTENT_MEMORY_PATH = "../data/persistent_memory.json"

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
    
        with open(self.GENERAL_INFORMATION_PATH, "r") as file:
            self.general_information = json.load(file)

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
        with open(self.PERSISTENT_MEMORY_PATH, "a") as file:
            print(f"Persisting {self.persist_memory} to {self.PERSISTENT_MEMORY_PATH}")
            json.dump(self.relevant_retrieved_memory, file, indent=4)

        