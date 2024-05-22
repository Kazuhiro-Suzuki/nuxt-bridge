import datetime
from dataclasses import asdict
from typing import List, Callable, Any, Optional
import dateutil.parser
import re


def to_camel_case(snake_str: str) -> str:
    if snake_str.startswith('_') or '_' not in snake_str:
        return snake_str
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def to_camel_case_recursive(data, replace=True):
    if isinstance(data, list):
        return [to_camel_case_recursive(x, replace) for x in data]
    if isinstance(data, dict):
        if replace:
            return {
                to_camel_case(key): to_camel_case_recursive(value)
                for key, value in data.items()
            }
        for key in list(data.keys()):
            data_ = to_camel_case_recursive(data[key])
            data[key] = data_
            data[to_camel_case(key)] = data_
    return data


def dataclass_as_dict(obj):
    return to_camel_case_recursive(asdict(obj))


def get_fields(dataclass) -> List[str]:
    return list(dataclass.__dict__['__dataclass_fields__'].keys())


def get_date_fields(dataclass) -> List[str]:
    return [
        v.type
        for k, v
        in dataclass.__dict__['__dataclass_fields__'].items()
        if v.type == Optional[datetime.date] or v.type == datetime.date
    ]


def parse_date_fields(data, *date_fields: str) -> dict:
    _date_fields = set(date_fields)

    def _(key: str, value):
        if key in _date_fields:
            if value is not None and value != '':
                return dateutil.parser.parse(value).date()
            return None
        return value

    return {k: _(k, v) for k, v in data.items()}


def select_fields(data, *fields: str, default_factory: Callable[[str], Any] = None) -> dict:
    if default_factory is None:
        def _(key):
            return None
        default_factory = _
    return {
        key: data[key] if key in data else default_factory(key)
        for key in fields
    }


def parse_datetime_fields(data, *datetime_fields: List[str]) -> dict:
    _datetime_fields = set(datetime_fields)

    def _(key: str, value):
        if key in _datetime_fields:
            if value is not None and value != '':
                return dateutil.parser.parse(value)
            return None
        return value

    return {k: _(k, v) for k, v in data.items()}


def replace_api_with_domain(site_domain: str, model_values: list) -> List[dict]:
    instances = []
    for model_value in model_values:
        pattern = re.compile(r'/api/v1/')
        result = pattern.sub(site_domain + "/api/v1/", model_value['body'])
        model_value['body'] = result
        instances.append(model_value)
    return instances