from tools.store_into_memory import StoreIntoMemory, store_into_memory

tools = [StoreIntoMemory]

tool_calls = {
    "StoreIntoMemory" : store_into_memory
}