from typing import Any, List, Union


def convert_to_list(value_str: Any) -> List[str]:
    if type(value_str) is str:
        return [value_str]
    else: 
        return value_str

def fetch_dict_or_List(itemList: list) -> Union[List[dict], dict]:
    if len(itemList) == 1:
           return itemList[0]
    else:
        return itemList