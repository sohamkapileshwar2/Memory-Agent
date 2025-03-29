import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # Points to 'src/memory'
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..")) # Move up two levels to reach the root directory

data_folder_path = os.path.join(ROOT_DIR, "data")
os.chmod(data_folder_path, 0o777)

class AgentMemory:
    USER_INFO_PATH = f"{data_folder_path}/user_info.json"
    KNOWLEDGE_STORE_PATH = f"{data_folder_path}/knowledge_store.json"

    def __init__(self) -> None:
        self.user_info = {}
        self.retrieved_knowledge = {}
        self.read_user_info()
    
    def read_user_info(self) -> None:
        if not os.path.exists(self.USER_INFO_PATH):
            print(f"{self.USER_INFO_PATH} not found. Initializing empty agent memory.")
            self.user_info = {}  # Initialize as empty
            return
    
        with open(self.USER_INFO_PATH, "r") as file:
            self.user_info = json.load(file)

    def write_user_info(self) -> None:
        with open(self.USER_INFO_PATH, "w") as file:
            print(f"Persisting {self.user_info} to {self.USER_INFO_PATH}")
            json.dump(self.user_info, file, indent=4)

    def read_knowledge_store(self) -> None:
        if not os.path.exists(self.KNOWLEDGE_STORE_PATH):
            print(f"{self.KNOWLEDGE_STORE_PATH} not found. Initializing empty agent memory.")
            self.retrieved_knowledge = {}  # Initialize as empty
            return
    
        with open(self.KNOWLEDGE_STORE_PATH, "r") as file:
            self.retrieved_knowledge = json.load(file)

    def write_knowledge_store(self) -> None:
        with open(self.KNOWLEDGE_STORE_PATH, "w") as file:
            print(f"Persisting {self.retrieved_knowledge} to {self.KNOWLEDGE_STORE_PATH}")
            json.dump(self.retrieved_knowledge, file, indent=4)

        