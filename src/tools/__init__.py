from tools.store_general_information import StoreGeneralInformation, store_general_information
from tools.store_data import StoreData, store_data
from tools.retrieve_data import RetrieveData, retrieve_data


tools = [StoreGeneralInformation,StoreData,RetrieveData]

tool_calls = {
    "StoreGeneralInformation" : store_general_information,
    "StoreData": store_data,
    "RetrieveData": retrieve_data,
}