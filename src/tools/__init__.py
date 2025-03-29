from tools.store_general_information import StoreGeneralInformation, store_general_information,store_general_information_tool
from tools.store_data import StoreData, store_data,store_data_tool
from tools.retrieve_data import RetrieveData, retrieve_data,retrieve_data_tool


tools = [store_general_information_tool,store_data_tool,retrieve_data_tool]

tool_calls = {
    "StoreGeneralInformation" : store_general_information,
    "StoreData": store_data,
    "RetrieveData": retrieve_data,
}